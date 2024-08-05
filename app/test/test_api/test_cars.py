from fastapi.testclient import TestClient

from ..base_insertion import insert_into_cars
from ..database_test import configure_test_database, clear_database
from ..templates.car_tempĺates import car_json, car_not_found_error
from ...main import app

CAR_ROUTE = "/api/v1/cars"

client = TestClient(app)


def setup_module(module):
    configure_test_database(app)


def setup_function(module):
    clear_database()


def test_create_car(car_json):
    ''' Create a car with success '''
    response = client.post(CAR_ROUTE + "/", json=car_json)
    assert response.status_code == 201
    assert response.json() == car_json


def test_read_car(car_json):
    ''' Read a car with success '''
    insert_into_cars(car_json)

    request_url = CAR_ROUTE + "/1"
    response = client.get(request_url)
    assert response.status_code == 200
    assert response.json() == car_json


def test_read_cars(car_json):
    ''' Read all cars paginated with success '''
    insert_into_cars(car_json)

    request_url = CAR_ROUTE + "?skip=0&limit=100"
    response = client.get(request_url)
    assert response.status_code == 200
    assert response.json() == [car_json]


def test_delete_car(car_json):
    ''' Delete a car with success '''
    insert_into_cars(car_json)

    request_url = CAR_ROUTE + "/1"
    response = client.delete(request_url)
    assert response.status_code == 200
    assert response.json() == True


def test_read_car_not_found(car_not_found_error):
    ''' Read a car when not found '''
    request_url = CAR_ROUTE + "/1"
    response = client.get(request_url)
    assert response.status_code == 404
    assert response.json() == car_not_found_error


def test_read_cars_not_found():
    ''' Read all cars paginated when not found '''
    request_url = CAR_ROUTE + "?skip=0&limit=100"
    response = client.get(request_url)
    assert response.status_code == 200
    assert response.json() == []


def test_delete_car_not_found(car_not_found_error):
    ''' Delete a car when not exists '''
    request_url = CAR_ROUTE + "/1"
    response = client.delete(request_url)
    assert response.status_code == 404
    assert response.json() == car_not_found_error
