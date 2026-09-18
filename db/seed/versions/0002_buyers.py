"""Seed revision paired with migration 0002_create_buyers."""

from sqlalchemy.engine import Connection

from app.src.domain.buyer.models import Buyer


revision = "0002_create_buyers"
table_name = "buyers"


def seed(connection: Connection) -> None:
    """Create a buyer used by the sample sale."""
    connection.execute(
        Buyer.__table__.insert().values(
            name="Marina Costa",
            phone="11987654321",
            address_cep="01310-100",
            address_public_place="Avenida Paulista",
            address_city="São Paulo",
            address_district="Bela Vista",
            address_state="SP",
        )
    )
