"""Structured types shared across modules."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class BookLevel:
    price: float
    size: int


@dataclass(frozen=True)
class Book:
    market_id: str
    yes_bids: list[BookLevel]
    yes_asks: list[BookLevel]
    no_bids: list[BookLevel]
    no_asks: list[BookLevel]
    min_tick_size: float
    min_order_size: int
