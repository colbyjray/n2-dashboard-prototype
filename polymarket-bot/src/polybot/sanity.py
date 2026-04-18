"""Claude sanity-check veto layer.

The arb math is mechanical. This layer catches cases where the math looks fine
but the market is obviously broken: resolution already announced, ambiguous
question wording, one side stale, etc. Veto is cheap; missing a flag is not.
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class SanityResult:
    approve: bool
    reasoning: str


def review_trade(
    *,
    api_key: str,
    model: str,
    max_tokens: int,
    market_question: str,
    yes_ask: float,
    no_ask: float,
    edge_bps: int,
    size: int,
) -> SanityResult:
    """Return approve=True only on clear green light from the model.

    Phase 0 ships the interface. The call is implemented in Phase 1 when
    we have real candidates to review.
    """
    raise NotImplementedError("sanity.review_trade is wired up in Phase 1")
