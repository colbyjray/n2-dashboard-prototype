"""Markets watched. Live data from the in-memory scanner state."""
from __future__ import annotations

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse, PlainTextResponse

from polybot.dashboard.auth import require_token
from polybot.runtime.scanner import ScannerConfig, get_or_create_scanner
from polybot.runtime.state import SHARED

router = APIRouter(prefix="/markets", dependencies=[Depends(require_token)])


@router.get("", response_class=HTMLResponse)
async def markets_page(request: Request) -> HTMLResponse:
    from polybot.dashboard.app import get_templates

    return get_templates().TemplateResponse(request, "markets.html", {})


@router.get("/data", response_class=HTMLResponse)
async def markets_data(request: Request) -> HTMLResponse:
    from polybot.dashboard.app import get_templates

    status, quotes = await SHARED.snapshot()
    best = quotes[0] if quotes else None
    return get_templates().TemplateResponse(
        request,
        "_markets_data.html",
        {"status": status, "quotes": quotes, "best": best},
    )


@router.post("/scanner/start", response_class=PlainTextResponse)
async def scanner_start() -> PlainTextResponse:
    scanner = get_or_create_scanner(ScannerConfig())
    await scanner.start()
    return PlainTextResponse("scanner: starting")


@router.post("/scanner/stop", response_class=PlainTextResponse)
async def scanner_stop() -> PlainTextResponse:
    scanner = get_or_create_scanner(ScannerConfig())
    await scanner.stop()
    return PlainTextResponse("scanner: stopped")
