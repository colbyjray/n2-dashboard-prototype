"""Status page. Balance, positions, open orders, dry-run toggle, kill-switch."""
from __future__ import annotations

import logging
from pathlib import Path

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse, PlainTextResponse

from polybot import secrets
from polybot.client import balances, make_client, open_orders, positions
from polybot.dashboard.auth import require_token

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/status", dependencies=[Depends(require_token)])

KILLSWITCH_PATH = Path("STOP")


def _killswitch_active() -> bool:
    return KILLSWITCH_PATH.exists()


@router.get("", response_class=HTMLResponse)
async def status_page(request: Request) -> HTMLResponse:
    from polybot.dashboard.app import get_templates

    creds = secrets.load_credentials()
    return get_templates().TemplateResponse(
        request,
        "status.html",
        {
            "polymarket_ready": creds.polymarket_ready,
            "killswitch_active": _killswitch_active(),
        },
    )


@router.get("/data", response_class=HTMLResponse)
async def status_data(request: Request) -> HTMLResponse:
    from polybot.dashboard.app import get_templates

    creds = secrets.load_credentials()
    if not creds.polymarket_ready:
        return get_templates().TemplateResponse(
            request,
            "_status_data.html",
            {"ready": False, "error": "credentials not set"},
        )

    try:
        client = make_client(
            key_id=creds.polymarket_key_id or "",
            secret_key=creds.polymarket_secret_key or "",
        )
        bal = balances(client)
        pos = positions(client)
        orders = open_orders(client)
        return get_templates().TemplateResponse(
            request,
            "_status_data.html",
            {
                "ready": True,
                "balance": repr(bal),
                "positions": repr(pos) if pos else "(none)",
                "orders": repr(orders) if orders else "(none)",
                "killswitch_active": _killswitch_active(),
            },
        )
    except Exception as exc:
        logger.exception("status fetch failed")
        return get_templates().TemplateResponse(
            request,
            "_status_data.html",
            {"ready": False, "error": str(exc)},
        )


@router.post("/killswitch/engage", response_class=PlainTextResponse)
async def engage_killswitch() -> PlainTextResponse:
    KILLSWITCH_PATH.write_text("halt\n")
    return PlainTextResponse("KILL SWITCH ENGAGED")


@router.post("/killswitch/release", response_class=PlainTextResponse)
async def release_killswitch() -> PlainTextResponse:
    if KILLSWITCH_PATH.exists():
        KILLSWITCH_PATH.unlink()
    return PlainTextResponse("kill switch released")
