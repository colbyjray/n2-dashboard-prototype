"""Thin wrapper around the polymarket-us SDK client.

Phase 0 exposes construction and a handful of read methods used by
scripts/test_connection.py. Trading methods land in Phase 3.
"""
from __future__ import annotations

from typing import Any

try:
    from polymarket_us import PolymarketUS  # type: ignore[import-not-found]
except ImportError as exc:  # pragma: no cover
    raise ImportError(
        "polymarket-us is not installed. Run: pip install -r requirements.txt"
    ) from exc


def make_client(key_id: str, secret_key: str) -> PolymarketUS:
    return PolymarketUS(key_id=key_id, secret_key=secret_key)


def balances(client: PolymarketUS) -> Any:
    return client.account.balances()


def positions(client: PolymarketUS) -> Any:
    return client.portfolio.positions()


def open_orders(client: PolymarketUS) -> Any:
    return client.orders.list()
