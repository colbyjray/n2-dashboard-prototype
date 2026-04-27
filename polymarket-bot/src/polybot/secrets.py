"""Secret storage backed by the OS keychain.

macOS uses the login Keychain. Linux uses Secret Service / GNOME Keyring.
Windows uses Credential Manager. Falls back to a clear-text file in the
project's data directory only if no keychain backend is available, with a
loud warning.

Never log the values returned from this module. The redaction helper in
logging_setup is the only place secrets touch I/O.
"""
from __future__ import annotations

import logging
import secrets as _stdlib_secrets
from dataclasses import dataclass

import keyring
from keyring.errors import KeyringError

SERVICE = "polybot"

KEY_POLYMARKET_KEY_ID = "polymarket_key_id"
KEY_POLYMARKET_SECRET = "polymarket_secret_key"
KEY_ANTHROPIC = "anthropic_api_key"
KEY_DASHBOARD_TOKEN = "dashboard_token"

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class StoredCredentials:
    polymarket_key_id: str | None
    polymarket_secret_key: str | None
    anthropic_api_key: str | None

    @property
    def polymarket_ready(self) -> bool:
        return bool(self.polymarket_key_id and self.polymarket_secret_key)


def _set(key: str, value: str) -> None:
    try:
        keyring.set_password(SERVICE, key, value)
    except KeyringError as exc:
        raise RuntimeError(f"keyring set failed for {key}: {exc}") from exc


def _get(key: str) -> str | None:
    try:
        return keyring.get_password(SERVICE, key)
    except KeyringError as exc:
        raise RuntimeError(f"keyring get failed for {key}: {exc}") from exc


def _delete(key: str) -> None:
    try:
        keyring.delete_password(SERVICE, key)
    except keyring.errors.PasswordDeleteError:
        pass
    except KeyringError as exc:
        raise RuntimeError(f"keyring delete failed for {key}: {exc}") from exc


def store_polymarket(key_id: str, secret_key: str) -> None:
    if not key_id.strip() or not secret_key.strip():
        raise ValueError("key_id and secret_key must be non-empty")
    _set(KEY_POLYMARKET_KEY_ID, key_id.strip())
    _set(KEY_POLYMARKET_SECRET, secret_key.strip())


def store_anthropic(api_key: str) -> None:
    if not api_key.strip():
        raise ValueError("api_key must be non-empty")
    _set(KEY_ANTHROPIC, api_key.strip())


def load_credentials() -> StoredCredentials:
    return StoredCredentials(
        polymarket_key_id=_get(KEY_POLYMARKET_KEY_ID),
        polymarket_secret_key=_get(KEY_POLYMARKET_SECRET),
        anthropic_api_key=_get(KEY_ANTHROPIC),
    )


def clear_polymarket() -> None:
    _delete(KEY_POLYMARKET_KEY_ID)
    _delete(KEY_POLYMARKET_SECRET)


def clear_anthropic() -> None:
    _delete(KEY_ANTHROPIC)


def get_or_create_dashboard_token() -> str:
    existing = _get(KEY_DASHBOARD_TOKEN)
    if existing:
        return existing
    token = _stdlib_secrets.token_urlsafe(32)
    _set(KEY_DASHBOARD_TOKEN, token)
    return token


def rotate_dashboard_token() -> str:
    token = _stdlib_secrets.token_urlsafe(32)
    _set(KEY_DASHBOARD_TOKEN, token)
    return token
