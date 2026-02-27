from typing import List

from app.src.domain.stock import models, schemas


def convert(db_stock: models.Stock):
    """Customized conversion to response template"""
    return schemas.Stock(
        id=db_stock.id,
        car_id=db_stock.car_id,
        quantity=db_stock.quantity,
        created_at=db_stock.created_at,
        updated_at=db_stock.updated_at,
    )


def convert_many(db_stocks: List):
    """Convert list customized"""
    return [convert(db_stock) for db_stock in db_stocks]
