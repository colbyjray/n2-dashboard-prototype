"""Token auth for the dashboard.

The expected token lives in the OS keychain. After the user lands on
`/?token=...` once, the server sets an HttpOnly cookie that all subsequent
requests carry automatically. Cookie has SameSite=strict so other sites
cannot forge requests to localhost.

For programmatic access (curl, scripts) the token is also accepted in the
`X-Polybot-Token` header or `?token=` query string.

Constant-time comparison guards against timing leaks.
"""
from __future__ import annotations

import hmac

from fastapi import HTTPException, Request, status

from polybot import secrets

COOKIE_NAME = "polybot_session"
COOKIE_MAX_AGE = 60 * 60 * 24 * 30  # 30 days


def expected_token() -> str:
    return secrets.get_or_create_dashboard_token()


def _extract(request: Request) -> str | None:
    cookie = request.cookies.get(COOKIE_NAME)
    if cookie:
        return cookie
    header = request.headers.get("x-polybot-token")
    if header:
        return header
    return request.query_params.get("token")


def is_valid_token(presented: str) -> bool:
    return hmac.compare_digest(presented, expected_token())


async def require_token(request: Request) -> None:
    presented = _extract(request)
    if not presented:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="missing token")
    if not is_valid_token(presented):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid token")
