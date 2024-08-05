from typing import List

from . import buyer_converter
from . import car_converter
from . import seller_converter
from ...domain.sale import schemas, models


def convert(db_sale: models.Sale):
    ''' Customized convertion to response template '''
    return schemas.Sale(
        id=db_sale.id,
        car=car_converter.convert(db_sale.car),
        seller=seller_converter.convert(db_sale.seller),
        buyer=buyer_converter.convert(db_sale.buyer),
        created_at=db_sale.created_at
    )


def convert_many(db_sales: List):
    ''' Convert list customized '''
    return [convert(db_sale) for db_sale in db_sales]
