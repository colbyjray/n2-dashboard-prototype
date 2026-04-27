"""In-process state shared between the scanner and the dashboard.

Single asyncio.Lock guards the dict-of-dicts. Reads return copies so
template rendering never touches a mutating structure.
"""
from __future__ import annotations

import asyncio
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class EventQuote:
    event_id: int
    event_slug: str
    title: str
    market_count: int
    total_ask: float
    total_fee: float
    edge: float
    edge_bps: int
    min_size: int
    notional_usdc: float
    legs: list[dict[str, float | str]] = field(default_factory=list)
    updated_at: str = ""


@dataclass
class ScannerStatus:
    state: str = "idle"  # idle | running | error | stopped
    last_run_at: str = ""
    last_run_duration_ms: int = 0
    last_error: str = ""
    cycle_count: int = 0
    watched_events: int = 0
    candidates_above_threshold: int = 0


class SharedState:
    def __init__(self) -> None:
        self._lock = asyncio.Lock()
        self._events: dict[int, EventQuote] = {}
        self._status = ScannerStatus()

    async def replace_events(self, quotes: list[EventQuote]) -> None:
        async with self._lock:
            self._events = {q.event_id: q for q in quotes}

    async def update_status(self, **kwargs: object) -> None:
        async with self._lock:
            for k, v in kwargs.items():
                if hasattr(self._status, k):
                    setattr(self._status, k, v)

    async def snapshot(self) -> tuple[ScannerStatus, list[EventQuote]]:
        async with self._lock:
            quotes = sorted(
                self._events.values(),
                key=lambda q: q.edge_bps,
                reverse=True,
            )
            status = ScannerStatus(**self._status.__dict__)
            return status, quotes


SHARED = SharedState()


def now_iso() -> str:
    return datetime.now().isoformat(timespec="seconds")
