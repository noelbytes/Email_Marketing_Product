from __future__ import annotations

from flask import Blueprint, abort, g, jsonify, request
from pydantic import ValidationError
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from ..db.models import EmailTemplate
from ..extensions import db
from ..services.email import send_html_email
from ..services.rendering import render_html_document
from .authz import requires_permission
from .schemas import (
    TemplateCreateSchema,
    TemplateSendTestSchema,
    TemplateUpdateSchema,
)

templates_bp = Blueprint("templates", __name__)


def require_identity() -> tuple[int, int]:
    user_id = getattr(g, "current_user_id", None)
    org_id = getattr(g, "current_org_id", None)
    if not user_id or not org_id:
        abort(401, description="User context required")
    return int(user_id), int(org_id)


def serialize_template(template: EmailTemplate) -> dict:
    return {
        "id": template.id,
        "name": template.name,
        "subject": template.subject,
        "html": template.html,
        "css": template.css,
        "project_data": template.project_data,
        "organization_id": template.organization_id,
        "created_by_user_id": template.created_by_user_id,
        "created_at": template.created_at.isoformat(),
        "updated_at": template.updated_at.isoformat(),
    }


@templates_bp.errorhandler(ValidationError)
def handle_validation_error(err: ValidationError):
    return jsonify({"error": {"message": "Validation error", "code": 400, "details": err.errors()}}), 400


@templates_bp.get("")
@requires_permission("templates.manage")
def list_templates():
    _, org_id = require_identity()
    stmt = (
        select(EmailTemplate)
        .where(EmailTemplate.organization_id == org_id)
        .order_by(EmailTemplate.updated_at.desc())
    )
    templates = db.session.execute(stmt).unique().scalars().all()
    return jsonify({"data": [serialize_template(tpl) for tpl in templates]}), 200


@templates_bp.post("")
@requires_permission("templates.manage")
def create_template():
    user_id, org_id = require_identity()
    payload = TemplateCreateSchema.model_validate(request.get_json() or {})
    template = EmailTemplate(
        organization_id=org_id,
        created_by_user_id=user_id,
        name=payload.name,
        subject=payload.subject,
        html=payload.html or "",
        css=payload.css,
        project_data=payload.project_data,
    )
    db.session.add(template)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        abort(409, description="Template name already exists in this workspace")
    return jsonify({"data": serialize_template(template)}), 201


@templates_bp.get("/<int:template_id>")
@requires_permission("templates.manage")
def get_template(template_id: int):
    _, org_id = require_identity()
    template = db.session.get(EmailTemplate, template_id)
    if not template or template.organization_id != org_id:
        abort(404, description="Template not found")
    return jsonify({"data": serialize_template(template)}), 200


@templates_bp.put("/<int:template_id>")
@requires_permission("templates.manage")
def update_template(template_id: int):
    _, org_id = require_identity()
    template = db.session.get(EmailTemplate, template_id)
    if not template or template.organization_id != org_id:
        abort(404, description="Template not found")
    payload = TemplateUpdateSchema.model_validate(request.get_json() or {})

    if payload.name is not None:
        template.name = payload.name
    if payload.subject is not None:
        template.subject = payload.subject
    if payload.html is not None:
        template.html = payload.html
    if payload.css is not None:
        template.css = payload.css
    if payload.project_data is not None:
        template.project_data = payload.project_data

    db.session.add(template)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        abort(409, description="Template name already exists in this workspace")
    return jsonify({"data": serialize_template(template)}), 200


@templates_bp.delete("/<int:template_id>")
@requires_permission("templates.manage")
def delete_template(template_id: int):
    _, org_id = require_identity()
    template = db.session.get(EmailTemplate, template_id)
    if not template or template.organization_id != org_id:
        abort(404, description="Template not found")
    db.session.delete(template)
    db.session.commit()
    return jsonify({"status": "deleted"}), 200


@templates_bp.post("/<int:template_id>/send-test")
@requires_permission("emails.send_test")
def send_test(template_id: int):
    _, org_id = require_identity()
    template = db.session.get(EmailTemplate, template_id)
    if not template or template.organization_id != org_id:
        abort(404, description="Template not found")

    payload = TemplateSendTestSchema.model_validate(request.get_json() or {})
    combined = render_html_document(html=template.html or "", css=template.css)

    subject = payload.subject or template.subject or f"Test email: {template.name}"
    try:
        send_html_email(to_email=payload.to, subject=subject, html=combined)
    except Exception as exc:
        abort(502, description=f"SMTP send failed: {exc}")

    return jsonify({"status": "sent", "to": payload.to}), 200
