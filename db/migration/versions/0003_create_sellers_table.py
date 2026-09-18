"""Create sellers table.

Revision ID: 0003_create_sellers
Revises: 0002_create_buyers
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "0003_create_sellers"
down_revision: Union[str, Sequence[str], None] = "0002_create_buyers"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "sellers",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=True),
        sa.Column("cpf", sa.String(), nullable=True),
        sa.Column("phone", sa.String(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_sellers_cpf"), "sellers", ["cpf"], unique=False)
    op.create_index(op.f("ix_sellers_id"), "sellers", ["id"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_sellers_id"), table_name="sellers")
    op.drop_index(op.f("ix_sellers_cpf"), table_name="sellers")
    op.drop_table("sellers")
