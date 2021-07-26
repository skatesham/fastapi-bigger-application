from fastapi.testclient import TestClient

from ..database_test import configure_test_database

from ...main import app

configure_test_database(app)

client = TestClient(app)

sellers_route = "/api/v1/sellers"


def test_create_seller():
    ''' Create a seller with success '''
    request_json = {
        "name": "João da Silva",
        "cpf": "69285717640",
        "phone": "1299871234"
    }
    response = client.post(sellers_route + "/", json=request_json)
    assert response.status_code == 201
    assert response.json() == {
        "id": 1,
        "name": "João da Silva",
        "cpf": "69285717640",
        "phone": "1299871234"
    }


def test_read_seller():
    ''' Read a seller with success '''
    request_url = sellers_route + "/1"
    response = client.get(request_url)
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "name": "João da Silva",
        "cpf": "69285717640",
        "phone": "1299871234"
    }
    
def test_read_seller_by_cpf():
    ''' Read a seller by cpf with success '''
    request_url = sellers_route + "/cpf/69285717640"
    response = client.get(request_url)
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "name": "João da Silva",
        "cpf": "69285717640",
        "phone": "1299871234"
    }


def test_read_sellers():
    ''' Read all sellers paginated with success '''
    request_url = sellers_route + "?skip=0&limit=100"
    response = client.get(request_url)
    assert response.status_code == 200
    assert response.json() == [
        {
            "id": 1,
            "name": "João da Silva",
            "cpf": "69285717640",
            "phone": "1299871234"
        }
    ]


def test_delete_seller():
    ''' Delete a seller with success '''
    request_url = sellers_route + "/1"
    response = client.delete(request_url)
    assert response.status_code == 200
    assert response.json() == True


def test_read_seller_not_found():
    ''' Read a seller when not found '''
    request_url = sellers_route + "/1"
    response = client.get(request_url)
    assert response.status_code == 404
    assert response.json() == {
        "detail": "Seller not found"
    }


def test_read_seller_by_cpf():
    ''' Read a seller by cpf when not found '''
    request_url = sellers_route + "/cpf/69285717640"
    response = client.get(request_url)
    assert response.status_code == 404
    assert response.json() == {
        "detail": "Seller not found"
    }
    
    
def test_read_sellers_not_found():
    ''' Read all sellers paginated when not found '''
    request_url = sellers_route + "?skip=0&limit=100"
    response = client.get(request_url)
    assert response.status_code == 200
    assert response.json() == []


def test_delete_seller_not_found():
    ''' Delete a seller when not exists '''
    request_url = sellers_route + "/1"
    response = client.delete(request_url)
    assert response.status_code == 404
    assert response.json() == {
        'detail': 'Seller not found'
        }
    