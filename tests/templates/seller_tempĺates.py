import pytest


@pytest.fixture
def seller_json():
    return {
        "id": 1,
        "name": "João da Silva",
        "cpf": "69285717640",
        "phone": "1299871234",
    }


@pytest.fixture
def seller_not_found_error():
    return {"detail": "seller does not exist"}
