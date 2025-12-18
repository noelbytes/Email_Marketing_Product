from __future__ import annotations

from sqlalchemy import ForeignKey, String, Text, UniqueConstraint, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, TimestampMixin


class EmailTemplate(TimestampMixin, Base):
    __tablename__ = "email_templates"
    __table_args__ = (UniqueConstraint("organization_id", "name", name="uq_org_template_name"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    organization_id: Mapped[int] = mapped_column(
        ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False
    )
    created_by_user_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )

    name: Mapped[str] = mapped_column(String(200), nullable=False)
    subject: Mapped[str | None] = mapped_column(String(255), nullable=True)
    html: Mapped[str] = mapped_column(Text, nullable=False, default="")
    css: Mapped[str | None] = mapped_column(Text, nullable=True)
    project_data: Mapped[dict | None] = mapped_column(JSON, nullable=True)

    organization = relationship("Organization", lazy="joined")
    created_by = relationship("User", lazy="joined")
