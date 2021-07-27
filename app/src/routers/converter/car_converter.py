from typing import List

from ...domain.car import schemas, models


def convert(db_car: models.Car):
    return schemas.Car(
            id=db_car.id,
            name=db_car.name,
            year=db_car.year,
            brand=db_car.brand
        )


def convert_many(db_cars: List):
    return [convert(db_car) for db_car in db_cars]