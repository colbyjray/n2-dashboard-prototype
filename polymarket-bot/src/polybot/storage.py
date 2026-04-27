"""SQLite schema and helpers. Phase 0 ships the schema only."""
from __future__ import annotations

import sqlite3
from pathlib import Path

SCHEMA = """
CREATE TABLE IF NOT EXISTS decisions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ts TEXT NOT NULL,
    market_id TEXT NOT NULL,
    market_question TEXT,
    side TEXT,
    price REAL,
    size INTEGER,
    edge_bps INTEGER,
    reasoning TEXT,
    sanity_verdict TEXT,
    placed INTEGER NOT NULL DEFAULT 0,
    outcome TEXT
);

CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ts TEXT NOT NULL,
    decision_id INTEGER,
    polymarket_order_id TEXT,
    market_id TEXT NOT NULL,
    side TEXT NOT NULL,
    price REAL NOT NULL,
    size INTEGER NOT NULL,
    status TEXT NOT NULL,
    FOREIGN KEY (decision_id) REFERENCES decisions(id)
);

CREATE TABLE IF NOT EXISTS fills (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ts TEXT NOT NULL,
    polymarket_order_id TEXT,
    market_id TEXT NOT NULL,
    side TEXT NOT NULL,
    price REAL NOT NULL,
    size INTEGER NOT NULL,
    fee REAL
);

CREATE INDEX IF NOT EXISTS idx_decisions_ts ON decisions(ts);
CREATE INDEX IF NOT EXISTS idx_orders_ts ON orders(ts);
CREATE INDEX IF NOT EXISTS idx_fills_ts ON fills(ts);
"""


def connect(path: str | Path) -> sqlite3.Connection:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(p)
    conn.row_factory = sqlite3.Row
    return conn


def init_db(path: str | Path) -> None:
    conn = connect(path)
    try:
        conn.executescript(SCHEMA)
        conn.commit()
    finally:
        conn.close()


def list_recent_decisions(path: str | Path, limit: int = 200) -> list[sqlite3.Row]:
    if not Path(path).exists():
        return []
    conn = connect(path)
    try:
        rows = conn.execute(
            "SELECT * FROM decisions ORDER BY id DESC LIMIT ?", (limit,)
        ).fetchall()
        return list(rows)
    finally:
        conn.close()
