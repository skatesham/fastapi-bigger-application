from typing import List

from fastapi import APIRouter

from ...deps import Database, SellerService, SellerConverter
from ....domain.seller import schemas

router = APIRouter()


@router.post("/", response_model=schemas.Seller, status_code=201)
def create_seller(
    seller: schemas.SellerCreate,
    db: Database,
    seller_service: SellerService,
    seller_converter: SellerConverter,
):
    """Create new seller using dependency injection"""
    db_seller = seller_service.create_seller(db=db, seller=seller)
    return seller_converter.convert(db_seller)


@router.get("/{seller_id}", response_model=schemas.Seller)
def read_seller(
    seller_id: int,
    db: Database,
    seller_service: SellerService,
    seller_converter: SellerConverter,
):
    """Get seller by ID using dependency injection"""
    db_seller = seller_service.get_seller(db, seller_id=seller_id)
    return seller_converter.convert(db_seller)


@router.get("/", response_model=List[schemas.Seller])
def read_sellers(
    db: Database,
    seller_service: SellerService,
    seller_converter: SellerConverter,
    skip: int = 0,
    limit: int = 100,
):
    """Get all sellers with pagination using dependency injection"""
    db_sellers = seller_service.get_sellers(db, skip=skip, limit=limit)
    return seller_converter.convert_many(db_sellers)


@router.delete("/{seller_id}", response_model=bool)
def delete_seller(
    seller_id: int,
    db: Database,
    seller_service: SellerService,
):
    """Delete seller by ID using dependency injection"""
    return seller_service.remove_seller(db, seller_id=seller_id)
