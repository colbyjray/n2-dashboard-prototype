"""Markets watched page. Phase 1 wires this to the live scanner."""
from __future__ import annotations

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse

from polybot.dashboard.auth import require_token

router = APIRouter(prefix="/markets", dependencies=[Depends(require_token)])


@router.get("", response_class=HTMLResponse)
async def markets_page(request: Request) -> HTMLResponse:
    from polybot.dashboard.app import get_templates

    return get_templates().TemplateResponse(
        request,
        "markets.html",
        {"phase": "stub"},
    )
