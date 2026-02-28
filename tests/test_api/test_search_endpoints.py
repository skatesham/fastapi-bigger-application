import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_search_cars_by_brand():
    """Test search cars by brand endpoint"""
    # Create a test car first
    car_data = {"name": "Test Search Car", "brand": "SearchBrand", "year": 2022}
    response = client.post("/api/v1/cars", json=car_data)
    assert response.status_code == 201
    
    # Search by brand
    response = client.get("/api/v1/cars/search/?brand=SearchBrand")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["brand"] == "SearchBrand"
    assert data[0]["name"] == "Test Search Car"
    
    # Search non-existent brand
    response = client.get("/api/v1/cars/search/?brand=NonExistent")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 0

def test_search_cars_by_brand_case_insensitive():
    """Test search cars by brand is case insensitive"""
    # Create a test car first
    car_data = {"name": "Case Test Car", "brand": "testbrand", "year": 2022}
    response = client.post("/api/v1/cars", json=car_data)
    assert response.status_code == 201
    
    # Search with different case
    response = client.get("/api/v1/cars/search/?brand=TESTBRAND")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["brand"] == "testbrand"
