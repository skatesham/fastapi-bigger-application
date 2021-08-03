from fastapi.testclient import TestClient

from ..database_test import configure_test_database, insert_into_cars, clear_database

from ...main import app


CAR_ROUTE = "/api/v1/cars"

CAR_JSON = {
    "id": 1,
    "name": "Galardo",
    "year": 1999,
    "brand": "lamborghini"
    }

CAR_ERROR = { 'errors': ['car does not exist'] }


client = TestClient(app)


def setup_function(module):
    configure_test_database(app)
    clear_database() 


def test_create_car():
    ''' Create a car with success '''
    response = client.post(CAR_ROUTE + "/", json=CAR_JSON)
    assert response.status_code == 201
    assert response.json() == CAR_JSON


def test_read_car():
    ''' Read a car with success '''
    insert_into_cars(CAR_JSON)
    
    request_url = CAR_ROUTE + "/1"
    response = client.get(request_url)
    assert response.status_code == 200
    assert response.json() == CAR_JSON


def test_read_cars():
    ''' Read all cars paginated with success '''
    insert_into_cars(CAR_JSON)
    
    request_url = CAR_ROUTE + "?skip=0&limit=100"
    response = client.get(request_url)
    assert response.status_code == 200
    assert response.json() == [ CAR_JSON ]


def test_delete_car():
    ''' Delete a car with success '''
    insert_into_cars(CAR_JSON)
    
    request_url = CAR_ROUTE + "/1"
    response = client.delete(request_url)
    assert response.status_code == 200
    assert response.json() == True


def test_read_car_not_found():
    ''' Read a car when not found '''
    request_url = CAR_ROUTE + "/1"
    response = client.get(request_url)
    assert response.status_code == 404
    assert response.json() == CAR_ERROR
    
    
def test_read_cars_not_found():
    ''' Read all cars paginated when not found '''
    request_url = CAR_ROUTE + "?skip=0&limit=100"
    response = client.get(request_url)
    assert response.status_code == 200
    assert response.json() == []


def test_delete_car_not_found():
    ''' Delete a car when not exists '''
    request_url = CAR_ROUTE + "/1"
    response = client.delete(request_url)
    assert response.status_code == 404
    assert response.json() == CAR_ERROR

