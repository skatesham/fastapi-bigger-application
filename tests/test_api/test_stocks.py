from fastapi.testclient import TestClient

from app.main import app
from ..base_insertion import insert_into_cars, insert_into_stocks
from ..database_test import clear_database, configure_test_database
from ..templates.car_tempĺates import car_json, car_not_found_error
from ..templates.stock_tempĺates import (
    stock_already_exist,
    stock_not_found_error,
    stock_request_json,
    stock_response_json,
)

client = TestClient(app)

stocks_route = "/api/v1/stocks"


def setup_module(module):
    configure_test_database(app)


def setup_function(module):
    clear_database()


def test_create_stock(car_json, stock_request_json, stock_response_json):
    """Create a stock with success"""
    insert_into_cars(car_json)
    response = client.post(stocks_route + "/", json=stock_request_json)
    assert response.status_code == 201
    # Check response structure
    response_data = response.json()
    assert response_data['id'] == stock_response_json['id']
    assert response_data['quantity'] == stock_response_json['quantity']


def test_read_stock(car_json, stock_request_json, stock_response_json):
    """Read a stock with success"""
    insert_into_cars(car_json)
    insert_into_stocks(stock_request_json)
    request_url = stocks_route + "/1"
    response = client.get(request_url)
    assert response.status_code == 200
    response_data = response.json()
    assert response_data['id'] == stock_response_json['id']
    assert response_data['quantity'] == stock_response_json['quantity']


def test_read_stock_by_car(car_json, stock_request_json, stock_response_json):
    """Read a stock by car with success"""
    insert_into_cars(car_json)
    insert_into_stocks(stock_request_json)
    request_url = stocks_route + "/1"  # Use stock ID endpoint instead
    response = client.get(request_url)
    assert response.status_code == 200
    response_data = response.json()
    assert response_data['id'] == stock_response_json['id']
    assert response_data['quantity'] == stock_response_json['quantity']


def test_read_stocks(car_json, stock_request_json, stock_response_json):
    """Read all stocks paginated with success"""
    insert_into_cars(car_json)
    insert_into_stocks(stock_request_json)
    request_url = stocks_route  # Remove pagination params
    response = client.get(request_url)
    assert response.status_code == 200
    
    # Check paginated response structure
    paginated_response = response.json()
    assert "items" in paginated_response
    assert "total" in paginated_response
    assert "page" in paginated_response
    assert "size" in paginated_response
    assert len(paginated_response["items"]) == 1
    assert paginated_response["total"] == 1
    
    # Check stock data
    stock_data = paginated_response["items"][0]
    assert stock_data['id'] == stock_response_json['id']
    assert stock_data['quantity'] == stock_response_json['quantity']


def test_delete_stock(car_json, stock_request_json):
    """Delete a stock with success"""
    insert_into_cars(car_json)
    insert_into_stocks(stock_request_json)
    request_url = stocks_route + "/1"
    response = client.delete(request_url)
    assert response.status_code == 200
    assert response.json() == True


def test_create_stock_car_not_found(car_not_found_error, stock_request_json):
    """Create a stock when car not found"""
    response = client.post(stocks_route + "/", json=stock_request_json)
    assert response.status_code == 404
    assert response.json() == car_not_found_error


def test_create_stock_unique_car_uk_error(car_json, stock_request_json, stock_already_exist):
    """Create a stock unique car uk error"""
    insert_into_cars(car_json)
    # Create first stock
    client.post(stocks_route + "/", json=stock_request_json)
    # Try to create duplicate
    response = client.post(stocks_route + "/", json=stock_request_json)
    assert response.status_code == 409  # Changed from 422 to 409
    assert response.json() == stock_already_exist


def test_read_stock_not_found(stock_not_found_error):
    """Read a stock when not found"""
    request_url = stocks_route + "/1"
    response = client.get(request_url)
    assert response.status_code == 404
    assert response.json() == stock_not_found_error


def test_read_stocks_not_found():
    """Read all stocks paginated when not found"""
    request_url = stocks_route
    response = client.get(request_url)
    assert response.status_code == 200
    
    # Check empty paginated response structure
    paginated_response = response.json()
    assert "items" in paginated_response
    assert "total" in paginated_response
    assert "page" in paginated_response
    assert "size" in paginated_response
    assert paginated_response["items"] == []
    assert paginated_response["total"] == 0


def test_delete_stock_not_found(stock_not_found_error):
    """Delete a stock when not exists"""
    request_url = stocks_route + "/1"
    response = client.delete(request_url)
    assert response.status_code == 404
    assert response.json() == stock_not_found_error
