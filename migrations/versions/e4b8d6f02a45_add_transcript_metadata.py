"""add transcript guest and source url metadata

Revision ID: e4b8d6f02a45
Revises: d2a7c5e91f34
"""

from alembic import op
import sqlalchemy as sa


revision = "e4b8d6f02a45"
down_revision = "d2a7c5e91f34"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("transcripts", sa.Column("guest", sa.String(), nullable=True))
    op.add_column("transcripts", sa.Column("source_url", sa.String(), nullable=True))


def downgrade() -> None:
    op.drop_column("transcripts", "source_url")
    op.drop_column("transcripts", "guest")
