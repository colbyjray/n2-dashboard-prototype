"""Fee and rebate math for Polymarket US.

Fee schedule effective 2026-04-03. Fees are symmetric around price $0.50 and
lowest at the extremes. The spec Polymarket publishes uses a coefficient Theta:

    taker_fee_per_contract = Theta_taker * p * (1 - p) * 2

At p=0.50 with Theta=0.05, fee per 100 contracts = 0.05 * 0.25 * 2 * 100 = $1.25.
At p=0.10 with Theta=0.05, fee per 100 contracts = 0.05 * 0.09 * 2 * 100 = $0.90.

The formula below keeps that shape and scales to any notional. Values are
dollars per contract, where one contract pays $1 at resolution.
"""
from __future__ import annotations


def taker_fee_per_contract(price: float, theta_taker: float) -> float:
    if not 0.0 < price < 1.0:
        raise ValueError(f"price must be in (0, 1); got {price}")
    return theta_taker * price * (1.0 - price) * 2.0


def maker_rebate_per_contract(price: float, theta_maker: float) -> float:
    if not 0.0 < price < 1.0:
        raise ValueError(f"price must be in (0, 1); got {price}")
    return theta_maker * price * (1.0 - price) * 2.0


def effective_taker_fee(price: float, theta_taker: float, rebate_fraction: float) -> float:
    """Taker fee net of any active taker rebate promo."""
    if not 0.0 <= rebate_fraction <= 1.0:
        raise ValueError(f"rebate_fraction must be in [0, 1]; got {rebate_fraction}")
    return taker_fee_per_contract(price, theta_taker) * (1.0 - rebate_fraction)
