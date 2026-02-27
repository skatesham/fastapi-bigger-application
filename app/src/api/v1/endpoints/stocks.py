from typing import List

from fastapi import APIRouter

from ...deps import Database, StockService, StockConverter
from ....domain.stock import schemas

router = APIRouter()


@router.post("/", response_model=schemas.Stock, status_code=201)
def create_stock(
    stock: schemas.StockCreate,
    db: Database,
    stock_service: StockService,
    stock_converter: StockConverter,
):
    """Create new stock using dependency injection"""
    db_stock = stock_service.create_stock(db=db, stock=stock)
    return stock_converter.convert(db_stock)


@router.get("/{stock_id}", response_model=schemas.Stock)
def read_stock(
    stock_id: int,
    db: Database,
    stock_service: StockService,
    stock_converter: StockConverter,
):
    """Get stock by ID using dependency injection"""
    db_stock = stock_service.get_stock(db, stock_id=stock_id)
    return stock_converter.convert(db_stock)


@router.get("/", response_model=List[schemas.Stock])
def read_stocks(
    db: Database,
    stock_service: StockService,
    stock_converter: StockConverter,
    skip: int = 0,
    limit: int = 100,
):
    """Get all stocks with pagination using dependency injection"""
    db_stocks = stock_service.get_stocks(db, skip=skip, limit=limit)
    return stock_converter.convert_many(db_stocks)


@router.delete("/{stock_id}", response_model=bool)
def delete_stock(
    stock_id: int,
    db: Database,
    stock_service: StockService,
):
    """Delete stock by ID using dependency injection"""
    return stock_service.remove_stock(db, stock_id=stock_id)
