"""add lexical search index for transcript chunks

Revision ID: caed09b67db2
Revises: eaa7d30bc1f1
"""

from alembic import op


revision = "caed09b67db2"
down_revision = "eaa7d30bc1f1"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_chunks_text_search "
        "ON chunks USING gin (to_tsvector('english', text))"
    )


def downgrade() -> None:
    op.execute("DROP INDEX IF EXISTS ix_chunks_text_search")
