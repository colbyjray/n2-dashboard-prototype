"""FastAPI app factory for the polybot dashboard."""
from __future__ import annotations

import logging
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse, Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from polybot.dashboard.auth import COOKIE_MAX_AGE, COOKIE_NAME, is_valid_token
from polybot.dashboard.routes import decisions, history, logs, markets, pnl, setup, status
from polybot.runtime.scanner import ScannerConfig, get_or_create_scanner

logger = logging.getLogger(__name__)

PKG_DIR = Path(__file__).resolve().parent
TEMPLATES = Jinja2Templates(directory=str(PKG_DIR / "templates"))
STATIC_DIR = PKG_DIR / "static"


@asynccontextmanager
async def _lifespan(app: FastAPI) -> AsyncIterator[None]:
    scanner = get_or_create_scanner(ScannerConfig())
    await scanner.start()
    try:
        yield
    finally:
        await scanner.stop()


def create_app() -> FastAPI:
    app = FastAPI(
        title="polybot dashboard",
        docs_url=None,
        redoc_url=None,
        lifespan=_lifespan,
    )
    app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

    app.include_router(setup.router)
    app.include_router(status.router)
    app.include_router(history.router)
    app.include_router(markets.router)
    app.include_router(decisions.router)
    app.include_router(pnl.router)
    app.include_router(logs.router)

    @app.get("/")
    async def root(request: Request) -> Response:
        # If the user has a valid cookie, send them to /status.
        cookie = request.cookies.get(COOKIE_NAME)
        if cookie and is_valid_token(cookie):
            return RedirectResponse(url="/status", status_code=303)

        # If a valid token is in the query, set the cookie and redirect.
        token = request.query_params.get("token")
        if token and is_valid_token(token):
            response = RedirectResponse(url="/status", status_code=303)
            response.set_cookie(
                key=COOKIE_NAME,
                value=token,
                max_age=COOKIE_MAX_AGE,
                httponly=True,
                samesite="strict",
                secure=False,  # 127.0.0.1 only, http is fine
                path="/",
            )
            return response

        # Otherwise show the landing page.
        return TEMPLATES.TemplateResponse(
            request,
            "landing.html",
            {"bad_token": bool(token)},
        )

    @app.post("/logout")
    async def logout() -> Response:
        response = RedirectResponse(url="/", status_code=303)
        response.delete_cookie(COOKIE_NAME, path="/")
        return response

    @app.get("/healthz")
    async def healthz() -> dict[str, str]:
        return {"status": "ok"}

    return app


def get_templates() -> Jinja2Templates:
    return TEMPLATES
