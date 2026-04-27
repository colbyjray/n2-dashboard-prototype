"""Decision feed. Phase 1 wires this to the SQLite decisions table."""
from __future__ import annotations

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse

from polybot.dashboard.auth import require_token

router = APIRouter(prefix="/decisions", dependencies=[Depends(require_token)])


@router.get("", response_class=HTMLResponse)
async def decisions_page(request: Request) -> HTMLResponse:
    from polybot.dashboard.app import get_templates

    return get_templates().TemplateResponse(
        request,
        "decisions.html",
        {"phase": "stub"},
    )
