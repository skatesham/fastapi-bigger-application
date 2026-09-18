"""Seed revision paired with migration 0006_create_sales."""

from datetime import datetime

from sqlalchemy import select
from sqlalchemy.engine import Connection

from app.src.domain.buyer.models import Buyer
from app.src.domain.car.models import Car
from app.src.domain.sale.models import Sale
from app.src.domain.seller.models import Seller


revision = "0006_create_sales"
table_name = "sales"


def seed(connection: Connection) -> None:
    """Create one completed sale relating the seeded records."""
    buyer_id = connection.execute(
        select(Buyer.id).where(Buyer.phone == "11987654321")
    ).scalar_one()
    seller_id = connection.execute(
        select(Seller.id).where(Seller.cpf == "12345678909")
    ).scalar_one()
    car_id = connection.execute(
        select(Car.id).where(
            Car.name == "Civic Touring", Car.year == 2024, Car.brand == "Honda"
        )
    ).scalar_one()

    connection.execute(
        Sale.__table__.insert().values(
            car_id=car_id,
            buyer_id=buyer_id,
            seller_id=seller_id,
            created_at=datetime(2026, 1, 15, 10, 0, 0),
        )
    )
