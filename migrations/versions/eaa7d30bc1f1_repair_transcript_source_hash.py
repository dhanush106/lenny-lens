"""repair transcript source hash migration

Revision ID: eaa7d30bc1f1
Revises: dbc451de910d
"""

from alembic import op
import sqlalchemy as sa


revision = "eaa7d30bc1f1"
down_revision = "dbc451de910d"
branch_labels = None
depends_on = None


def upgrade() -> None:
    columns = {column["name"] for column in sa.inspect(op.get_bind()).get_columns("transcripts")}
    if "source_hash" not in columns:
        op.add_column("transcripts", sa.Column("source_hash", sa.String(length=64), nullable=True))


def downgrade() -> None:
    columns = {column["name"] for column in sa.inspect(op.get_bind()).get_columns("transcripts")}
    if "source_hash" in columns:
        op.drop_column("transcripts", "source_hash")
