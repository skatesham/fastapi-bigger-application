"""Create buyers table.

Revision ID: 0002_create_buyers
Revises: 0001_create_users
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "0002_create_buyers"
down_revision: Union[str, Sequence[str], None] = "0001_create_users"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "buyers",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=True),
        sa.Column("phone", sa.String(), nullable=True),
        sa.Column("address_cep", sa.String(), nullable=True),
        sa.Column("address_public_place", sa.String(), nullable=True),
        sa.Column("address_city", sa.String(), nullable=True),
        sa.Column("address_district", sa.String(), nullable=True),
        sa.Column("address_state", sa.String(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_buyers_id"), "buyers", ["id"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_buyers_id"), table_name="buyers")
    op.drop_table("buyers")
