from fastapi.testclient import TestClient

from ..database_test import configure_test_database

from ...main import get_application

app = get_application()

configure_test_database(app)

client = TestClient(app)

buyers_route = "/api/v1/buyers"

request_json = {
    "name": "Bruce Lee",
    "address": {
        "cep": "73770-000",
        "public_place": "Banbusal",
        "city": "Alto Paraiso de Goias",
        "district": "Cidade Baixa",
        "state": "Goias"
    },
    "phone": "12996651234"
}

response_json = {
    "id": 1,
    "name": "Bruce Lee",
    "address": {
        "cep": "73770-000",
        "public_place": "Banbusal",
        "city": "Alto Paraiso de Goias",
        "district": "Cidade Baixa",
        "state": "Goias"
    },
    "phone": "12996651234"
}

response_error = { 'detail': 'Buyer not found' }


def test_create_buyer():
    ''' Create a buyer with success '''
    response = client.post(buyers_route + "/", json=request_json)
    assert response.status_code == 201
    assert response.json() == response_json


def test_read_buyer():
    ''' Read a buyer with success '''
    request_url = buyers_route + "/1"
    response = client.get(request_url)
    assert response.status_code == 200
    assert response.json() == response_json


def test_read_buyers():
    ''' Read all buyers paginated with success '''
    request_url = buyers_route + "?skip=0&limit=100"
    response = client.get(request_url)
    assert response.status_code == 200
    assert response.json() == [ response_json ]


def test_delete_buyer():
    ''' Delete a buyer with success '''
    request_url = buyers_route + "/1"
    response = client.delete(request_url)
    assert response.status_code == 200
    assert response.json() == True


def test_read_buyer_not_found():
    ''' Read a buyer when not found '''
    request_url = buyers_route + "/1"
    response = client.get(request_url)
    assert response.status_code == 404
    assert response.json() == response_error
    
    
def test_read_buyers_not_found():
    ''' Read all buyers paginated when not found '''
    request_url = buyers_route + "?skip=0&limit=100"
    response = client.get(request_url)
    assert response.status_code == 200
    assert response.json() == []


def test_delete_buyer_not_found():
    ''' Delete a buyer when not exists '''
    request_url = buyers_route + "/1"
    response = client.delete(request_url)
    assert response.status_code == 404
    assert response.json() == response_error
    