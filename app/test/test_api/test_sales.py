from fastapi.testclient import TestClient

from ..database_test import configure_test_database

from ...main import app

configure_test_database(app)

client = TestClient(app)

sales_route = "/api/v1/sales"

request_json = {
  "car_id": 1,
  "seller_id": 1,
  "buyer_id": 1
}

response_json = {
  "id": 1,
  "car": {
    "id": 1,
    "name": "Ram 3",
    "year": 2020,
    "brand": "Dodge"
    },
  "buyer": {
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
    },
  "seller": {
    "id": 1,
    "name": "João da Silva",
    "cpf": "69285717640",
    "phone": "1299871234"
    },
  "created_at": None
}

response_error = { 'errors': ['Sale not found'] }

def create_test_mass():
    client.post("/api/v1/cars/", json={ ## car
        "name": "Ram 3",
        "year": 2020,
        "brand": "Dodge"
    })        
    client.post("/api/v1/stocks/", json={ ## stock
        "car_id": 1,
        "quantity": 10
    })    
    client.post("/api/v1/sellers/", json={ ## seller
        "name": "João da Silva",
        "cpf": "69285717640",
        "phone": "1299871234"
    })    
    client.post("/api/v1/buyers/", json={ ## buyer
        "name": "Bruce Lee",
        "address": {
            "cep": "73770-000",
            "public_place": "Banbusal",
            "city": "Alto Paraiso de Goias",
            "district": "Cidade Baixa",
            "state": "Goias"
        },
        "phone": "12996651234"
    })
    
def teardown_class():
    client.delete("/api/v1/cars/1")
    client.delete("/api/v1/buyers/1")
    client.delete("/api/v1/sellers/1")
    client.delete("/api/v1/stocks/1")
    

def test_create_sale():
    ''' Create a sale with success '''
    create_test_mass()
    
    response = client.post(sales_route + "/", json=request_json)
    assert response.status_code == 201
    response_json["created_at"] = response.json()["created_at"]
    assert response.json() == response_json


def test_read_sale():
    ''' Read a sale with success '''
    request_url = sales_route + "/1"
    response = client.get(request_url)
    assert response.status_code == 200
    response_json["created_at"] = response.json()["created_at"]
    assert response.json() == response_json


def test_read_sales():
    ''' Read all sales paginated with success '''
    request_url = sales_route + "?skip=0&limit=100"
    response = client.get(request_url)
    assert response.status_code == 200
    response_json["created_at"] = response.json()[0]["created_at"]
    assert response.json() == [ response_json ]


def test_delete_sale():
    ''' Delete a sale with success '''
    request_url = sales_route + "/1"
    response = client.delete(request_url)
    assert response.status_code == 200
    assert response.json() == True


def test_read_sale_not_found():
    ''' Read a sale when not found '''
    request_url = sales_route + "/1"
    response = client.get(request_url)
    assert response.status_code == 404
    assert response.json() == response_error
    
    
def test_read_sales_not_found():
    ''' Read all sales paginated when not found '''
    request_url = sales_route + "?skip=0&limit=100"
    response = client.get(request_url)
    assert response.status_code == 200
    assert response.json() == []


def test_delete_sale_not_found():
    ''' Delete a sale when not exists '''
    request_url = sales_route + "/1"
    response = client.delete(request_url)
    assert response.status_code == 404
    assert response.json() == response_error
    teardown_class()

