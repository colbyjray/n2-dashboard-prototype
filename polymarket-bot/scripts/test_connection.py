"""Phase 0 connection test.

Reads credentials from .env, authenticates to Polymarket US, prints account
balance, open positions, and open orders. No trading logic. No side effects
on the account.

Run:
    python scripts/test_connection.py
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))


def _die(msg: str, code: int = 1) -> None:
    print(f"ERROR: {msg}", file=sys.stderr)
    sys.exit(code)


def main() -> int:
    load_dotenv(ROOT / ".env")

    key_id = os.environ.get("POLYMARKET_KEY_ID", "").strip()
    secret_key = os.environ.get("POLYMARKET_SECRET_KEY", "").strip()
    if not key_id or not secret_key:
        _die(
            "POLYMARKET_KEY_ID and POLYMARKET_SECRET_KEY must be set in .env. "
            "Generate them at https://polymarket.us/developer."
        )

    try:
        from polybot.client import balances, make_client, open_orders, positions
    except ImportError as exc:
        _die(f"import failed: {exc}. Did you run `pip install -r requirements.txt`?")
        return 1

    print("Authenticating to Polymarket US...")
    try:
        client = make_client(key_id=key_id, secret_key=secret_key)
    except Exception as exc:
        _die(f"client construction failed: {exc}")
        return 1

    print("\n--- Account balance ---")
    try:
        bal = balances(client)
        print(bal)
    except Exception as exc:
        _die(f"balances() failed: {exc}")
        return 1

    print("\n--- Open positions ---")
    try:
        pos = positions(client)
        if not pos:
            print("(none)")
        else:
            print(pos)
    except Exception as exc:
        _die(f"positions() failed: {exc}")
        return 1

    print("\n--- Open orders ---")
    try:
        orders = open_orders(client)
        if not orders:
            print("(none)")
        else:
            print(orders)
    except Exception as exc:
        _die(f"orders.list() failed: {exc}")
        return 1

    print("\nOK. Connection verified. No trades placed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
