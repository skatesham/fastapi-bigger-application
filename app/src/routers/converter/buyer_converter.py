from typing import List

from ...domain.buyer import schemas, models


def convert(db_buyer: models.Buyer):
    ''' Customized convertion to response template '''
    return schemas.Buyer(
        id=db_buyer.id,
        name=db_buyer.name,
        phone=db_buyer.phone,
        address=schemas.Address(
                cep=db_buyer.address_cep,
                public_place=db_buyer.address_public_place,
                city=db_buyer.address_city,
                district=db_buyer.address_district,
                state=db_buyer.address_state,
            )
        )


def convert_many(db_buyers: List):
    ''' Convert list customized '''
    return [convert(db_buyer) for db_buyer in db_buyers]