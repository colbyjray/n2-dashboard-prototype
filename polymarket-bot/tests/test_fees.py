from __future__ import annotations

import pytest

from polybot.fees import (
    effective_taker_fee,
    maker_rebate_per_contract,
    taker_fee_per_contract,
)


def test_taker_fee_symmetric_around_half():
    theta = 0.05
    left = taker_fee_per_contract(0.30, theta)
    right = taker_fee_per_contract(0.70, theta)
    assert left == pytest.approx(right)


def test_taker_fee_peaks_at_half():
    theta = 0.05
    at_half = taker_fee_per_contract(0.50, theta)
    at_ten = taker_fee_per_contract(0.10, theta)
    at_ninety = taker_fee_per_contract(0.90, theta)
    assert at_half > at_ten
    assert at_half > at_ninety


def test_taker_fee_spec_value_at_half():
    # Spec: $1.25 per 100 contracts at p=0.50 with Theta=0.05.
    fee_per_contract = taker_fee_per_contract(0.50, 0.05)
    assert fee_per_contract * 100 == pytest.approx(1.25)


def test_rebate_matches_coefficient():
    at_half_taker = taker_fee_per_contract(0.50, 0.05)
    at_half_rebate = maker_rebate_per_contract(0.50, 0.0125)
    assert at_half_rebate == pytest.approx(at_half_taker * 0.25)


def test_effective_taker_fee_applies_rebate():
    gross = taker_fee_per_contract(0.50, 0.05)
    net = effective_taker_fee(0.50, 0.05, 0.50)
    assert net == pytest.approx(gross * 0.5)


def test_fee_rejects_invalid_price():
    with pytest.raises(ValueError):
        taker_fee_per_contract(0.0, 0.05)
    with pytest.raises(ValueError):
        taker_fee_per_contract(1.0, 0.05)


def test_effective_taker_fee_rejects_invalid_rebate():
    with pytest.raises(ValueError):
        effective_taker_fee(0.5, 0.05, -0.1)
    with pytest.raises(ValueError):
        effective_taker_fee(0.5, 0.05, 1.1)
