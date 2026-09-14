"""add sources json to messages

Revision ID: d2a7c5e91f34
Revises: f1a2b3c4d5e6
"""

from alembic import op
import sqlalchemy as sa


revision = "d2a7c5e91f34"
down_revision = "f1a2b3c4d5e6"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("messages", sa.Column("sources", sa.JSON(), nullable=True))


def downgrade() -> None:
    op.drop_column("messages", "sources")
