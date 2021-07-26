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


@router.post("/", response_model=schemas.Car, status_code=201)
def create_car(car: schemas.CarCreate, db: Session = Depends(get_db)):
    return service.create_car(db=db, car=car)

@router.get("/{car_id}", response_model=schemas.Car)
def read_car(car_id: int, db: Session = Depends(get_db)):
    return service.get_car(db, car_id=car_id)

@router.get("/", response_model=List[schemas.Car])
def read_cars(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    cars = service.get_cars(db, skip=skip, limit=limit)
    return cars

@router.delete("/{car_id}", response_model=bool)
def delete_car(car_id: int, db: Session = Depends(get_db)):
    return service.remove_car(db, car_id=car_id)

