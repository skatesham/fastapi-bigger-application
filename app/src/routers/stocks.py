from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..dependencies import get_db, get_token_header

from ..domain.stock import service, schemas

from ..domain.car import service as car_service


router = APIRouter(
    prefix="/stocks",
    tags=["stocks"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)

@router.post("/", response_model=schemas.Stock, status_code=201)
def create_stock(stock: schemas.StockCreate, db: Session = Depends(get_db)):
    if car_service.get_car(db, car_id=stock.car_id) is None:
        raise HTTPException(status_code=404, detail="car not found")
    return service.create_stock(db=db, stock=stock)


@router.get("/{stock_id}", response_model=schemas.Stock)
def read_stock(stock_id: int, db: Session = Depends(get_db)):
    db_stock = service.get_stock(db, stock_id=stock_id)
    if db_stock is None:
        raise HTTPException(status_code=404, detail="stock not found")
    return service.get_stock(db, stock_id=stock_id)


@router.get("/car/{car_id}", response_model=schemas.Stock)
def read_stock_by_car(car_id: int, db: Session = Depends(get_db)):
    db_stock = service.get_stock_by_car(db, car_id=car_id)
    if db_stock is None:
        raise HTTPException(status_code=404, detail="stock not found")
    return service.get_stock_by_car(db, car_id=car_id)


@router.get("/", response_model=List[schemas.Stock])
def read_stocks(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return service.get_stocks(db, skip=skip, limit=limit)


@router.delete("/{stock_id}", response_model=bool)
def delete_stock(stock_id: int, db: Session = Depends(get_db)):
    db_stock = service.get_stock(db, stock_id=stock_id)
    if db_stock is None:
        raise HTTPException(status_code=404, detail="stock not found")
    return service.remove_stock(db, db_stock=db_stock)

