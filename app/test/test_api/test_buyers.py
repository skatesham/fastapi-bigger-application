from fastapi.testclient import TestClient

from ..database_test import configure_test_database, clear_database

from ..base_insertion import insert_into_buyers

from ..templates.buyer_tempĺates import buyer_json, buyer_not_found_error

from ...main import app


client = TestClient(app)

buyers_route = "/api/v1/buyers"


def setup_module(module):
    configure_test_database(app)


def setup_function(module):
    clear_database()
    

def test_create_buyer(buyer_json):
    ''' Create a buyer with success '''
    response = client.post(buyers_route + "/", json=buyer_json)
    assert response.status_code == 201
    assert response.json() == buyer_json


def test_read_buyer(buyer_json):
    ''' Read a buyer with success '''
    insert_into_buyers(buyer_json)
    request_url = buyers_route + "/1"
    response = client.get(request_url)
    assert response.status_code == 200
    assert response.json() == buyer_json


def test_read_buyers(buyer_json):
    ''' Read all buyers paginated with success '''
    insert_into_buyers(buyer_json)
    request_url = buyers_route + "?skip=0&limit=100"
    response = client.get(request_url)
    assert response.status_code == 200
    assert response.json() == [ buyer_json ]


def test_delete_buyer(buyer_json):
    ''' Delete a buyer with success '''
    insert_into_buyers(buyer_json)
    request_url = buyers_route + "/1"
    response = client.delete(request_url)
    assert response.status_code == 200
    assert response.json() == True


def test_read_buyer_not_found(buyer_not_found_error):
    ''' Read a buyer when not found '''
    request_url = buyers_route + "/1"
    response = client.get(request_url)
    assert response.status_code == 404
    assert response.json() == buyer_not_found_error
    
    
def test_read_buyers_not_found():
    ''' Read all buyers paginated when not found '''
    request_url = buyers_route + "?skip=0&limit=100"
    response = client.get(request_url)
    assert response.status_code == 200
    assert response.json() == []


def test_delete_buyer_not_found(buyer_not_found_error):
    ''' Delete a buyer when not exists '''
    request_url = buyers_route + "/1"
    response = client.delete(request_url)
    assert response.status_code == 404
    assert response.json() == buyer_not_found_error
    