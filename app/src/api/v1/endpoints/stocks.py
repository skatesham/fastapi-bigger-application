from typing import List

from fastapi import APIRouter, HTTPException

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
        return schemas.Stock.from_model(db_stock)
    except exceptions.StockAlreadyExistsError as e:
        raise HTTPException(status_code=409, detail=STOCK_ALREADY_EXISTS_ERROR)
    except exceptions.InvalidStockError as e:
        raise HTTPException(status_code=400, detail=INVALID_STOCK_ERROR)


@router.get("/{stock_id}", response_model=schemas.Stock)
def read_stock(
    stock_id: int,
    db: Database,
    stock_service: StockService,
):
    """Get stock by ID using dependency injection"""
    try:
        db_stock = stock_service.get_stock(db, stock_id=stock_id)
        return schemas.Stock.from_model(db_stock)
    except exceptions.StockNotFoundError as e:
        raise HTTPException(status_code=404, detail=STOCK_DOES_NOT_EXIST_ERROR)


@router.get("/", response_model=List[schemas.Stock])
def read_stocks(
    db: Database,
    stock_service: StockService,
    skip: int = 0,
    limit: int = 100,
):
    """Get all stocks with pagination using dependency injection"""
    db_stocks = stock_service.get_stocks(db, skip=skip, limit=limit)
    return schemas.Stock.from_models(db_stocks)


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
