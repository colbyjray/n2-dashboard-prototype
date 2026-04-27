"""Decision feed. Reads from SQLite decisions table written by the scanner."""
from __future__ import annotations

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse

from polybot.dashboard.auth import require_token
from polybot.runtime.scanner import ScannerConfig
from polybot.storage import list_recent_decisions

router = APIRouter(prefix="/decisions", dependencies=[Depends(require_token)])


@router.get("", response_class=HTMLResponse)
async def decisions_page(request: Request) -> HTMLResponse:
    from polybot.dashboard.app import get_templates

    return get_templates().TemplateResponse(request, "decisions.html", {})


@router.get("/data", response_class=HTMLResponse)
async def decisions_data(request: Request) -> HTMLResponse:
    from polybot.dashboard.app import get_templates

    cfg = ScannerConfig()
    rows = list_recent_decisions(cfg.sqlite_path, limit=200)
    return get_templates().TemplateResponse(
        request,
        "_decisions_data.html",
        {"rows": rows},
    )
