"""Load and validate polybot configuration from TOML + .env."""
from __future__ import annotations

import os
import tomllib
from pathlib import Path

from pydantic import BaseModel, Field, field_validator


class ModeConfig(BaseModel):
    dry_run: bool = True
    autonomous: bool = False
    unlock_phrase: str = ""


class RiskConfig(BaseModel):
    max_trade_usdc: float = Field(gt=0)
    daily_loss_limit_usdc: float = Field(gt=0)
    max_concurrent_positions: int = Field(ge=1)
    max_position_pct_of_balance: float = Field(gt=0, le=1.0)
    min_edge_bps: int = Field(ge=0)


class FeesConfig(BaseModel):
    taker_coefficient: float = Field(ge=0)
    maker_rebate_coefficient: float = Field(ge=0)
    taker_rebate_fraction: float = Field(ge=0, le=1.0)


class ScannerConfig(BaseModel):
    top_n_markets: int = Field(ge=1)
    book_depth_levels: int = Field(ge=1)


class StorageConfig(BaseModel):
    sqlite_path: str


class LoggingConfig(BaseModel):
    level: str = "INFO"
    file: str = "logs/polybot.log"


class SanityConfig(BaseModel):
    enabled: bool = True
    model: str = "claude-sonnet-4-6"
    max_tokens: int = Field(ge=1)


class KillSwitchConfig(BaseModel):
    sentinel_path: str = "STOP"


class Secrets(BaseModel):
    polymarket_key_id: str
    polymarket_secret_key: str
    anthropic_api_key: str = ""

    @field_validator("polymarket_key_id", "polymarket_secret_key")
    @classmethod
    def non_empty(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("required credential is empty")
        return v.strip()


class Config(BaseModel):
    mode: ModeConfig
    risk: RiskConfig
    fees: FeesConfig
    scanner: ScannerConfig
    storage: StorageConfig
    logging: LoggingConfig
    sanity: SanityConfig
    killswitch: KillSwitchConfig


def load_config(path: Path | str) -> Config:
    with open(path, "rb") as f:
        raw = tomllib.load(f)
    return Config(**raw)


def load_secrets() -> Secrets:
    return Secrets(
        polymarket_key_id=os.environ.get("POLYMARKET_KEY_ID", ""),
        polymarket_secret_key=os.environ.get("POLYMARKET_SECRET_KEY", ""),
        anthropic_api_key=os.environ.get("ANTHROPIC_API_KEY", ""),
    )
