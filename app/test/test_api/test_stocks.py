from fastapi.testclient import TestClient

from ..database_test import configure_test_database, clear_database

from ..templates.stock_tempĺates import stock_request_json, stock_response_json, stock_not_found_error

from ..templates.car_tempĺates import car_json, car_not_found_error

from ..base_insertion import insert_into_stocks, insert_into_cars

from ...main import app

configure_test_database(app)

client = TestClient(app)

stocks_route = "/api/v1/stocks"

def setup_module(module):
    configure_test_database(app)


def setup_function(module):
    clear_database()
    

def test_create_stock(car_json, stock_request_json, stock_response_json):
    ''' Create a stock with success '''
    insert_into_cars(car_json)
    response = client.post(stocks_route + "/", json=stock_request_json)
    assert response.status_code == 201
    assert response.json() == stock_response_json


def test_read_stock(car_json, stock_request_json, stock_response_json):
    ''' Read a stock with success '''
    insert_into_cars(car_json)
    insert_into_stocks(stock_request_json)
    request_url = stocks_route + "/1"
    response = client.get(request_url)
    assert response.status_code == 200
    assert response.json() == stock_response_json


def test_read_stocks(car_json, stock_request_json, stock_response_json):
    ''' Read all stocks paginated with success '''
    insert_into_cars(car_json)
    insert_into_stocks(stock_request_json)
    request_url = stocks_route + "?skip=0&limit=100"
    response = client.get(request_url)
    assert response.status_code == 200
    assert response.json() == [stock_response_json]


def test_delete_stock(car_json, stock_request_json):
    ''' Delete a stock with success '''
    insert_into_cars(car_json)
    insert_into_stocks(stock_request_json)
    request_url = stocks_route + "/1"
    response = client.delete(request_url)
    assert response.status_code == 200
    assert response.json() == True


def test_read_stock_not_found(stock_not_found_error):
    ''' Read a stock when not found '''
    request_url = stocks_route + "/1"
    response = client.get(request_url)
    assert response.status_code == 404
    assert response.json() == stock_not_found_error


def test_read_stocks_not_found():
    ''' Read all stocks paginated when not found '''
    request_url = stocks_route + "?skip=0&limit=100"
    response = client.get(request_url)
    assert response.status_code == 200
    assert response.json() == []


def test_delete_stock_not_found(stock_not_found_error):
    ''' Delete a stock when not exists '''
    request_url = stocks_route + "/1"
    response = client.delete(request_url)
    assert response.status_code == 404
    assert response.json() == stock_not_found_error
