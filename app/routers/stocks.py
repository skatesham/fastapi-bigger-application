from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..dependencies import get_db

from ..domain.stock import service, schemas

from ..domain.car import service


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
    return service.get_stock(db, stock_id=stock_id)

@router.get("/car/{car_id}", response_model=schemas.Stock)
def read_stock_by_car(car_id: int, db: Session = Depends(get_db)):
    return service.get_stock_by_car(db, car_id=car_id)

@router.get("/", response_model=List[schemas.Stock])
def read_stocks(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return service.get_stocks(db, skip=skip, limit=limit)

@router.delete("/{stock_id}", response_model=bool)
def delete_stock(stock_id: int, db: Session = Depends(get_db)):
    return service.remove_stock(db, stock_id=stock_id)

