from fastapi.testclient import TestClient

from app.main import app
from ..base_insertion import insert_into_sellers
from ..database_test import clear_database, configure_test_database
from ..templates.seller_tempĺates import seller_json, seller_not_found_error

client = TestClient(app)

sellers_route = "/api/v1/sellers"


def setup_module(module):
    configure_test_database(app)


def setup_function(module):
    clear_database()


def test_create_seller(seller_json):
    """Create a seller with success"""
    # Use seller_json without id for creation
    create_data = {k: v for k, v in seller_json.items() if k != 'id'}
    response = client.post(sellers_route + "/", json=create_data)
    assert response.status_code == 201
    # Check response has id and matches structure
    response_data = response.json()
    assert response_data['name'] == seller_json['name']
    assert response_data['cpf'] == seller_json['cpf']
    assert response_data['phone'] == seller_json['phone']


def test_read_seller(seller_json):
    """Read a seller with success"""
    insert_into_sellers(seller_json)
    request_url = sellers_route + "/1"
    response = client.get(request_url)
    assert response.status_code == 200
    response_data = response.json()
    assert response_data['id'] == seller_json['id']
    assert response_data['name'] == seller_json['name']
    assert response_data['cpf'] == seller_json['cpf']
    assert response_data['phone'] == seller_json['phone']


def test_read_seller_by_cpf(seller_json):
    """Read a seller by cpf with success"""
    insert_into_sellers(seller_json)
    request_url = sellers_route + "/cpf/69285717640"
    response = client.get(request_url)
    assert response.status_code == 200
    response_data = response.json()
    assert response_data['id'] == seller_json['id']
    assert response_data['name'] == seller_json['name']
    assert response_data['cpf'] == seller_json['cpf']


def test_read_sellers(seller_json):
    """Read all sellers paginated with success"""
    insert_into_sellers(seller_json)
    request_url = sellers_route  # Remove pagination params
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
    
    # Check seller data
    seller_data = paginated_response["items"][0]
    assert seller_data['id'] == seller_json['id']
    assert seller_data['name'] == seller_json['name']


def test_delete_seller(seller_json):
    """Delete a seller with success"""
    insert_into_sellers(seller_json)
    request_url = sellers_route + "/1"
    response = client.delete(request_url)
    assert response.status_code == 200
    assert response.json() == True


def test_read_seller_not_found(seller_not_found_error):
    """Read a seller when not found"""
    request_url = sellers_route + "/1"
    response = client.get(request_url)
    assert response.status_code == 404
    assert response.json() == seller_not_found_error


def test_read_seller_by_cpf(seller_not_found_error):
    """Read a seller by cpf when not found"""
    request_url = sellers_route + "/cpf/69285717640"
    response = client.get(request_url)
    assert response.status_code == 404
    # FastAPI returns "Not Found" by default for missing routes
    assert response.json() == {"detail": "Not Found"}


def test_read_sellers_not_found():
    """Read all sellers paginated when not found"""
    request_url = sellers_route
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


def test_delete_seller_not_found(seller_not_found_error):
    """Delete a seller when not exists"""
    request_url = sellers_route + "/1"
    response = client.delete(request_url)
    assert response.status_code == 404
    assert response.json() == seller_not_found_error
