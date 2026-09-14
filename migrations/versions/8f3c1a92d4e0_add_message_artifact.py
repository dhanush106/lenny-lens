"""add artifact json to messages

Revision ID: 8f3c1a92d4e0
Revises: caed09b67db2
"""

from alembic import op
import sqlalchemy as sa


revision = "8f3c1a92d4e0"
down_revision = "caed09b67db2"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("messages", sa.Column("artifact", sa.JSON(), nullable=True))


def downgrade() -> None:
    op.drop_column("messages", "artifact")
