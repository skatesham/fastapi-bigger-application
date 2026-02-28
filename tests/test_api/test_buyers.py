from fastapi.testclient import TestClient

from app.main import app
from ..base_insertion import insert_into_buyers
from ..database_test import clear_database, configure_test_database
from ..templates.buyer_tempĺates import buyer_json, buyer_not_found_error

client = TestClient(app)

buyers_route = "/api/v1/buyers"


def setup_module(module):
    configure_test_database(app)


def setup_function(module):
    clear_database()


def test_create_buyer(buyer_json):
    """Create a buyer with success"""
    # Use buyer_json without id for creation
    create_data = {k: v for k, v in buyer_json.items() if k != 'id'}
    response = client.post(buyers_route + "/", json=create_data)
    assert response.status_code == 201
    # Check response has id and matches structure
    response_data = response.json()
    assert response_data['name'] == buyer_json['name']
    assert response_data['phone'] == buyer_json['phone']
    # Check address fields are correctly mapped
    assert response_data['address_cep'] == buyer_json['address']['cep']
    assert response_data['address_public_place'] == buyer_json['address']['public_place']
    assert response_data['address_city'] == buyer_json['address']['city']


def test_read_buyer(buyer_json):
    """Read a buyer with success"""
    insert_into_buyers(buyer_json)
    request_url = buyers_route + "/1"
    response = client.get(request_url)
    assert response.status_code == 200
    response_data = response.json()
    assert response_data['id'] == buyer_json['id']
    assert response_data['name'] == buyer_json['name']
    assert response_data['phone'] == buyer_json['phone']
    # Check address fields
    assert response_data['address_cep'] == buyer_json['address']['cep']
    assert response_data['address_public_place'] == buyer_json['address']['public_place']
    assert response_data['address_city'] == buyer_json['address']['city']


def test_read_buyers(buyer_json):
    """Read all buyers paginated with success"""
    insert_into_buyers(buyer_json)
    request_url = buyers_route  # Remove pagination params
    response = client.get(request_url)
    assert response.status_code == 200
    
    # Check paginated response structure
    paginated_response = response.json()
    assert "items" in paginated_response
    assert "total" in paginated_response
    assert "page" in paginated_response
    assert "size" in paginated_response
    assert len(paginated_response["items"]) == 1
    assert paginated_response["total"] == 1
    
    # Check buyer data
    buyer_data = paginated_response["items"][0]
    assert buyer_data['id'] == buyer_json['id']
    assert buyer_data['name'] == buyer_json['name']


def test_delete_buyer(buyer_json):
    """Delete a buyer with success"""
    insert_into_buyers(buyer_json)
    request_url = buyers_route + "/1"
    response = client.delete(request_url)
    assert response.status_code == 200
    assert response.json() == True


def test_read_buyer_not_found(buyer_not_found_error):
    """Read a buyer when not found"""
    request_url = buyers_route + "/1"
    response = client.get(request_url)
    assert response.status_code == 404
    assert response.json() == buyer_not_found_error


def test_read_buyers_not_found():
    """Read all buyers paginated when not found"""
    request_url = buyers_route
    response = client.get(request_url)
    assert response.status_code == 200
    
    # Check empty paginated response structure
    paginated_response = response.json()
    assert "items" in paginated_response
    assert "total" in paginated_response
    assert "page" in paginated_response
    assert "size" in paginated_response
    assert paginated_response["items"] == []
    assert paginated_response["total"] == 0


def test_delete_buyer_not_found(buyer_not_found_error):
    """Delete a buyer when not exists"""
    request_url = buyers_route + "/1"
    response = client.delete(request_url)
    assert response.status_code == 404
    assert response.json() == buyer_not_found_error
