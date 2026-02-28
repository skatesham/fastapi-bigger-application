from fastapi.testclient import TestClient

from app.main import app
from ..database_test import clear_database, configure_test_database

client = TestClient(app)

users_route = "/api/v1/users"


def setup_module(module):
    configure_test_database(app)


def setup_function(module):
    clear_database()


def test_create_user():
    """Create a user with success"""
    user_data = {
        "email": "test@example.com",
        "password": "password123"
    }
    response = client.post(users_route + "/", json=user_data)
    assert response.status_code == 201
    response_data = response.json()
    assert response_data['email'] == user_data['email']
    assert response_data['is_active'] == True
    assert 'id' in response_data


def test_create_user_invalid_email():
    """Create a user with invalid email"""
    user_data = {
        "email": "invalid-email",
        "password": "password123"
    }
    response = client.post(users_route + "/", json=user_data)
    assert response.status_code == 422


def test_create_user_short_password():
    """Create a user with short password"""
    user_data = {
        "email": "test@example.com",
        "password": "123"
    }
    response = client.post(users_route + "/", json=user_data)
    assert response.status_code == 422


def test_read_user():
    """Read a user with success"""
    # First create a user
    user_data = {
        "email": "test@example.com",
        "password": "password123"
    }
    create_response = client.post(users_route + "/", json=user_data)
    user_id = create_response.json()['id']
    
    # Then read the user
    response = client.get(f"{users_route}/{user_id}")
    assert response.status_code == 200
    response_data = response.json()
    assert response_data['email'] == user_data['email']
    assert response_data['id'] == user_id


def test_read_user_not_found():
    """Read a user when not found"""
    response = client.get(users_route + "/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "user does not exist"}


def test_read_users():
    """Read all users paginated with success"""
    # Create a user first
    user_data = {
        "email": "test@example.com",
        "password": "password123"
    }
    client.post(users_route + "/", json=user_data)
    
    response = client.get(users_route)
    assert response.status_code == 200
    
    # Check paginated response structure
    paginated_response = response.json()
    assert "items" in paginated_response
    assert "total" in paginated_response
    assert "page" in paginated_response
    assert "size" in paginated_response
    assert len(paginated_response["items"]) == 1
    assert paginated_response["total"] == 1


def test_read_users_empty():
    """Read all users when none exist"""
    response = client.get(users_route)
    assert response.status_code == 200
    
    # Check empty paginated response structure
    paginated_response = response.json()
    assert "items" in paginated_response
    assert "total" in paginated_response
    assert "page" in paginated_response
    assert "size" in paginated_response
    assert paginated_response["items"] == []
    assert paginated_response["total"] == 0
