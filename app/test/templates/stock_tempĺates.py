import pytest


@pytest.fixture
def stock_request_json():
    return {
        "id": 1,
        "car_id": 1,
        "quantity": 10
    }
    
    
@pytest.fixture
def stock_response_json():
    return {
        "id": 1,
        "car": {"id": 1, "name": "Galardo", "year": 1999, "brand": "lamborghini"},
        "quantity": 10
    }


@pytest.fixture
def stock_not_found_error():
    return { "errors": ["stock not found"] }

