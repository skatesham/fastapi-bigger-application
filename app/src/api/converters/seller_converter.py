from typing import List

from app.src.domain.seller import models, schemas


def convert(db_seller: models.Seller):
    """Customized conversion to response template"""
    return schemas.Seller(
        id=db_seller.id,
        name=db_seller.name,
        email=db_seller.email,
        phone=db_seller.phone,
        created_at=db_seller.created_at,
        updated_at=db_seller.updated_at,
    )


def convert_many(db_sellers: List):
    """Convert list customized"""
    return [convert(db_seller) for db_seller in db_sellers]
