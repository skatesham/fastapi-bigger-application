import pytest


@pytest.fixture
def stock_request_json():
    return {
        "id": 1,
        "car_id": 1,
        "quantity": 10
    }
    
@pytest.fixture
def stock_request_json_out_of_stock():
    return {
        "id": 1,
        "car_id": 1,
        "quantity": 0
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


@pytest.fixture
def stock_already_exist():
    return { "errors": ["stock already exist"] }


@pytest.fixture
def stock_out_of_stock():
    return { "errors": ["out of stock"] }

