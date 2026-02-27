from typing import List

from ...domain.car import models, schemas


def convert(db_car: models.Car):
    """Customized convertion to response template"""
    return schemas.Car(
        id=db_car.id, name=db_car.name, year=db_car.year, brand=db_car.brand
    )


def convert_many(db_cars: List):
    """Convert list customized"""
    return [convert(db_car) for db_car in db_cars]
