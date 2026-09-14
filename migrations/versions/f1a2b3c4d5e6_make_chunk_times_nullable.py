"""allow unknown transcript timestamps

Revision ID: f1a2b3c4d5e6
Revises: 8f3c1a92d4e0
"""

from alembic import op
import sqlalchemy as sa


revision = "f1a2b3c4d5e6"
down_revision = "8f3c1a92d4e0"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.alter_column("chunks", "start_time", existing_type=sa.Float(), nullable=True)
    op.alter_column("chunks", "end_time", existing_type=sa.Float(), nullable=True)
    op.execute("UPDATE chunks SET start_time = NULL WHERE start_time = 0")


def downgrade() -> None:
    op.execute("UPDATE chunks SET start_time = 0 WHERE start_time IS NULL")
    op.execute("UPDATE chunks SET end_time = 0 WHERE end_time IS NULL")
    op.alter_column("chunks", "start_time", existing_type=sa.Float(), nullable=False)
    op.alter_column("chunks", "end_time", existing_type=sa.Float(), nullable=False)