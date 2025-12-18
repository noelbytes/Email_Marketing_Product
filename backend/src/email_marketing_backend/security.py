from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Any

import jwt
from flask import current_app


class TokenError(Exception):
    pass


def create_access_token(claims: dict[str, Any], expires_delta: timedelta | None = None) -> str:
    expires_delta = expires_delta or timedelta(
        minutes=current_app.config.get("TOKEN_TTL_MINUTES", 60)
    )
    now = datetime.now(tz=timezone.utc)
    payload = {
        **claims,
        "iat": now,
        "exp": now + expires_delta,
    }
    secret = current_app.config["SECRET_KEY"]
    return jwt.encode(payload, secret, algorithm="HS256")


def decode_token(token: str) -> dict[str, Any]:
    try:
        return jwt.decode(
            token,
            current_app.config["SECRET_KEY"],
            algorithms=["HS256"],
            options={"require": ["exp", "iat"]},
        )
    except jwt.PyJWTError as exc:
        raise TokenError(str(exc)) from exc
