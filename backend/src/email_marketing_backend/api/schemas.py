from __future__ import annotations

from pydantic import BaseModel, EmailStr


class OrganizationCreateSchema(BaseModel):
    name: str
    slug: str


class ContactCreateSchema(BaseModel):
    email: EmailStr
    first_name: str | None = None
    last_name: str | None = None


class TemplateCreateSchema(BaseModel):
    name: str
    subject: str | None = None
    html: str | None = None
    css: str | None = None
    project_data: dict | None = None


class TemplateUpdateSchema(BaseModel):
    name: str | None = None
    subject: str | None = None
    html: str | None = None
    css: str | None = None
    project_data: dict | None = None


class TemplateSendTestSchema(BaseModel):
    to: EmailStr
    subject: str | None = None


class CampaignCreateSchema(BaseModel):
    name: str
    template_id: int
    subject: str | None = None
    from_email: EmailStr | None = None
    reply_to: EmailStr | None = None
    audience_type: str = "all_contacts"
    recipients: list[EmailStr] | None = None
    notes: str | None = None


class CampaignSendSchema(BaseModel):
    send: bool = True
