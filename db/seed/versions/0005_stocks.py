"""Seed revision paired with migration 0005_create_stocks."""

from sqlalchemy import select
from sqlalchemy.engine import Connection

from app.src.domain.car.models import Car
from app.src.domain.stock.models import Stock


revision = "0005_create_stocks"
table_name = "stocks"


def seed(connection: Connection) -> None:
    """Create inventory records for all sample cars."""
    civic_id = connection.execute(
        select(Car.id).where(
            Car.name == "Civic Touring", Car.year == 2024, Car.brand == "Honda"
        )
    ).scalar_one()
    corolla_id = connection.execute(
        select(Car.id).where(
            Car.name == "Corolla XEi", Car.year == 2023, Car.brand == "Toyota"
        )
    ).scalar_one()
    tcross_id = connection.execute(
        select(Car.id).where(
            Car.name == "T-Cross Highline",
            Car.year == 2024,
            Car.brand == "Volkswagen",
        )
    ).scalar_one()

    connection.execute(
        Stock.__table__.insert(),
        [
            {"car_id": civic_id, "quantity": 2},
            {"car_id": corolla_id, "quantity": 3},
            {"car_id": tcross_id, "quantity": 1},
        ],
    )
