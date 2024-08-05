from fastapi.testclient import TestClient

from ..base_insertion import insert_into_sellers
from ..database_test import configure_test_database, clear_database
from ..templates.seller_tempĺates import seller_json, seller_not_found_error
from ...main import app

client = TestClient(app)

sellers_route = "/api/v1/sellers"


def setup_module(module):
    configure_test_database(app)


def setup_function(module):
    clear_database()


def test_create_seller(seller_json):
    ''' Create a seller with success '''
    response = client.post(sellers_route + "/", json=seller_json)
    assert response.status_code == 201
    assert response.json() == seller_json


def test_read_seller(seller_json):
    ''' Read a seller with success '''
    insert_into_sellers(seller_json)
    request_url = sellers_route + "/1"
    response = client.get(request_url)
    assert response.status_code == 200
    assert response.json() == seller_json


def test_read_seller_by_cpf(seller_json):
    ''' Read a seller by cpf with success '''
    insert_into_sellers(seller_json)
    request_url = sellers_route + "/cpf/69285717640"
    response = client.get(request_url)
    assert response.status_code == 200
    assert response.json() == seller_json


def test_read_sellers(seller_json):
    ''' Read all sellers paginated with success '''
    insert_into_sellers(seller_json)
    request_url = sellers_route + "?skip=0&limit=100"
    response = client.get(request_url)
    assert response.status_code == 200
    assert response.json() == [seller_json]


def test_delete_seller(seller_json):
    ''' Delete a seller with success '''
    insert_into_sellers(seller_json)
    request_url = sellers_route + "/1"
    response = client.delete(request_url)
    assert response.status_code == 200
    assert response.json() == True


def test_read_seller_not_found(seller_not_found_error):
    ''' Read a seller when not found '''
    request_url = sellers_route + "/1"
    response = client.get(request_url)
    assert response.status_code == 404
    assert response.json() == seller_not_found_error


def test_read_seller_by_cpf(seller_not_found_error):
    ''' Read a seller by cpf when not found '''
    request_url = sellers_route + "/cpf/69285717640"
    response = client.get(request_url)
    assert response.status_code == 404
    assert response.json() == seller_not_found_error


def test_read_sellers_not_found():
    ''' Read all sellers paginated when not found '''
    request_url = sellers_route + "?skip=0&limit=100"
    response = client.get(request_url)
    assert response.status_code == 200
    assert response.json() == []


def test_delete_seller_not_found(seller_not_found_error):
    ''' Delete a seller when not exists '''
    request_url = sellers_route + "/1"
    response = client.delete(request_url)
    assert response.status_code == 404
    assert response.json() == seller_not_found_error
