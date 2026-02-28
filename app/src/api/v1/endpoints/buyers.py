from typing import List
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate

from fastapi import APIRouter, HTTPException, Query
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate

from app.src.api.deps import Database, BuyerService
from app.src.domain.buyer import exceptions, schemas
from app.resources.strings import BUYER_ALREADY_EXISTS_ERROR, BUYER_DOES_NOT_EXIST_ERROR, INVALID_BUYER_ERROR

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
        return db_buyer
    except exceptions.BuyerAlreadyExistsError as e:
        raise HTTPException(status_code=409, detail=BUYER_ALREADY_EXISTS_ERROR)
    except exceptions.BuyerInvalidDataError as e:
        raise HTTPException(status_code=400, detail=INVALID_BUYER_ERROR)


@router.get("/{buyer_id}", response_model=schemas.Buyer)
def read_buyer(
    buyer_id: int,
    db: Database,
    buyer_service: BuyerService,
):
    """Get buyer by ID using dependency injection"""
    try:
        db_buyer = buyer_service.get_buyer(db, buyer_id=buyer_id)
        return db_buyer
    except exceptions.BuyerNotFoundError as e:
        raise HTTPException(status_code=404, detail=BUYER_DOES_NOT_EXIST_ERROR)


@router.get("/", response_model=Page[schemas.Buyer])
def read_buyers(
    db: Database,
    buyer_service: BuyerService,
):
    """Get all buyers with automatic pagination"""
    return buyer_service.get_buyers(db)


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
        raise HTTPException(status_code=404, detail=BUYER_DOES_NOT_EXIST_ERROR)


@router.get("/search/", response_model=List[schemas.Buyer])
def search_buyers(
    db: Database,
    buyer_service: BuyerService,
    name: str = Query(..., description="Search buyers by name"),
):
    """Search buyers by name"""
    return buyer_service.search_buyers_by_name(db, name=name)
