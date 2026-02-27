import pytest


@pytest.fixture
def car_json():
    return {"id": 1, "name": "Galardo", "year": 1999, "brand": "lamborghini"}


@pytest.fixture
def car_not_found_error():
    return {"errors": ["car does not exist"]}
