from typing import List
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate

from fastapi import APIRouter, HTTPException, Query
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate

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


@router.get("/", response_model=Page[schemas.Car])
def read_cars(
    db: Database,
    car_service: CarService,
):
    """Get all cars with automatic pagination"""
    return car_service.get_cars(db)


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


@router.get("/search/", response_model=List[schemas.Car])
def search_cars(
    db: Database,
    car_service: CarService,
    brand: str = Query(..., description="Search cars by brand"),
):
    """Search cars by brand"""
    return car_service.search_cars_by_brand(db, brand=brand)
