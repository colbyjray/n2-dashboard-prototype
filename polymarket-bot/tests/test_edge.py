from __future__ import annotations

from polybot.edge import ArbQuote, compute_edge


def test_no_edge_when_prices_sum_to_one():
    q = ArbQuote(
        market_id="m1",
        yes_ask=0.50,
        no_ask=0.50,
        yes_ask_size=100,
        no_ask_size=100,
    )
    result = compute_edge(q, theta_taker=0.05, taker_rebate_fraction=0.0)
    # Prices alone zero out; fees make edge negative.
    assert result.edge_per_pair < 0


def test_positive_edge_when_prices_sum_below_one_minus_fees():
    q = ArbQuote(
        market_id="m1",
        yes_ask=0.45,
        no_ask=0.45,
        yes_ask_size=50,
        no_ask_size=50,
    )
    result = compute_edge(q, theta_taker=0.05, taker_rebate_fraction=0.0)
    assert result.edge_per_pair > 0
    assert result.max_pairs == 50
    assert result.edge_bps > 0


def test_max_pairs_is_min_of_both_sides():
    q = ArbQuote(
        market_id="m1",
        yes_ask=0.40,
        no_ask=0.40,
        yes_ask_size=10,
        no_ask_size=200,
    )
    result = compute_edge(q, theta_taker=0.05, taker_rebate_fraction=0.0)
    assert result.max_pairs == 10


def test_rebate_increases_edge():
    q = ArbQuote(
        market_id="m1",
        yes_ask=0.48,
        no_ask=0.48,
        yes_ask_size=100,
        no_ask_size=100,
    )
    no_rebate = compute_edge(q, theta_taker=0.05, taker_rebate_fraction=0.0)
    with_rebate = compute_edge(q, theta_taker=0.05, taker_rebate_fraction=0.5)
    assert with_rebate.edge_per_pair > no_rebate.edge_per_pair
