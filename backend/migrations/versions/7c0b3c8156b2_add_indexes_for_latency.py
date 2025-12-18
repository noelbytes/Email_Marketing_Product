"""add indexes for latency

Revision ID: 7c0b3c8156b2
Revises: ed0fbf1d3d91
Create Date: 2025-12-18 06:10:00.000000

"""

from alembic import op


# revision identifiers, used by Alembic.
revision = "7c0b3c8156b2"
down_revision = "ed0fbf1d3d91"
branch_labels = None
depends_on = None


def upgrade():
    op.create_index("ix_contacts_organization_id", "contacts", ["organization_id"])
    op.create_index("ix_email_templates_organization_id", "email_templates", ["organization_id"])
    op.create_index("ix_campaigns_organization_id", "campaigns", ["organization_id"])
    op.create_index("ix_campaigns_template_id", "campaigns", ["template_id"])
    op.create_index("ix_email_sends_organization_id", "email_sends", ["organization_id"])
    op.create_index("ix_email_sends_campaign_id", "email_sends", ["campaign_id"])


def downgrade():
    op.drop_index("ix_email_sends_campaign_id", table_name="email_sends")
    op.drop_index("ix_email_sends_organization_id", table_name="email_sends")
    op.drop_index("ix_campaigns_template_id", table_name="campaigns")
    op.drop_index("ix_campaigns_organization_id", table_name="campaigns")
    op.drop_index("ix_email_templates_organization_id", table_name="email_templates")
    op.drop_index("ix_contacts_organization_id", table_name="contacts")

