from __future__ import annotations

from pathlib import Path

from polybot.config import RiskConfig
from polybot.risk import check_trade, killswitch_active


def _cfg() -> RiskConfig:
    return RiskConfig(
        max_trade_usdc=5.0,
        daily_loss_limit_usdc=10.0,
        max_concurrent_positions=3,
        max_position_pct_of_balance=0.25,
        min_edge_bps=50,
    )


def test_happy_path():
    result = check_trade(
        trade_usdc=4.0,
        balance_usdc=32.0,
        open_positions=1,
        realized_pnl_today_usdc=0.0,
        edge_bps=80,
        cfg=_cfg(),
    )
    assert result.allowed


def test_rejects_oversized_trade():
    result = check_trade(
        trade_usdc=6.0,
        balance_usdc=100.0,
        open_positions=0,
        realized_pnl_today_usdc=0.0,
        edge_bps=100,
        cfg=_cfg(),
    )
    assert not result.allowed
    assert "exceeds cap" in result.reason


def test_rejects_pct_of_balance():
    result = check_trade(
        trade_usdc=4.0,
        balance_usdc=10.0,
        open_positions=0,
        realized_pnl_today_usdc=0.0,
        edge_bps=100,
        cfg=_cfg(),
    )
    assert not result.allowed
    assert "max_position_pct_of_balance" in result.reason


def test_rejects_at_position_cap():
    result = check_trade(
        trade_usdc=4.0,
        balance_usdc=100.0,
        open_positions=3,
        realized_pnl_today_usdc=0.0,
        edge_bps=100,
        cfg=_cfg(),
    )
    assert not result.allowed


def test_rejects_daily_loss_hit():
    result = check_trade(
        trade_usdc=4.0,
        balance_usdc=100.0,
        open_positions=0,
        realized_pnl_today_usdc=-10.0,
        edge_bps=100,
        cfg=_cfg(),
    )
    assert not result.allowed


def test_rejects_low_edge():
    result = check_trade(
        trade_usdc=4.0,
        balance_usdc=100.0,
        open_positions=0,
        realized_pnl_today_usdc=0.0,
        edge_bps=10,
        cfg=_cfg(),
    )
    assert not result.allowed


def test_killswitch_detects_file(tmp_path: Path):
    sentinel = tmp_path / "STOP"
    assert not killswitch_active(sentinel)
    sentinel.write_text("halt")
    assert killswitch_active(sentinel)
