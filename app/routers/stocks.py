from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..dependencies import get_db

from ..domain.stock import service, schemas


router = APIRouter(
    prefix="/stocks",
    tags=["stocks"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)

@router.post("/", response_model=schemas.Stock)
def create_stock(stock: schemas.StockCreate, db: Session = Depends(get_db)):
    return service.create_stock(db=db, stock=stock)

@router.get("/{stock_id}", response_model=schemas.Stock)
def read_stock(stock_id: int, db: Session = Depends(get_db)):
    db_stock = service.get_stock(db, stock_id=stock_id)
    if db_stock is None:
        raise HTTPException(status_code=404, detail="Stock not found")
    return db_stock

@router.get("/", response_model=List[schemas.Stock])
def read_stocks(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    stocks = service.get_stocks(db, skip=skip, limit=limit)
    return stocks

@router.delete("/{stock_id}", response_model=bool)
def delete_stock(stock_id: int, db: Session = Depends(get_db)):
    db_stock = service.get_stock(db, stock_id=stock_id)
    if db_stock is None:
        raise HTTPException(status_code=404, detail="Stock not found")
    return service.remove_stock(db, db_stock=db_stock)

