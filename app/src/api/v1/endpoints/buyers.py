from typing import List

from fastapi import APIRouter, HTTPException

from app.src.api.deps import Database, BuyerService
from app.src.domain.buyer import exceptions, schemas

router = APIRouter()


@router.post("/", response_model=schemas.Buyer, status_code=201)
def create_buyer(
    buyer: schemas.BuyerCreate,
    db: Database,
    buyer_service: BuyerService,
):
    """Create new buyer using dependency injection"""
    try:
        db_buyer = buyer_service.create_buyer(db=db, buyer=buyer)
        return schemas.Buyer.from_model(db_buyer)
    except exceptions.BuyerAlreadyExistsError as e:
        raise HTTPException(status_code=409, detail=str(e))
    except exceptions.BuyerInvalidDataError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{buyer_id}", response_model=schemas.Buyer)
def read_buyer(
    buyer_id: int,
    db: Database,
    buyer_service: BuyerService,
):
    """Get buyer by ID using dependency injection"""
    try:
        db_buyer = buyer_service.get_buyer(db, buyer_id=buyer_id)
        return schemas.Buyer.from_model(db_buyer)
    except exceptions.BuyerNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/", response_model=List[schemas.Buyer])
def read_buyers(
    db: Database,
    buyer_service: BuyerService,
    skip: int = 0,
    limit: int = 100,
):
    """Get all buyers with pagination using dependency injection"""
    db_buyers = buyer_service.get_buyers(db, skip=skip, limit=limit)
    return schemas.Buyer.from_models(db_buyers)


@router.delete("/{buyer_id}", response_model=bool)
def delete_buyer(
    buyer_id: int,
    db: Database,
    buyer_service: BuyerService,
):
    """Delete buyer by ID using dependency injection"""
    try:
        return buyer_service.delete_buyer(db, buyer_id=buyer_id)
    except exceptions.BuyerNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
