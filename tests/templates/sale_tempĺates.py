from datetime import datetime, timezone

import pytest


@pytest.fixture
def sale_request_json():
    return {
        "id": 1,
        "car_id": 1,
        "seller_id": 1,
        "buyer_id": 1,
        "created_at": str(datetime.now(timezone.utc)),
    }


@pytest.fixture
def sale_response_json():
    return {
        "id": 1,
        "car": {"id": 1, "name": "Galardo", "year": 1999, "brand": "lamborghini"},
        "buyer": {
            "id": 1,
            "name": "Bruce Lee",
            "address_cep": "73770-000",
            "address_public_place": "Banbusal",
            "address_city": "Alto Paraiso de Goias",
            "address_district": "Cidade Baixa",
            "address_state": "Goias",
            "phone": "12996651234",
        },
        "seller": {
            "id": 1,
            "name": "João da Silva",
            "cpf": "69285717640",
            "phone": "1299871234",
        },
        "created_at": None,
    }


@pytest.fixture
def sale_not_found_error():
    return {"detail": "sale does not exist"}


@pytest.fixture
def sale_all_not_found_error():
    return {"detail": "stock does not exist"}
