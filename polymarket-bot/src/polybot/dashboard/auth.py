"""Token auth for the dashboard.

The token lives in the OS keychain. The browser stores it in localStorage
after the user lands on a URL with `?token=...` once. Every request must
present the token in the `X-Polybot-Token` header or as a query string.

We compare with constant-time equality to keep timing attacks out.
"""
from __future__ import annotations

import hmac

from fastapi import HTTPException, Request, status

from polybot import secrets


def expected_token() -> str:
    return secrets.get_or_create_dashboard_token()


def _extract(request: Request) -> str | None:
    header = request.headers.get("x-polybot-token")
    if header:
        return header
    query = request.query_params.get("token")
    return query


async def require_token(request: Request) -> None:
    presented = _extract(request)
    if not presented:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="missing token")
    if not hmac.compare_digest(presented, expected_token()):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid token")
