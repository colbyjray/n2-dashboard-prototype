"""FastAPI app factory for the polybot dashboard."""
from __future__ import annotations

import logging
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from polybot.dashboard.routes import decisions, logs, markets, pnl, setup, status

logger = logging.getLogger(__name__)

PKG_DIR = Path(__file__).resolve().parent
TEMPLATES = Jinja2Templates(directory=str(PKG_DIR / "templates"))
STATIC_DIR = PKG_DIR / "static"


def create_app() -> FastAPI:
    app = FastAPI(title="polybot dashboard", docs_url=None, redoc_url=None)
    app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

    app.include_router(setup.router)
    app.include_router(status.router)
    app.include_router(markets.router)
    app.include_router(decisions.router)
    app.include_router(pnl.router)
    app.include_router(logs.router)

    @app.get("/", response_class=HTMLResponse)
    async def root(request: Request) -> HTMLResponse:
        # If a token is provided in the URL, the landing page captures it
        # into localStorage and bounces to /status.
        return TEMPLATES.TemplateResponse(request, "landing.html", {})

    @app.get("/healthz")
    async def healthz() -> dict[str, str]:
        return {"status": "ok"}

    return app


def get_templates() -> Jinja2Templates:
    return TEMPLATES
