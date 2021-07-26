from fastapi.testclient import TestClient

from ..database_test import configure_test_database

from ...main import app

configure_test_database(app)

client = TestClient(app)

cars_route = "/api/v1/cars"

request_json = {
    "name": "Ram 3",
    "year": 2020,
    "brand": "Dodge"
}

response_json = {
    "id": 1,
    "name": "Ram 3",
    "year": 2020,
    "brand": "Dodge"
}

response_error = { 'detail': 'Car Model not found' }


def test_create_car():
    ''' Create a car with success '''
    response = client.post(cars_route + "/", json=request_json)
    assert response.status_code == 201
    assert response.json() == response_json


def test_read_car():
    ''' Read a car with success '''
    request_url = cars_route + "/1"
    response = client.get(request_url)
    assert response.status_code == 200
    assert response.json() == response_json


def test_read_cars():
    ''' Read all cars paginated with success '''
    request_url = cars_route + "?skip=0&limit=100"
    response = client.get(request_url)
    assert response.status_code == 200
    assert response.json() == [ response_json ]


def test_delete_car():
    ''' Delete a car with success '''
    request_url = cars_route + "/1"
    response = client.delete(request_url)
    assert response.status_code == 200
    assert response.json() == True


def test_read_car_not_found():
    ''' Read a car when not found '''
    request_url = cars_route + "/1"
    response = client.get(request_url)
    assert response.status_code == 404
    assert response.json() == response_error
    
    
def test_read_cars_not_found():
    ''' Read all cars paginated when not found '''
    request_url = cars_route + "?skip=0&limit=100"
    response = client.get(request_url)
    assert response.status_code == 200
    assert response.json() == []


def test_delete_car_not_found():
    ''' Delete a car when not exists '''
    request_url = cars_route + "/1"
    response = client.delete(request_url)
    assert response.status_code == 404
    assert response.json() == response_error
    