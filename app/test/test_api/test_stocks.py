from fastapi.testclient import TestClient

from ..database_test import configure_test_database

from ...main import app

configure_test_database(app)

client = TestClient(app)

stocks_route = "/api/v1/stocks"

request_json = {
    "car_id": 1,
    "quantity": 10
}

response_json = {
    "id": 1,
    "car": {
        "id": 1,
        "name": "Ram 3",
        "year": 2020,
        "brand": "Dodge"
    },
    "quantity": 10
}

response_error = {"detail": "Stock not found"}

headers = {"X-token":"fake-super-secret-token"}

def create_car():
    response = client.post("/api/v1/cars/", json={
        "name": "Ram 3",
        "year": 2020,
        "brand": "Dodge"
    })

def test_create_stock():
    ''' Create a stock with success '''
    create_car()
    response = client.post(stocks_route + "/", json=request_json)
    assert response.status_code == 201
    assert response.json() == response_json


def test_read_stock():
    ''' Read a stock with success '''
    request_url = stocks_route + "/1"
    response = client.get(request_url)
    assert response.status_code == 200
    assert response.json() == response_json


def test_buy_from_stock_by_car():
    ''' Buy from stock by car with success '''
    
    request_url = stocks_route + "/buy/1/9"
    response = client.patch(request_url, headers=headers)
    assert response.status_code == 200
    response_changed = response_json.copy()
    response_changed["quantity"] = 1
    assert response.json() == response_changed
    
def test_buy_from_stock_by_car_out_of_stock():
    ''' Buy from stock by car when out of stock failure '''
 
    request_url = stocks_route + "/buy/1/100"
    response = client.patch(request_url, headers=headers)
    assert response.status_code == 422
    assert response.json() == {"detail": "Out of stock"}


def test_read_stocks():
    ''' Read all stocks paginated with success '''
    request_url = stocks_route + "?skip=0&limit=100"
    response = client.get(request_url)
    assert response.status_code == 200
    response_changed = response_json.copy()
    response_changed["quantity"] = 1
    assert response.json() == [response_changed]


def test_delete_stock():
    ''' Delete a stock with success '''
    request_url = stocks_route + "/1"
    response = client.delete(request_url)
    assert response.status_code == 200
    assert response.json() == True


def test_read_stock_not_found():
    ''' Read a stock when not found '''
    request_url = stocks_route + "/1"
    response = client.get(request_url)
    assert response.status_code == 404
    assert response.json() == response_error
    
def test_buy_from_stock_by_car_not_found():
    ''' Buy from stock by car when not found '''
    
    request_url = stocks_route + "/buy/1/9"
    response = client.patch(request_url, headers=headers)
    assert response.status_code == 404
    assert response.json() == response_error


def test_read_stocks_not_found():
    ''' Read all stocks paginated when not found '''
    request_url = stocks_route + "?skip=0&limit=100"
    response = client.get(request_url)
    assert response.status_code == 200
    assert response.json() == []


def test_delete_stock_not_found():
    ''' Delete a stock when not exists '''
    request_url = stocks_route + "/1"
    response = client.delete(request_url)
    assert response.status_code == 404
    assert response.json() == response_error
