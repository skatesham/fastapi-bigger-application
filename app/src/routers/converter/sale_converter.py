from typing import List

from ...domain.sale import models, schemas
from . import buyer_converter, car_converter, seller_converter


def convert(db_sale: models.Sale):
    """Customized convertion to response template"""
    return schemas.Sale(
        id=db_sale.id,
        car=car_converter.convert(db_sale.car),
        seller=seller_converter.convert(db_sale.seller),
        buyer=buyer_converter.convert(db_sale.buyer),
        created_at=db_sale.created_at,
    )


def convert_many(db_sales: List):
    """Convert list customized"""
    return [convert(db_sale) for db_sale in db_sales]
