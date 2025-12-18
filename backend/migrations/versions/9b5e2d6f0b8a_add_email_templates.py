"""add email templates

Revision ID: 9b5e2d6f0b8a
Revises: 7a1c9f4c4ed4
Create Date: 2025-12-17 23:40:00.000000

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "9b5e2d6f0b8a"
down_revision = "7a1c9f4c4ed4"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "email_templates",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("organization_id", sa.Integer(), nullable=False),
        sa.Column("created_by_user_id", sa.Integer(), nullable=True),
        sa.Column("name", sa.String(length=200), nullable=False),
        sa.Column("subject", sa.String(length=255), nullable=True),
        sa.Column("html", sa.Text(), nullable=False),
        sa.Column("css", sa.Text(), nullable=True),
        sa.Column("project_data", sa.JSON(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["created_by_user_id"], ["users.id"], ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["organization_id"], ["organizations.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("organization_id", "name", name="uq_org_template_name"),
    )


def downgrade():
    op.drop_table("email_templates")

