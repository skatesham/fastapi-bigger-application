from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..dependencies import get_token_header, get_db

from ..domain.car import service, schemas


router = APIRouter(
    prefix="/cars",
    tags=["cars"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)

@router.post("/", response_model=schemas.Car)
def create_car(car: schemas.CarCreate, db: Session = Depends(get_db)):
    return service.create_car(db=db, car=car)

@router.get("/{car_id}", response_model=schemas.Car)
def read_car(car_id: int, db: Session = Depends(get_db)):
    db_car = service.get_car(db, car_id=car_id)
    if db_car is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_car

@router.get("/", response_model=List[schemas.Car])
def read_cars(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    cars = service.get_cars(db, skip=skip, limit=limit)
    return cars

