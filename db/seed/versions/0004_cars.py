"""Seed revision paired with migration 0004_create_cars."""

from sqlalchemy.engine import Connection

from app.src.domain.car.models import Car


revision = "0004_create_cars"
table_name = "cars"


def seed(connection: Connection) -> None:
    """Create cars for the initial stock and sale examples."""
    connection.execute(
        Car.__table__.insert(),
        [
            {"name": "Civic Touring", "year": 2024, "brand": "Honda"},
            {"name": "Corolla XEi", "year": 2023, "brand": "Toyota"},
            {"name": "T-Cross Highline", "year": 2024, "brand": "Volkswagen"},
        ],
    )
