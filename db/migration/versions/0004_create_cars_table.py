"""Create cars table.

Revision ID: 0004_create_cars
Revises: 0003_create_sellers
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "0004_create_cars"
down_revision: Union[str, Sequence[str], None] = "0003_create_sellers"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "cars",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=True),
        sa.Column("year", sa.Integer(), nullable=True),
        sa.Column("brand", sa.String(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_cars_brand"), "cars", ["brand"], unique=False)
    op.create_index(op.f("ix_cars_id"), "cars", ["id"], unique=False)
    op.create_index(op.f("ix_cars_name"), "cars", ["name"], unique=False)
    op.create_index(op.f("ix_cars_year"), "cars", ["year"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_cars_year"), table_name="cars")
    op.drop_index(op.f("ix_cars_name"), table_name="cars")
    op.drop_index(op.f("ix_cars_id"), table_name="cars")
    op.drop_index(op.f("ix_cars_brand"), table_name="cars")
    op.drop_table("cars")
