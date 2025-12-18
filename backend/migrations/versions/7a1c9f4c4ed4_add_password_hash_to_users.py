"""add password hash to users

Revision ID: 7a1c9f4c4ed4
Revises: 75d5046fe71f
Create Date: 2025-12-17 18:12:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7a1c9f4c4ed4'
down_revision = '75d5046fe71f'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('users', sa.Column('password_hash', sa.String(), nullable=True))


def downgrade():
    op.drop_column('users', 'password_hash')
