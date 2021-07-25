from app.domain import car
from sqlalchemy.orm import Session

from fastapi import HTTPException

from . import models, schemas, repository


def create_stock(db: Session, stock: schemas.StockCreate):
    if repository.get_car(db, car_id=stock.car_id) is None:
        raise HTTPException(status_code=404, detail="Car not found")
    return repository.create_stock(db, stock=stock)

def get_stock(db: Session, stock_id: int):
    db_stock = repository.get_stock(db, stock_id=stock_id)
    if db_stock is None:
        raise HTTPException(status_code=404, detail="Stock not found")
    return repository.get_stock(db, stock_id=stock_id)

def get_stock_by_car(db: Session, car_id: int):
    db_stock = repository.get_stock_by_car(db, car_id=car_id)
    if db_stock is None:
        raise HTTPException(status_code=404, detail="Stock not found")
    return repository.get_stock_by_car(db, car_id=car_id)

def buy_car_from_stock(db: Session, car_id: int):
    db_stock = get_stock_by_car(db, car_id=car_id)
    if db_stock.quantity == 0:
        raise HTTPException(status_code=422, detail="Stock sold off")
    return buy_car_from_stock(db, db_stock=db_stock)  

def get_stocks(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Stock).offset(skip).limit(limit).all()

def remove_stock(db: Session, stock_id: int):
    db_stock = repository.get_stock(db, stock_id=stock_id)
    if db_stock is None:
        raise HTTPException(status_code=404, detail="Stock not found")
    return repository.remove_stock(db, db_stock=db_stock)

