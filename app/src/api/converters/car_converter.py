from typing import List

from app.src.domain.car import models, schemas


def convert(db_car: models.Car):
    """Customized conversion to response template"""
    return schemas.Car(
        id=db_car.id,
        name=db_car.name,
        model=db_car.model,
        year=db_car.year,
        price=db_car.price,
        created_at=db_car.created_at,
        updated_at=db_car.updated_at,
    )


def convert_many(db_cars: List):
    """Convert list customized"""
    return [convert(db_car) for db_car in db_cars]
