"""Seed revision paired with migration 0003_create_sellers."""

from sqlalchemy.engine import Connection

from app.src.domain.seller.models import Seller


revision = "0003_create_sellers"
table_name = "sellers"


def seed(connection: Connection) -> None:
    """Create the seller used by the sample sale."""
    connection.execute(
        Seller.__table__.insert().values(
            name="Rafael Mendes",
            cpf="12345678909",
            phone="11976543210",
        )
    )
