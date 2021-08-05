from typing import List

from ...domain.seller import schemas, models


def convert(db_seller: models.Seller):
    ''' Customized convertion to response template '''
    return schemas.Seller(
        id=db_seller.id,
        name=db_seller.name,
        cpf=db_seller.cpf,
        phone=db_seller.phone)


def convert_many(db_sellers: List):
    ''' Convert list customized '''
    return [convert(db_seller) for db_seller in db_sellers]