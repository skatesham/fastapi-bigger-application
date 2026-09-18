"""Create stocks table.

Revision ID: 0005_create_stocks
Revises: 0004_create_cars
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "0005_create_stocks"
down_revision: Union[str, Sequence[str], None] = "0004_create_cars"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "stocks",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("quantity", sa.Integer(), nullable=True),
        sa.Column("car_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(["car_id"], ["cars.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("car_id"),
    )
    op.create_index(op.f("ix_stocks_id"), "stocks", ["id"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_stocks_id"), table_name="stocks")
    op.drop_table("stocks")
