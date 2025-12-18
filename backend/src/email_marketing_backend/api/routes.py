from __future__ import annotations

from datetime import datetime, timezone

from flask import Blueprint, current_app, jsonify, request, abort, g
from pydantic import ValidationError
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from ..extensions import db
from ..db.models import Organization, Contact
from .schemas import OrganizationCreateSchema, ContactCreateSchema
from .authz import requires_internal, requires_permission

api_bp = Blueprint("api", __name__)


def serialize_organization(org: Organization) -> dict[str, str]:
    return {
        "id": org.id,
        "name": org.name,
        "slug": org.slug,
        "created_at": org.created_at.isoformat(),
    }


def serialize_contact(contact: Contact) -> dict[str, str]:
    return {
        "id": contact.id,
        "email": contact.email,
        "first_name": contact.first_name,
        "last_name": contact.last_name,
        "organization_id": contact.organization_id,
        "created_at": contact.created_at.isoformat(),
    }


@api_bp.errorhandler(ValidationError)
def handle_validation_error(err: ValidationError):
    return jsonify({"error": {"message": "Validation error", "code": 400, "details": err.errors()}}), 400


@api_bp.get("/healthz")
def api_health() -> tuple[dict[str, str], int]:
    payload = {
        "status": "ok",
        "service": "email-marketing-api",
        "version": current_app.config.get("API_VERSION", "0.1.0"),
        "timestamp": datetime.now(tz=timezone.utc).isoformat(),
    }
    return jsonify(payload), 200


@api_bp.get("/organizations")
@requires_internal
def list_organizations():
    organizations = db.session.scalars(select(Organization)).all()
    return jsonify({"data": [serialize_organization(org) for org in organizations]})


@api_bp.post("/organizations")
@requires_internal
def create_organization():
    payload = OrganizationCreateSchema.model_validate(request.get_json() or {})
    org = Organization(name=payload.name, slug=payload.slug)
    db.session.add(org)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        abort(409, description="Organization with that name or slug already exists")
    return jsonify({"data": serialize_organization(org)}), 201


@api_bp.get("/organizations/<int:org_id>/contacts")
@requires_permission("journeys.build")
def list_contacts(org_id: int):
    if getattr(g, "auth_mode", None) != "api_key":
        current_org_id = getattr(g, "current_org_id", None)
        if current_org_id is not None and int(current_org_id) != org_id:
            abort(403, description="Cross-workspace access denied")
    organization = db.session.get(Organization, org_id)
    if not organization:
        abort(404, description="Organization not found")
    contacts = db.session.scalars(
        select(Contact).where(Contact.organization_id == organization.id)
    ).all()
    return jsonify({"data": [serialize_contact(contact) for contact in contacts]})


@api_bp.post("/organizations/<int:org_id>/contacts")
@requires_permission("journeys.build")
def create_contact(org_id: int):
    if getattr(g, "auth_mode", None) != "api_key":
        current_org_id = getattr(g, "current_org_id", None)
        if current_org_id is not None and int(current_org_id) != org_id:
            abort(403, description="Cross-workspace access denied")
    organization = db.session.get(Organization, org_id)
    if not organization:
        abort(404, description="Organization not found")
    payload = ContactCreateSchema.model_validate(request.get_json() or {})
    contact = Contact(
        email=payload.email,
        first_name=payload.first_name,
        last_name=payload.last_name,
        organization_id=organization.id,
    )
    db.session.add(contact)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        abort(409, description="Contact with that email already exists for this organization")
    return jsonify({"data": serialize_contact(contact)}), 201
