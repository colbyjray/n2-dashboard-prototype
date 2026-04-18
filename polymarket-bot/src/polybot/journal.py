"""Decision journal writer. Logs every proposed trade with reasoning."""
from __future__ import annotations

import sqlite3
from dataclasses import dataclass
from datetime import datetime, timezone


@dataclass(frozen=True)
class DecisionRecord:
    market_id: str
    market_question: str
    side: str
    price: float
    size: int
    edge_bps: int
    reasoning: str
    sanity_verdict: str
    placed: bool


def write_decision(conn: sqlite3.Connection, record: DecisionRecord) -> int:
    ts = datetime.now(timezone.utc).isoformat()
    cur = conn.execute(
        """
        INSERT INTO decisions
            (ts, market_id, market_question, side, price, size,
             edge_bps, reasoning, sanity_verdict, placed)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            ts,
            record.market_id,
            record.market_question,
            record.side,
            record.price,
            record.size,
            record.edge_bps,
            record.reasoning,
            record.sanity_verdict,
            int(record.placed),
        ),
    )
    conn.commit()
    return int(cur.lastrowid)
