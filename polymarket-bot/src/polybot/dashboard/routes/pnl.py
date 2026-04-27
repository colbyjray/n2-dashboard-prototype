"""P&L page. Phase 2 wires this to fills + position values."""
from __future__ import annotations

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse

from polybot.dashboard.auth import require_token

router = APIRouter(prefix="/pnl", dependencies=[Depends(require_token)])


@router.get("", response_class=HTMLResponse)
async def pnl_page(request: Request) -> HTMLResponse:
    from polybot.dashboard.app import get_templates

    return get_templates().TemplateResponse(
        request,
        "pnl.html",
        {"phase": "stub"},
    )
