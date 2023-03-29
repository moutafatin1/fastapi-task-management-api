"""init

Revision ID: d2999b58fdd0
Revises: 
Create Date: 2023-03-29 17:24:13.789899

"""
import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "d2999b58fdd0"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("username", sa.String, unique=True, nullable=False),
        sa.Column("password_hash", sa.String, nullable=False),
    )


def downgrade() -> None:
    op.drop_table("users")
