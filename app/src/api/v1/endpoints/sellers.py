from typing import List
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate

from fastapi import APIRouter, HTTPException, Query
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate

from app.src.api.deps import Database, SellerService
from app.src.domain.seller import exceptions, schemas
from app.resources.strings import SELLER_ALREADY_EXISTS_ERROR, SELLER_DOES_NOT_EXIST_ERROR, INVALID_SELLER_ERROR

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
        return db_seller
    except exceptions.SellerAlreadyExistsError as e:
        raise HTTPException(status_code=409, detail=SELLER_ALREADY_EXISTS_ERROR)
    except exceptions.InvalidSellerError as e:
        raise HTTPException(status_code=400, detail=INVALID_SELLER_ERROR)


@router.get("/{seller_id}", response_model=schemas.Seller)
def read_seller(
    seller_id: int,
    db: Database,
    seller_service: SellerService,
):
    """Get seller by ID using dependency injection"""
    try:
        db_seller = seller_service.get_seller(db, seller_id=seller_id)
        return db_seller
    except exceptions.SellerNotFoundError as e:
        raise HTTPException(status_code=404, detail=SELLER_DOES_NOT_EXIST_ERROR)


@router.get("/", response_model=Page[schemas.Seller])
def read_sellers(
    db: Database,
    seller_service: SellerService,
):
    """Get all sellers with automatic pagination"""
    return seller_service.get_sellers(db)


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
        raise HTTPException(status_code=404, detail=SELLER_DOES_NOT_EXIST_ERROR)


@router.get("/search/", response_model=List[schemas.Seller])
def search_sellers(
    db: Database,
    seller_service: SellerService,
    name: str = Query(..., description="Search sellers by name"),
):
    """Search sellers by name"""
    return seller_service.search_sellers_by_name(db, name=name)
