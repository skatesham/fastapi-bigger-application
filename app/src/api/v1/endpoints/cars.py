from typing import List

from fastapi import APIRouter, HTTPException

from app.src.api.deps import Database, CarService
from app.src.domain.car import exceptions, schemas
from app.resources.strings import CAR_ALREADY_EXISTS_ERROR, CAR_DOES_NOT_EXIST_ERROR

router = APIRouter()


@router.post("/", response_model=schemas.Car, status_code=201)
def create_car(
    car: schemas.CarCreate,
    db: Database,
    car_service: CarService,
):
    """Create new car using dependency injection"""
    try:
        return car_service.create_car(db=db, car=car)
    except exceptions.CarAlreadyExistsError as e:
        raise HTTPException(status_code=409, detail=CAR_ALREADY_EXISTS_ERROR)


@router.get("/{car_id}", response_model=schemas.Car)
def read_car(
    car_id: int,
    db: Database,
    car_service: CarService,
):
    """Get car by ID using dependency injection"""
    try:
        return car_service.get_car(db, car_id=car_id)
    except exceptions.CarNotFoundError as e:
        raise HTTPException(status_code=404, detail=CAR_DOES_NOT_EXIST_ERROR)


@router.get("/", response_model=List[schemas.Car])
def read_cars(
    db: Database,
    car_service: CarService,
    skip: int = 0,
    limit: int = 100,
):
    """Get all cars with pagination using dependency injection"""
    cars = car_service.get_cars(db, skip=skip, limit=limit)
    return cars


@router.delete("/{car_id}", response_model=bool)
def delete_car(
    car_id: int,
    db: Database,
    car_service: CarService,
):
    """Delete car by ID using dependency injection"""
    try:
        return car_service.delete_car(db, car_id=car_id)
    except exceptions.CarNotFoundError as e:
        raise HTTPException(status_code=404, detail=CAR_DOES_NOT_EXIST_ERROR)
