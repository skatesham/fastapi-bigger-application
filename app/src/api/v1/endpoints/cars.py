from typing import List

from fastapi import APIRouter

from app.src.api.deps import Database, CarService
from app.src.domain.car import schemas

router = APIRouter()


@router.post("/", response_model=schemas.Car, status_code=201)
def create_car(
    car: schemas.CarCreate,
    db: Database,
    car_service: CarService,
):
    """Create new car using dependency injection"""
    return car_service.create_car(db=db, car=car)


@router.get("/{car_id}", response_model=schemas.Car)
def read_car(
    car_id: int,
    db: Database,
    car_service: CarService,
):
    """Get car by ID using dependency injection"""
    return car_service.get_car(db, car_id=car_id)


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
    return car_service.remove_car(db, car_id=car_id)
