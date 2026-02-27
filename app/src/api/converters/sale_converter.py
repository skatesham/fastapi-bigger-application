from typing import List

from app.src.domain.sale import models, schemas


def convert(db_sale: models.Sale):
    """Customized conversion to response template"""
    return schemas.Sale(
        id=db_sale.id,
        car_id=db_sale.car_id,
        buyer_id=db_sale.buyer_id,
        seller_id=db_sale.seller_id,
        price=db_sale.price,
        created_at=db_sale.created_at,
        updated_at=db_sale.updated_at,
    )


def convert_many(db_sales: List):
    """Convert list customized"""
    return [convert(db_sale) for db_sale in db_sales]
