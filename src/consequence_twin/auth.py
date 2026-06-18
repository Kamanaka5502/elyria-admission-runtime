from __future__ import annotations

import secrets
from typing import Annotated

from fastapi import Header, HTTPException, status

from .settings import get_settings


def require_client_auth(authorization: Annotated[str | None, Header()] = None) -> None:
    settings = get_settings()
    if settings.is_demo_mode:
        return
    if not settings.api_token:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Client mode requires ELYRIA_API_TOKEN to be configured.",
        )
    expected = f"Bearer {settings.api_token}"
    if not authorization or not secrets.compare_digest(authorization, expected):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization required for client mode.",
            headers={"WWW-Authenticate": "Bearer"},
        )
