from typing import List
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate

from fastapi import APIRouter, HTTPException, Query
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate

from app.src.api.deps import Database, StockService
from app.src.domain.stock import exceptions, schemas
from app.resources.strings import STOCK_ALREADY_EXISTS_ERROR, STOCK_DOES_NOT_EXIST_ERROR, INVALID_STOCK_ERROR

router = APIRouter()


@router.post("/", response_model=schemas.Stock, status_code=201)
def create_stock(
    stock: schemas.StockCreate,
    db: Database,
    stock_service: StockService,
):
    """Create new stock using dependency injection"""
    try:
        db_stock = stock_service.create_stock(db=db, stock=stock)
        return db_stock
    except exceptions.StockAlreadyExistsError as e:
        raise HTTPException(status_code=409, detail=STOCK_ALREADY_EXISTS_ERROR)
    except exceptions.InvalidStockError as e:
        raise HTTPException(status_code=400, detail=INVALID_STOCK_ERROR)
    except Exception as e:
        # Handle CarNotFoundError specifically
        if "Car with id" in str(e) and "not found" in str(e):
            raise HTTPException(status_code=404, detail="car does not exist")
        raise


@router.get("/{stock_id}", response_model=schemas.Stock)
def read_stock(
    stock_id: int,
    db: Database,
    stock_service: StockService,
):
    """Get stock by ID using dependency injection"""
    try:
        db_stock = stock_service.get_stock(db, stock_id=stock_id)
        return db_stock
    except exceptions.StockNotFoundError as e:
        raise HTTPException(status_code=404, detail=STOCK_DOES_NOT_EXIST_ERROR)


@router.get("/", response_model=Page[schemas.Stock])
def read_stocks(
    db: Database,
    stock_service: StockService,
):
    """Get all stocks with automatic pagination"""
    return stock_service.get_stocks(db)


@router.delete("/{stock_id}", response_model=bool)
def delete_stock(
    stock_id: int,
    db: Database,
    stock_service: StockService,
):
    """Delete stock by ID using dependency injection"""
    try:
        return stock_service.delete_stock(db, stock_id=stock_id)
    except exceptions.StockNotFoundError as e:
        raise HTTPException(status_code=404, detail=STOCK_DOES_NOT_EXIST_ERROR)


@router.get("/search/low-stock/", response_model=List[schemas.Stock])
def search_low_stock(
    db: Database,
    stock_service: StockService,
    threshold: int = Query(default=5, description="Stock quantity threshold"),
):
    """Get stocks with quantity below threshold"""
    return stock_service.get_low_stock_items(db, threshold=threshold)


@router.get("/search/available/", response_model=List[schemas.Stock])
def search_available_stock(
    db: Database,
    stock_service: StockService,
):
    """Get all stocks with quantity > 0"""
    return stock_service.get_available_stocks(db)
