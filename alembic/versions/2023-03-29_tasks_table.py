"""tasks table

Revision ID: c6893ab37f84
Revises: d14ce644faad
Create Date: 2023-03-29 17:47:07.331862

"""
import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "c6893ab37f84"
down_revision = "d14ce644faad"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "tasks",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("body", sa.String, nullable=False),
        sa.Column("completed", sa.Boolean, nullable=False, default=False),
        sa.Column("user_id", sa.Integer, sa.ForeignKey("users.id"), nullable=False),
    )


def downgrade() -> None:
    op.drop_table("tasks")
