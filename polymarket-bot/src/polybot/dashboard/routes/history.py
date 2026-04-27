"""History page. Shows portfolio.activities() — trades, resolutions, deposits.

Read-only. No trade-placing methods are called from this module or anywhere
the dashboard reaches.
"""
from __future__ import annotations

import contextlib
import logging
from dataclasses import dataclass

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse

from polybot import secrets
from polybot.client import activities, make_client
from polybot.dashboard.auth import require_token

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/history", dependencies=[Depends(require_token)])


@dataclass
class TradeRow:
    when: str
    market: str
    side: str
    price: str
    qty: str
    cost: str
    realized_pnl: str
    aggressor: str


@dataclass
class ResolutionRow:
    when: str
    market: str
    side: str
    realized: str


@dataclass
class BalanceRow:
    when: str
    kind: str
    amount: str
    status: str


def _amount(a: object) -> str:
    if not a:
        return ""
    val = a.get("value") if isinstance(a, dict) else getattr(a, "value", None)
    cur = a.get("currency") if isinstance(a, dict) else getattr(a, "currency", "USD")
    if val is None:
        return ""
    return f"{val} {cur}"


def _get(d: object, key: str) -> object:
    if isinstance(d, dict):
        return d.get(key)
    return getattr(d, key, None)


def _classify(items: list[object]) -> tuple[list[TradeRow], list[ResolutionRow], list[BalanceRow]]:
    trades: list[TradeRow] = []
    resolutions: list[ResolutionRow] = []
    balance: list[BalanceRow] = []

    for a in items or []:
        atype = _get(a, "type")
        if atype == "ACTIVITY_TYPE_TRADE":
            t = _get(a, "trade") or {}
            aggressor = _get(t, "isAggressor")
            trades.append(
                TradeRow(
                    when=str(_get(t, "createTime") or ""),
                    market=str(_get(t, "marketSlug") or ""),
                    side=str(_get(t, "state") or ""),
                    price=_amount(_get(t, "price")),
                    qty=str(_get(t, "qty") or ""),
                    cost=_amount(_get(t, "costBasis")),
                    realized_pnl=_amount(_get(t, "realizedPnl")),
                    aggressor="taker" if aggressor else "maker",
                )
            )
        elif atype == "ACTIVITY_TYPE_POSITION_RESOLUTION":
            r = _get(a, "positionResolution") or {}
            after = _get(r, "afterPosition") or {}
            resolutions.append(
                ResolutionRow(
                    when=str(_get(r, "updateTime") or ""),
                    market=str(_get(r, "marketSlug") or ""),
                    side=str(_get(r, "side") or ""),
                    realized=_amount(_get(after, "realized")),
                )
            )
        elif atype in {
            "ACTIVITY_TYPE_ACCOUNT_DEPOSIT",
            "ACTIVITY_TYPE_ACCOUNT_ADVANCED_DEPOSIT",
            "ACTIVITY_TYPE_ACCOUNT_WITHDRAWAL",
            "ACTIVITY_TYPE_REFERRAL_BONUS",
            "ACTIVITY_TYPE_TRANSFER",
        }:
            change = _get(a, "accountBalanceChange") or {}
            txs = _get(change, "transactions") or []
            for tx in txs:
                balance.append(
                    BalanceRow(
                        when=str(_get(tx, "createTime") or ""),
                        kind=str(atype).replace("ACTIVITY_TYPE_", "").lower(),
                        amount=_amount(_get(tx, "amount")),
                        status=str(_get(tx, "status") or ""),
                    )
                )

    return trades, resolutions, balance


def _summary(trades: list[TradeRow]) -> dict[str, str]:
    total_trades = len(trades)
    realized = 0.0
    for t in trades:
        if t.realized_pnl:
            with contextlib.suppress(ValueError):
                realized += float(t.realized_pnl.split()[0])
    return {"trade_count": str(total_trades), "realized_pnl_usdc": f"{realized:.4f}"}


@router.get("", response_class=HTMLResponse)
async def history_page(request: Request) -> HTMLResponse:
    from polybot.dashboard.app import get_templates

    creds = secrets.load_credentials()
    return get_templates().TemplateResponse(
        request,
        "history.html",
        {"polymarket_ready": creds.polymarket_ready},
    )


@router.get("/data", response_class=HTMLResponse)
async def history_data(request: Request) -> HTMLResponse:
    from polybot.dashboard.app import get_templates

    creds = secrets.load_credentials()
    if not creds.polymarket_ready:
        return get_templates().TemplateResponse(
            request,
            "_history_data.html",
            {"ready": False, "error": "credentials not set"},
        )

    try:
        client = make_client(
            key_id=creds.polymarket_key_id or "",
            secret_key=creds.polymarket_secret_key or "",
        )
        resp = activities(client, limit=100)
        items = _get(resp, "activities") or []
        trades, resolutions, balance = _classify(items)
        summary = _summary(trades)
        return get_templates().TemplateResponse(
            request,
            "_history_data.html",
            {
                "ready": True,
                "trades": trades,
                "resolutions": resolutions,
                "balance": balance,
                "summary": summary,
            },
        )
    except Exception as exc:
        logger.exception("activities fetch failed")
        return get_templates().TemplateResponse(
            request,
            "_history_data.html",
            {"ready": False, "error": str(exc)},
        )
