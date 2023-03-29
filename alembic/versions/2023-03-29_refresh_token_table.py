"""refresh_token_table

Revision ID: d14ce644faad
Revises: d2999b58fdd0
Create Date: 2023-03-29 17:34:35.092883

"""
import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "d14ce644faad"
down_revision = "d2999b58fdd0"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "refresh_token",
        sa.Column("id", sa.UUID, primary_key=True),
        sa.Column("user_id", sa.Integer, sa.ForeignKey("users.id"), nullable=False),
        sa.Column("refresh_token", sa.String, nullable=False),
        sa.Column("expires_at", sa.DateTime, nullable=False),
        sa.Column("created_at", sa.DateTime, server_default=sa.func.now()),
        sa.Column(
            "updated_at",
            sa.DateTime,
            default=sa.func.now(),
            onupdate=sa.func.now(),
        ),
    )


def downgrade() -> None:
    op.drop_table("refresh_token")
