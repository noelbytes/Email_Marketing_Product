from __future__ import annotations

from celery import shared_task
from sqlalchemy import select

from ..db.models import Campaign, Contact, EmailSend, EmailTemplate
from ..extensions import db
from ..services.email import send_html_email
from ..services.rendering import render_html_document


def _compose_html(*, template: EmailTemplate) -> str:
    return render_html_document(html=template.html or "", css=template.css)


@shared_task(name="tasks.send_campaign")
def send_campaign_task(campaign_id: int) -> dict:
    return send_campaign(campaign_id)


def send_campaign(campaign_id: int) -> dict:
    campaign = db.session.get(Campaign, campaign_id)
    if not campaign:
        return {"status": "missing", "campaign_id": campaign_id}

    template = db.session.get(EmailTemplate, campaign.template_id)
    if not template:
        campaign.status = "failed"
        db.session.add(campaign)
        db.session.commit()
        return {"status": "failed", "campaign_id": campaign_id, "error": "template missing"}

    recipients: list[str]
    if campaign.audience_type == "custom":
        recipients = list(campaign.recipients or [])
    else:
        recipients = db.session.scalars(
            select(Contact.email).where(Contact.organization_id == campaign.organization_id)
        ).all()

    if not recipients:
        campaign.status = "failed"
        db.session.add(campaign)
        db.session.commit()
        return {"status": "failed", "campaign_id": campaign_id, "error": "no recipients"}

    subject = campaign.subject or template.subject or campaign.name
    html = _compose_html(template=template)

    failures = 0
    for to_email in recipients:
        send_row = EmailSend(
            organization_id=campaign.organization_id,
            campaign_id=campaign.id,
            to_email=to_email,
            status="queued",
        )
        db.session.add(send_row)
        db.session.commit()

        try:
            send_html_email(to_email=to_email, subject=subject, html=html)
            send_row.status = "sent"
            send_row.error = None
        except Exception as exc:
            failures += 1
            send_row.status = "failed"
            send_row.error = str(exc)
        db.session.add(send_row)
        db.session.commit()

    if failures == 0:
        campaign.status = "sent"
    elif failures == len(recipients):
        campaign.status = "failed"
    else:
        campaign.status = "partial"

    db.session.add(campaign)
    db.session.commit()

    return {"status": campaign.status, "campaign_id": campaign_id, "recipients": len(recipients), "failures": failures}
