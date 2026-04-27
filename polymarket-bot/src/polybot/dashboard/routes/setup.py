"""Setup page. Paste keys, store in OS keychain, test connection."""
from __future__ import annotations

import logging
from typing import Annotated

from fastapi import APIRouter, Depends, Form, HTTPException, Request
from fastapi.responses import HTMLResponse

from polybot import secrets
from polybot.client import balances, make_client
from polybot.dashboard.auth import require_token

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/setup", dependencies=[Depends(require_token)])


def _redact(value: str | None) -> str:
    if not value:
        return "(not set)"
    if len(value) <= 8:
        return "*" * len(value)
    return f"{value[:4]}...{value[-4:]}"


@router.get("", response_class=HTMLResponse)
async def setup_page(request: Request) -> HTMLResponse:
    from polybot.dashboard.app import get_templates

    creds = secrets.load_credentials()
    return get_templates().TemplateResponse(
        request,
        "setup.html",
        {
            "polymarket_key_id": _redact(creds.polymarket_key_id),
            "polymarket_secret_set": bool(creds.polymarket_secret_key),
            "anthropic_set": bool(creds.anthropic_api_key),
            "polymarket_ready": creds.polymarket_ready,
        },
    )


@router.post("/save", response_class=HTMLResponse)
async def save_keys(
    request: Request,
    polymarket_key_id: Annotated[str, Form()] = "",
    polymarket_secret_key: Annotated[str, Form()] = "",
    anthropic_api_key: Annotated[str, Form()] = "",
) -> HTMLResponse:
    from polybot.dashboard.app import get_templates

    saved: list[str] = []
    errors: list[str] = []

    if polymarket_key_id.strip() and polymarket_secret_key.strip():
        try:
            secrets.store_polymarket(polymarket_key_id, polymarket_secret_key)
            saved.append("Polymarket credentials")
        except Exception as exc:
            errors.append(f"Polymarket: {exc}")
    elif polymarket_key_id.strip() or polymarket_secret_key.strip():
        errors.append("Polymarket key_id and secret_key must both be provided")

    if anthropic_api_key.strip():
        try:
            secrets.store_anthropic(anthropic_api_key)
            saved.append("Anthropic key")
        except Exception as exc:
            errors.append(f"Anthropic: {exc}")

    return get_templates().TemplateResponse(
        request,
        "_setup_save_result.html",
        {"saved": saved, "errors": errors},
    )


@router.post("/test", response_class=HTMLResponse)
async def test_connection(request: Request) -> HTMLResponse:
    from polybot.dashboard.app import get_templates

    creds = secrets.load_credentials()
    if not creds.polymarket_ready:
        raise HTTPException(status_code=400, detail="Polymarket credentials not set")

    try:
        client = make_client(
            key_id=creds.polymarket_key_id or "",
            secret_key=creds.polymarket_secret_key or "",
        )
        bal = balances(client)
        ok = True
        message = f"Connected. Balance payload: {bal!r}"
    except Exception as exc:
        ok = False
        message = f"Connection failed: {exc}"
        logger.exception("connection test failed")

    return get_templates().TemplateResponse(
        request,
        "_setup_test_result.html",
        {"ok": ok, "message": message},
    )


@router.post("/clear-polymarket", response_class=HTMLResponse)
async def clear_polymarket(request: Request) -> HTMLResponse:
    from polybot.dashboard.app import get_templates

    secrets.clear_polymarket()
    return get_templates().TemplateResponse(
        request,
        "_setup_save_result.html",
        {"saved": ["Polymarket credentials cleared"], "errors": []},
    )
