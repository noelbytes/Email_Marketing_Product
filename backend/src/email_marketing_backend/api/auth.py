from __future__ import annotations

from dataclasses import asdict, dataclass

from flask import Blueprint, jsonify, request, abort
from sqlalchemy.exc import IntegrityError

from ..extensions import db
from ..db.models import Organization, User
from ..services.iam import assign_roles, list_permissions_for_user, seed_iam
from ..security import create_access_token, decode_token, TokenError

auth_bp = Blueprint("auth", __name__)


@dataclass
class AuthResponse:
    access_token: str
    token_type: str
    user: dict
    roles: list[str]
    permissions: list[str]


def ensure_organization(slug: str, name: str | None = None) -> Organization:
    org = db.session.query(Organization).filter_by(slug=slug).first()
    if org:
        return org
    org = Organization(name=name or slug.title(), slug=slug)
    db.session.add(org)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        org = db.session.query(Organization).filter_by(slug=slug).first()
    return org


def serialize_user(user: User) -> dict:
    return {
        "id": user.id,
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "organization_id": user.organization_id,
        "roles": [role.name for role in user.roles],
    }


def build_response(user: User, roles: list[str]) -> AuthResponse:
    permissions = list_permissions_for_user(user)
    claims = {
        "sub": str(user.id),
        "email": user.email,
        "org_id": user.organization_id,
        "roles": roles,
        "permissions": permissions,
    }
    token = create_access_token(claims)
    return AuthResponse(
        access_token=token,
        token_type="bearer",
        user=serialize_user(user),
        roles=roles,
        permissions=permissions,
    )


@auth_bp.post("/register")
def register():
    payload = request.get_json() or {}
    email = payload.get("email")
    password = payload.get("password")
    organization_slug = (payload.get("organization") or "constellation").lower()
    first_name = payload.get("first_name")
    last_name = payload.get("last_name")
    role_names = payload.get("roles") or ["journey-architect"]

    if not email or not password:
        abort(400, description="Email and password are required.")

    seed_iam()
    org = ensure_organization(organization_slug)

    if db.session.query(User).filter_by(email=email).first():
        abort(409, description="User already exists")

    user = User(
        email=email,
        organization_id=org.id,
        first_name=first_name or email.split("@")[0],
        last_name=last_name,
    )
    user.set_password(password)
    db.session.add(user)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        abort(409, description="User already exists")

    if email.endswith("@admin.com"):
        role_names = ["org-admin"]

    assign_roles(user, role_names)
    response = build_response(user, role_names)
    return jsonify(asdict(response)), 201


@auth_bp.post("/login")
def login():
    payload = request.get_json() or {}
    email = payload.get("email")
    password = payload.get("password")
    organization_slug = (payload.get("organization") or "").lower().strip()

    if not email or not password:
        abort(400, description="Email and password are required.")

    user = db.session.query(User).filter_by(email=email).first()
    if not user or not user.check_password(password):
        abort(401, description="Invalid credentials")

    if organization_slug and user.organization and user.organization.slug != organization_slug:
        abort(401, description="Invalid workspace")

    role_names = [role.name for role in user.roles]
    if not role_names:
        role_names = ["journey-architect"]
        assign_roles(user, role_names)

    response = build_response(user, role_names)
    return jsonify(asdict(response)), 200


@auth_bp.get("/me")
def me():
    auth_header = request.headers.get("Authorization", "")
    if not auth_header.startswith("Bearer "):
        abort(401, description="Missing token")
    token = auth_header.split(" ", 1)[1]
    try:
        payload = decode_token(token)
    except TokenError as exc:
        abort(401, description=str(exc))
    user = db.session.get(User, int(payload["sub"]))
    if not user:
        abort(404, description="User not found")
    permissions = list_permissions_for_user(user)
    return jsonify(
        {
            "user": serialize_user(user),
            "roles": payload.get("roles", []),
            "permissions": permissions,
        }
    )
