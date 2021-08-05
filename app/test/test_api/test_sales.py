import pytest

from fastapi.testclient import TestClient

from ..database_test import configure_test_database, clear_database

from ..templates.sale_tempĺates import sale_request_json, sale_response_json, sale_not_found_error

from ..templates.car_tempĺates import car_json, car_not_found_error

from ..templates.stock_tempĺates import stock_request_json, stock_not_found_error, stock_out_of_stock, stock_request_json_out_of_stock

from ..templates.seller_tempĺates import seller_json, seller_not_found_error

from ..templates.buyer_tempĺates import buyer_json, buyer_not_found_error

from ..base_insertion import insert_into_sales, insert_into_cars, insert_into_stocks, insert_into_sellers, insert_into_buyers

from ...main import app


configure_test_database(app)

client = TestClient(app)

sales_route = "/api/v1/sales"
    

def setup_module(module):
    configure_test_database(app)


def setup_function(module):
    clear_database()
    
    
def test_create_sale(car_json, stock_request_json, seller_json, buyer_json, sale_request_json, sale_response_json):
    ''' Create a sale with success '''
    insert_into_cars(car_json)
    insert_into_stocks(stock_request_json)
    insert_into_buyers(buyer_json)
    insert_into_sellers(seller_json)
    
    response = client.post(sales_route + "/", json=sale_request_json)
    assert response.status_code == 201
    sale_response_json["created_at"] = response.json()["created_at"]
    assert response.json() == sale_response_json


def test_read_sale(car_json, stock_request_json, seller_json, buyer_json, sale_request_json, sale_response_json):
    ''' Read a sale with success '''
    insert_into_cars(car_json)
    insert_into_stocks(stock_request_json)
    insert_into_buyers(buyer_json)
    insert_into_sellers(seller_json)
    insert_into_sales(sale_request_json)
    request_url = sales_route + "/1"
    response = client.get(request_url)
    assert response.status_code == 200
    sale_response_json["created_at"] = response.json()["created_at"]
    assert response.json() == sale_response_json


def test_read_sales(car_json, stock_request_json, seller_json, buyer_json, sale_request_json, sale_response_json):
    ''' Read all sales paginated with success '''
    insert_into_cars(car_json)
    insert_into_stocks(stock_request_json)
    insert_into_buyers(buyer_json)
    insert_into_sellers(seller_json)
    insert_into_sales(sale_request_json)
    request_url = sales_route + "?skip=0&limit=100"
    response = client.get(request_url)
    assert response.status_code == 200
    sale_response_json["created_at"] = response.json()[0]["created_at"]
    assert response.json() == [ sale_response_json ]


def test_delete_sale(car_json, stock_request_json, seller_json, buyer_json, sale_request_json):
    ''' Delete a sale with success '''
    insert_into_cars(car_json)
    insert_into_stocks(stock_request_json)
    insert_into_buyers(buyer_json)
    insert_into_sellers(seller_json)
    insert_into_sales(sale_request_json)
    request_url = sales_route + "/1"
    response = client.delete(request_url)
    assert response.status_code == 200
    assert response.json() == True


def test_read_sale_not_found(sale_not_found_error):
    ''' Read a sale when not found '''
    request_url = sales_route + "/1"
    response = client.get(request_url)
    assert response.status_code == 404
    assert response.json() == sale_not_found_error
    
    
def test_read_sales_not_found():
    ''' Read all sales paginated when not found '''
    request_url = sales_route + "?skip=0&limit=100"
    response = client.get(request_url)
    assert response.status_code == 200
    assert response.json() == []


def test_delete_sale_not_found(sale_not_found_error):
    ''' Delete a sale when not exists '''
    request_url = sales_route + "/1"
    response = client.delete(request_url)
    assert response.status_code == 404
    assert response.json() == sale_not_found_error


def test_create_sale_car_not_found(stock_request_json, seller_json, buyer_json, sale_request_json, car_not_found_error):
    ''' Create a sale with success '''
    insert_into_stocks(stock_request_json)
    insert_into_buyers(buyer_json)
    insert_into_sellers(seller_json)
    
    response = client.post(sales_route + "/", json=sale_request_json)
    assert response.status_code == 404
    assert response.json() == car_not_found_error


def test_create_sale_buyer_not_found(car_json, stock_request_json, seller_json, sale_request_json, buyer_not_found_error):
    ''' Create a sale with success '''
    insert_into_cars(car_json)
    insert_into_stocks(stock_request_json)
    insert_into_sellers(seller_json)
    
    response = client.post(sales_route + "/", json=sale_request_json)
    assert response.status_code == 404
    assert response.json() == buyer_not_found_error


def test_create_sale_seller_not_found(car_json, stock_request_json, buyer_json, sale_request_json, seller_not_found_error):
    ''' Create a sale with success '''
    insert_into_cars(car_json)
    insert_into_stocks(stock_request_json)
    insert_into_buyers(buyer_json)
    
    response = client.post(sales_route + "/", json=sale_request_json)
    # assert response.status_code == 404
    assert response.json() == seller_not_found_error


def test_create_sale_stock_not_found(car_json, seller_json, buyer_json, sale_request_json, stock_not_found_error):
    ''' Create a sale with success '''
    insert_into_cars(car_json)
    insert_into_buyers(buyer_json)
    insert_into_sellers(seller_json)
    
    response = client.post(sales_route + "/", json=sale_request_json)
    assert response.status_code == 404
    assert response.json() == stock_not_found_error


def test_create_sale_out_of_stock(car_json, seller_json, buyer_json, stock_request_json_out_of_stock, sale_request_json, stock_out_of_stock):
    ''' Create a sale with success '''
    insert_into_cars(car_json)
    insert_into_buyers(buyer_json)
    insert_into_sellers(seller_json)
    insert_into_stocks(stock_request_json_out_of_stock)
    
    response = client.post(sales_route + "/", json=sale_request_json)
    assert response.status_code == 422
    assert response.json() == stock_out_of_stock
    
