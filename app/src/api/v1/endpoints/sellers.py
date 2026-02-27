from typing import List

from fastapi import APIRouter, HTTPException

from app.src.api.deps import Database, SellerService
from app.src.domain.seller import exceptions, schemas

router = APIRouter()


@router.post("/", response_model=schemas.Seller, status_code=201)
def create_seller(
    seller: schemas.SellerCreate,
    db: Database,
    seller_service: SellerService,
):
    """Create new seller using dependency injection"""
    try:
        db_seller = seller_service.create_seller(db=db, seller=seller)
        return schemas.Seller.from_model(db_seller)
    except exceptions.SellerAlreadyExistsError as e:
        raise HTTPException(status_code=409, detail=str(e))
    except exceptions.InvalidSellerError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{seller_id}", response_model=schemas.Seller)
def read_seller(
    seller_id: int,
    db: Database,
    seller_service: SellerService,
):
    """Get seller by ID using dependency injection"""
    try:
        db_seller = seller_service.get_seller(db, seller_id=seller_id)
        return schemas.Seller.from_model(db_seller)
    except exceptions.SellerNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/", response_model=List[schemas.Seller])
def read_sellers(
    db: Database,
    seller_service: SellerService,
    skip: int = 0,
    limit: int = 100,
):
    """Get all sellers with pagination using dependency injection"""
    db_sellers = seller_service.get_sellers(db, skip=skip, limit=limit)
    return schemas.Seller.from_models(db_sellers)


@router.delete("/{seller_id}", response_model=bool)
def delete_seller(
    seller_id: int,
    db: Database,
    seller_service: SellerService,
):
    """Delete seller by ID using dependency injection"""
    try:
        return seller_service.delete_seller(db, seller_id=seller_id)
    except exceptions.SellerNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
