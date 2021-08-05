import pytest


@pytest.fixture
def buyer_json():
    return {
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


@pytest.fixture
def buyer_not_found_error():
    return { 'errors': ['buyer does not exist'] }

