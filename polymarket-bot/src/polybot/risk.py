"""Pre-trade risk checks and kill-switch."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from polybot.config import RiskConfig


@dataclass(frozen=True)
class RiskCheck:
    allowed: bool
    reason: str


def killswitch_active(sentinel_path: str | Path) -> bool:
    return Path(sentinel_path).exists()


def check_trade(
    *,
    trade_usdc: float,
    balance_usdc: float,
    open_positions: int,
    realized_pnl_today_usdc: float,
    edge_bps: int,
    cfg: RiskConfig,
) -> RiskCheck:
    if trade_usdc <= 0:
        return RiskCheck(False, "trade size must be positive")
    if trade_usdc > cfg.max_trade_usdc:
        return RiskCheck(False, f"trade size {trade_usdc} exceeds cap {cfg.max_trade_usdc}")
    if trade_usdc > balance_usdc * cfg.max_position_pct_of_balance:
        return RiskCheck(False, "trade exceeds max_position_pct_of_balance")
    if open_positions >= cfg.max_concurrent_positions:
        return RiskCheck(False, f"open positions {open_positions} at cap")
    if realized_pnl_today_usdc <= -cfg.daily_loss_limit_usdc:
        return RiskCheck(False, "daily loss limit hit")
    if edge_bps < cfg.min_edge_bps:
        return RiskCheck(False, f"edge {edge_bps}bps below threshold {cfg.min_edge_bps}bps")
    return RiskCheck(True, "ok")
