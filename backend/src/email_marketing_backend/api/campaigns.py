from __future__ import annotations

from flask import Blueprint, abort, g, jsonify, request
from pydantic import ValidationError
from sqlalchemy import select, func

from ..db.models import Campaign, Contact, EmailSend, EmailTemplate
from ..extensions import db
from ..tasks.campaigns import send_campaign_task
from .authz import requires_permission
from .schemas import CampaignCreateSchema

campaigns_bp = Blueprint("campaigns", __name__)


def require_identity() -> tuple[int, int]:
    user_id = getattr(g, "current_user_id", None)
    org_id = getattr(g, "current_org_id", None)
    if not user_id or not org_id:
        abort(401, description="User context required")
    return int(user_id), int(org_id)


def serialize_campaign(campaign: Campaign) -> dict:
    return {
        "id": campaign.id,
        "name": campaign.name,
        "status": campaign.status,
        "template_id": campaign.template_id,
        "subject": campaign.subject,
        "from_email": campaign.from_email,
        "reply_to": campaign.reply_to,
        "audience_type": campaign.audience_type,
        "recipients": campaign.recipients,
        "notes": campaign.notes,
        "organization_id": campaign.organization_id,
        "created_by_user_id": campaign.created_by_user_id,
        "created_at": campaign.created_at.isoformat(),
        "updated_at": campaign.updated_at.isoformat(),
    }


def serialize_send(send: EmailSend) -> dict:
    return {
        "id": send.id,
        "campaign_id": send.campaign_id,
        "to_email": send.to_email,
        "status": send.status,
        "error": send.error,
        "created_at": send.created_at.isoformat(),
        "updated_at": send.updated_at.isoformat(),
    }


@campaigns_bp.errorhandler(ValidationError)
def handle_validation_error(err: ValidationError):
    return jsonify({"error": {"message": "Validation error", "code": 400, "details": err.errors()}}), 400


@campaigns_bp.get("")
@requires_permission("campaigns.manage")
def list_campaigns():
    _, org_id = require_identity()
    items = db.session.execute(
        select(Campaign)
        .where(Campaign.organization_id == org_id)
        .order_by(Campaign.updated_at.desc())
    ).unique().scalars().all()
    return jsonify({"data": [serialize_campaign(item) for item in items]}), 200


@campaigns_bp.post("")
@requires_permission("campaigns.manage")
def create_campaign():
    user_id, org_id = require_identity()
    payload = CampaignCreateSchema.model_validate(request.get_json() or {})

    template = db.session.get(EmailTemplate, payload.template_id)
    if not template or template.organization_id != org_id:
        abort(404, description="Template not found")

    if payload.audience_type not in ("all_contacts", "custom"):
        abort(400, description="audience_type must be one of: all_contacts, custom")
    if payload.audience_type == "custom" and not payload.recipients:
        abort(400, description="recipients is required for custom audience_type")

    campaign = Campaign(
        organization_id=org_id,
        created_by_user_id=user_id,
        name=payload.name,
        template_id=payload.template_id,
        subject=payload.subject,
        from_email=str(payload.from_email) if payload.from_email else None,
        reply_to=str(payload.reply_to) if payload.reply_to else None,
        audience_type=payload.audience_type,
        recipients=[str(addr) for addr in payload.recipients] if payload.recipients else None,
        notes=payload.notes,
        status="draft",
    )
    db.session.add(campaign)
    db.session.commit()
    return jsonify({"data": serialize_campaign(campaign)}), 201


@campaigns_bp.get("/<int:campaign_id>")
@requires_permission("campaigns.manage")
def get_campaign(campaign_id: int):
    _, org_id = require_identity()
    campaign = db.session.get(Campaign, campaign_id)
    if not campaign or campaign.organization_id != org_id:
        abort(404, description="Campaign not found")
    return jsonify({"data": serialize_campaign(campaign)}), 200


@campaigns_bp.post("/<int:campaign_id>/send")
@requires_permission("campaigns.send")
def send_campaign(campaign_id: int):
    _, org_id = require_identity()
    campaign = db.session.get(Campaign, campaign_id)
    if not campaign or campaign.organization_id != org_id:
        abort(404, description="Campaign not found")
    if campaign.status in ("sending", "sent"):
        abort(409, description=f"Campaign is already {campaign.status}")

    if campaign.audience_type == "all_contacts":
        count = db.session.scalar(
            select(func.count()).select_from(Contact).where(Contact.organization_id == org_id)
        )
        if not count:
            abort(400, description="No contacts found for this workspace")
    if campaign.audience_type == "custom" and not (campaign.recipients or []):
        abort(400, description="No recipients set for custom campaign")

    campaign.status = "sending"
    db.session.add(campaign)
    db.session.commit()

    async_result = send_campaign_task.delay(campaign.id)
    return jsonify({"status": "queued", "task_id": async_result.id, "campaign_id": campaign.id}), 202


@campaigns_bp.get("/<int:campaign_id>/sends")
@requires_permission("campaigns.manage")
def list_campaign_sends(campaign_id: int):
    _, org_id = require_identity()
    campaign = db.session.get(Campaign, campaign_id)
    if not campaign or campaign.organization_id != org_id:
        abort(404, description="Campaign not found")
    sends = db.session.execute(
        select(EmailSend)
        .where(EmailSend.campaign_id == campaign.id)
        .order_by(EmailSend.created_at.desc())
        .limit(200)
    ).unique().scalars().all()
    return jsonify({"data": [serialize_send(item) for item in sends]}), 200
