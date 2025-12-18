from __future__ import annotations

from functools import wraps

from flask import abort, current_app, g, request

from ..security import decode_token, TokenError


def authenticate_request() -> None:
    allowed_keys = current_app.config.get("API_KEYS", [])
    provided_key = request.headers.get("X-API-Key")
    if provided_key and provided_key in allowed_keys:
        g.auth_mode = "api_key"
        g.jwt_payload = {"permissions": ["*"], "roles": ["internal"]}
        g.current_user = None
        g.current_user_id = None
        g.current_org_id = None
        g.current_email = None
        return

    auth_header = request.headers.get("Authorization", "")
    if auth_header.startswith("Bearer "):
        token = auth_header.split(" ", 1)[1]
        try:
            payload = decode_token(token)
        except TokenError as exc:
            abort(401, description=str(exc))
        g.auth_mode = "bearer"
        g.jwt_payload = payload
        g.current_user = None
        g.current_user_id = int(payload["sub"]) if payload.get("sub") else None
        g.current_org_id = payload.get("org_id")
        g.current_email = payload.get("email")
        return

    abort(401, description="Missing or invalid credentials")


def requires_permission(permission: str):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            payload = getattr(g, "jwt_payload", None)
            if not payload:
                abort(401, description="Missing authentication context")
            permissions = payload.get("permissions", [])
            if "*" in permissions or permission in permissions:
                return fn(*args, **kwargs)
            abort(403, description="Insufficient permissions")

        return wrapper

    return decorator


def requires_internal(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if getattr(g, "auth_mode", None) != "api_key":
            abort(403, description="Internal credentials required")
        return fn(*args, **kwargs)

    return wrapper
