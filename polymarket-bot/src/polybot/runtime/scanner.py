"""Arb scanner.

REST-polling implementation. Every `interval_seconds`:
1. List the top events by liquidity (single call).
2. For each event with 2+ markets, fetch BBO per market in parallel.
3. Compute total best-ask across legs, add fees, compare to $1.00.
4. Update shared in-memory state.
5. Log every candidate above the configured edge threshold to SQLite.

Pure read calls. The scanner never touches order placement, cancel, or
modify endpoints. The dashboard exposes start/stop controls but the
scanner can only observe.
"""
from __future__ import annotations

import asyncio
import logging
import sqlite3
import time
from dataclasses import dataclass

from polybot import secrets
from polybot.client import make_client
from polybot.fees import effective_taker_fee
from polybot.journal import DecisionRecord, write_decision
from polybot.runtime.state import SHARED, EventQuote, now_iso
from polybot.storage import connect, init_db

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class ScannerConfig:
    interval_seconds: float = 60.0
    top_n_events: int = 25
    min_edge_bps_to_log: int = 0  # log every candidate by default for calibration
    theta_taker: float = 0.05
    taker_rebate_fraction: float = 0.50
    sqlite_path: str = "data/polybot.sqlite"


def _amount_value(a: object) -> float | None:
    if a is None:
        return None
    v = a.get("value") if isinstance(a, dict) else getattr(a, "value", None)
    if v is None:
        return None
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


def _get(d: object, key: str, default: object = None) -> object:
    if isinstance(d, dict):
        return d.get(key, default)
    return getattr(d, key, default)


async def _bbo_for(client: object, slug: str) -> object | None:
    """One BBO call, off the event loop."""
    try:
        return await asyncio.to_thread(client.markets.bbo, slug)
    except Exception as exc:
        logger.warning("bbo failed for %s: %s", slug, exc)
        return None


async def _list_top_events(client: object, top_n: int) -> list[object]:
    """Single REST call. Active, not closed, sorted by liquidity desc."""
    try:
        from polymarket_us.types.events import EventsListParams

        params = EventsListParams(
            limit=top_n,
            active=True,
            closed=False,
            orderBy=["liquidity"],
            orderDirection="desc",
        )
        resp = await asyncio.to_thread(client.events.list, params)
        return list(_get(resp, "events") or [])
    except Exception as exc:
        logger.error("events.list failed: %s", exc)
        return []


async def _markets_for_event(client: object, event_slug: str) -> list[object]:
    """Fallback when events.list doesn't embed the markets list."""
    try:
        from polymarket_us.types.markets import MarketsListParams

        params = MarketsListParams(
            eventSlug=[event_slug],
            active=True,
            closed=False,
            limit=20,
        )
        resp = await asyncio.to_thread(client.markets.list, params)
        return list(_get(resp, "markets") or [])
    except Exception as exc:
        logger.warning("markets.list for %s failed: %s", event_slug, exc)
        return []


def _compute_edge(
    legs_best_ask: list[float],
    cfg: ScannerConfig,
) -> tuple[float, float, float]:
    """Return (total_ask, total_fee, edge)."""
    total_ask = sum(legs_best_ask)
    total_fee = sum(
        effective_taker_fee(p, cfg.theta_taker, cfg.taker_rebate_fraction)
        for p in legs_best_ask
        if 0.0 < p < 1.0
    )
    edge = 1.0 - total_ask - total_fee
    return total_ask, total_fee, edge


@dataclass
class FunnelCounts:
    events_returned: int = 0
    events_with_markets: int = 0
    events_with_valid_bbo: int = 0
    events_skipped_no_markets: int = 0
    events_skipped_one_leg: int = 0


async def _scan_once(
    client: object,
    cfg: ScannerConfig,
) -> tuple[list[EventQuote], int, FunnelCounts]:
    events = await _list_top_events(client, cfg.top_n_events)
    quotes: list[EventQuote] = []
    candidates_above_threshold = 0
    funnel = FunnelCounts(events_returned=len(events))

    for ev in events:
        event_slug = str(_get(ev, "slug") or "")
        markets = list(_get(ev, "markets") or [])

        # Fall back to markets.list when the embedded list is empty.
        if len(markets) < 2 and event_slug:
            markets = await _markets_for_event(client, event_slug)

        if len(markets) < 2:
            funnel.events_skipped_no_markets += 1
            continue

        funnel.events_with_markets += 1

        # Fetch BBO in parallel per leg.
        slugs = [str(_get(m, "slug") or "") for m in markets]
        bbos = await asyncio.gather(*(_bbo_for(client, s) for s in slugs if s))

        legs: list[dict[str, float | str]] = []
        legs_best_ask: list[float] = []
        legs_min_size: list[int] = []

        for market, bbo in zip(markets, bbos, strict=False):
            if bbo is None:
                continue
            best_ask = _amount_value(_get(bbo, "bestAsk"))
            ask_depth = _get(bbo, "askDepth")
            outcome = str(_get(market, "outcome") or _get(market, "title") or "")
            if best_ask is None or best_ask <= 0.0 or best_ask >= 1.0:
                continue
            legs.append(
                {
                    "outcome": outcome,
                    "slug": str(_get(market, "slug") or ""),
                    "best_ask": best_ask,
                    "ask_depth": int(ask_depth or 0),
                }
            )
            legs_best_ask.append(best_ask)
            legs_min_size.append(int(ask_depth or 0))

        if len(legs) < 2:
            funnel.events_skipped_one_leg += 1
            continue

        funnel.events_with_valid_bbo += 1

        total_ask, total_fee, edge = _compute_edge(legs_best_ask, cfg)
        edge_bps = int(round(edge * 10_000))
        min_size = min(legs_min_size) if legs_min_size else 0
        notional = total_ask * min_size

        quote = EventQuote(
            event_id=int(_get(ev, "id") or 0),
            event_slug=event_slug,
            title=str(_get(ev, "title") or ""),
            market_count=len(legs),
            total_ask=total_ask,
            total_fee=total_fee,
            edge=edge,
            edge_bps=edge_bps,
            min_size=min_size,
            notional_usdc=notional,
            legs=legs,
            updated_at=now_iso(),
        )
        quotes.append(quote)

        if edge_bps >= cfg.min_edge_bps_to_log:
            candidates_above_threshold += 1

    logger.info(
        "scan: events=%d with_markets=%d valid_bbo=%d quotes=%d",
        funnel.events_returned,
        funnel.events_with_markets,
        funnel.events_with_valid_bbo,
        len(quotes),
    )

    return quotes, candidates_above_threshold, funnel


def _log_candidate(conn: sqlite3.Connection, q: EventQuote) -> None:
    record = DecisionRecord(
        market_id=q.event_slug,
        market_question=q.title,
        side="ARB",
        price=q.total_ask,
        size=q.min_size,
        edge_bps=q.edge_bps,
        reasoning=(
            f"event={q.event_slug} legs={q.market_count} "
            f"total_ask={q.total_ask:.4f} fee={q.total_fee:.4f}"
        ),
        sanity_verdict="not-run-phase-1",
        placed=False,
    )
    write_decision(conn, record)


class Scanner:
    """Long-running scanner task. Owned by the FastAPI lifespan."""

    def __init__(self, cfg: ScannerConfig) -> None:
        self.cfg = cfg
        self._task: asyncio.Task[None] | None = None
        self._stop_event = asyncio.Event()

    async def start(self) -> None:
        if self._task and not self._task.done():
            return
        self._stop_event.clear()
        init_db(self.cfg.sqlite_path)
        self._task = asyncio.create_task(self._run(), name="polybot-scanner")
        logger.info("scanner started")

    async def stop(self) -> None:
        self._stop_event.set()
        if self._task:
            try:
                await asyncio.wait_for(self._task, timeout=5.0)
            except TimeoutError:
                self._task.cancel()
            self._task = None
        await SHARED.update_status(state="stopped")
        logger.info("scanner stopped")

    async def _run(self) -> None:
        await SHARED.update_status(state="running", last_error="")
        while not self._stop_event.is_set():
            await self._cycle_once()
            try:
                await asyncio.wait_for(
                    self._stop_event.wait(), timeout=self.cfg.interval_seconds
                )
            except TimeoutError:
                continue
        await SHARED.update_status(state="stopped")

    async def _cycle_once(self) -> None:
        creds = secrets.load_credentials()
        if not creds.polymarket_ready:
            await SHARED.update_status(
                state="error",
                last_error="no Polymarket credentials in keychain",
                last_run_at=now_iso(),
            )
            return

        start = time.monotonic()
        try:
            client = make_client(
                key_id=creds.polymarket_key_id or "",
                secret_key=creds.polymarket_secret_key or "",
            )
            quotes, candidates, funnel = await _scan_once(client, self.cfg)
            await SHARED.replace_events(quotes)

            if candidates:
                conn = connect(self.cfg.sqlite_path)
                try:
                    for q in quotes:
                        if q.edge_bps >= self.cfg.min_edge_bps_to_log:
                            _log_candidate(conn, q)
                finally:
                    conn.close()

            duration_ms = int((time.monotonic() - start) * 1000)
            await SHARED.update_status(
                state="running",
                last_run_at=now_iso(),
                last_run_duration_ms=duration_ms,
                cycle_count=(await self._next_cycle_count()),
                watched_events=len(quotes),
                candidates_above_threshold=candidates,
                events_returned=funnel.events_returned,
                events_with_markets=funnel.events_with_markets,
                events_with_valid_bbo=funnel.events_with_valid_bbo,
                events_skipped_no_markets=funnel.events_skipped_no_markets,
                events_skipped_one_leg=funnel.events_skipped_one_leg,
                last_error="",
            )
        except Exception as exc:
            logger.exception("scanner cycle failed")
            await SHARED.update_status(
                state="error",
                last_error=str(exc),
                last_run_at=now_iso(),
            )

    async def _next_cycle_count(self) -> int:
        status, _ = await SHARED.snapshot()
        return status.cycle_count + 1


SCANNER: Scanner | None = None


def get_or_create_scanner(cfg: ScannerConfig) -> Scanner:
    global SCANNER
    if SCANNER is None:
        SCANNER = Scanner(cfg)
    return SCANNER
