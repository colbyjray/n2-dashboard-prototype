"""Arb edge calculation.

Intra-market YES/NO arbitrage. Buying one YES and one NO guarantees a $1 payout
at resolution. If the combined cost plus fees is under $1, the difference is
realized profit per pair.

Edge per pair = 1.0 - yes_ask - no_ask - taker_fee(yes_ask) - taker_fee(no_ask)
"""
from __future__ import annotations

from dataclasses import dataclass

from polybot.fees import effective_taker_fee


@dataclass(frozen=True)
class ArbQuote:
    market_id: str
    yes_ask: float
    no_ask: float
    yes_ask_size: int
    no_ask_size: int


@dataclass(frozen=True)
class ArbEdge:
    market_id: str
    edge_per_pair: float
    edge_bps: int
    max_pairs: int
    notional_usdc: float


def compute_edge(
    quote: ArbQuote,
    theta_taker: float,
    taker_rebate_fraction: float,
) -> ArbEdge:
    yes_fee = effective_taker_fee(quote.yes_ask, theta_taker, taker_rebate_fraction)
    no_fee = effective_taker_fee(quote.no_ask, theta_taker, taker_rebate_fraction)
    edge = 1.0 - quote.yes_ask - quote.no_ask - yes_fee - no_fee
    max_pairs = min(quote.yes_ask_size, quote.no_ask_size)
    notional = (quote.yes_ask + quote.no_ask) * max_pairs
    edge_bps = int(round(edge * 10_000))
    return ArbEdge(
        market_id=quote.market_id,
        edge_per_pair=edge,
        edge_bps=edge_bps,
        max_pairs=max_pairs,
        notional_usdc=notional,
    )
