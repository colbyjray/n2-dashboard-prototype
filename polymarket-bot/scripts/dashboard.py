"""Launch the polybot dashboard.

Binds to 127.0.0.1 only. Prints a click-through URL with the auth token on
first launch (and every launch, for convenience). The token is stored in
your OS keychain and reused across launches.

Usage:
    python scripts/dashboard.py
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

import uvicorn  # noqa: E402

from polybot import secrets  # noqa: E402
from polybot.dashboard.app import create_app  # noqa: E402

HOST = "127.0.0.1"
PORT = 8765


def main() -> int:
    token = secrets.get_or_create_dashboard_token()
    url = f"http://{HOST}:{PORT}/?token={token}"

    print()
    print("polybot dashboard")
    print("-" * 60)
    print("  Open this URL in your browser (one click only):")
    print(f"    {url}")
    print()
    print("  After the first visit, the token is saved in your browser.")
    print("  You can then use http://127.0.0.1:8765 directly.")
    print()
    print("  To rotate the token, delete `polybot/dashboard_token` from")
    print("  your keychain and relaunch.")
    print("-" * 60)
    print()

    app = create_app()
    uvicorn.run(app, host=HOST, port=PORT, log_level="info", access_log=False)
    return 0


if __name__ == "__main__":
    sys.exit(main())
