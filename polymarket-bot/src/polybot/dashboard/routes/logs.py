"""Tail recent log lines."""
from __future__ import annotations

from collections import deque
from pathlib import Path

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse

from polybot.dashboard.auth import require_token

router = APIRouter(prefix="/logs", dependencies=[Depends(require_token)])

LOG_PATH = Path("logs/polybot.log")
TAIL_LINES = 200


def _tail(path: Path, n: int) -> list[str]:
    if not path.exists():
        return []
    with open(path, encoding="utf-8", errors="replace") as f:
        return list(deque(f, maxlen=n))


@router.get("", response_class=HTMLResponse)
async def logs_page(request: Request) -> HTMLResponse:
    from polybot.dashboard.app import get_templates

    return get_templates().TemplateResponse(
        request,
        "logs.html",
        {"lines": _tail(LOG_PATH, TAIL_LINES)},
    )
