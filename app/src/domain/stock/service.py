from sqlalchemy.orm import Session

# TODO: Remove this dependency
from fastapi import HTTPException

from . import models, schemas


def create_stock(db: Session, stock: schemas.StockCreate):
    db_stock = models.Stock(**stock.dict())
    db.add(db_stock)
    db.commit()
    db.refresh(db_stock)
    return db_stock

def get_stock(db: Session, stock_id: int):
    return db.query(models.Stock).filter(models.Stock.id == stock_id).first()


def get_stock_by_car(db: Session, car_id: int):
    return db.query(models.Stock).filter(models.Stock.car_id == car_id).first()


def buy_car_from_stock(db: Session, car_id: int, quantity: int ):
    db_stock = get_stock_by_car(db, car_id=car_id)
    if db_stock.quantity == 0 or db_stock.quantity < quantity:
        raise HTTPException(status_code=422, detail="Out of stock")
    db_stock.quantity -= quantity
    db.commit()
    db.refresh(db_stock)
    return db_stock


def get_stocks(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Stock).offset(skip).limit(limit).all()


def remove_stock(db: Session, db_stock: models.Stock):
    db.delete(db_stock)
    db.commit()
    return True
