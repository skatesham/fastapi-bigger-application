import pytest

from datetime import datetime


@pytest.fixture
def sale_request_json():
    return {
        "id": 1,
        "car_id": 1,
        "seller_id": 1,
        "buyer_id": 1,
        "created_at": str(datetime.utcnow())
    }
    
    
@pytest.fixture
def sale_response_json():
    return {
    "id": 1,
    "car": {
        "id": 1,
        "name": "Galardo",
        "year": 1999,
        "brand": "lamborghini"
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


@pytest.fixture
def sale_not_found_error():
    return { "errors": ["sale not found"] }


@pytest.fixture
def sale_all_not_found_error():
    return {'errors': ['car does not exist, buyer not found, seller not found, stock not found']}

