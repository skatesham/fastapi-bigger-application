from fastapi import HTTPException
from sqlalchemy.orm import Session

from ....resources.strings import CAR_DOES_NOT_EXIST_ERROR
from . import repository, schemas


def create_car(db: Session, car: schemas.CarCreate):
    return repository.create_car(db, car)


def get_car(db: Session, car_id: int):
    db_car = repository.get_car(db, car_id=car_id)
    if db_car is None:
        raise HTTPException(status_code=404, detail=CAR_DOES_NOT_EXIST_ERROR)
    return repository.get_car(db, car_id)


def get_cars(db: Session, skip: int = 0, limit: int = 100):
    return repository.get_cars(db, skip, limit)


def remove_car(db: Session, car_id: int):
    db_car = get_car(db, car_id=car_id)
    if db_car is None:
        raise HTTPException(status_code=404, detail=CAR_DOES_NOT_EXIST_ERROR)
    return repository.remove_car(db, db_car)
