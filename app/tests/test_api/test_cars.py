from fastapi.testclient import TestClient

from ...main import app


client = TestClient(app)

cars_route = "/api/v1/cars"

def test_create_car():
    request_json = {
        "name": "Ram 3",
        "year": 2020,
        "brand": "Dodge"
    }
    response = client.post(cars_route + "/", json=request_json)
    assert response.status_code == 201
    assert response.json() == {
        "id": 9,
        "name": "Ram 3",
        "year": 2020,
        "brand": "Dodge"
    }


def test_read_car():
    request_url = cars_route + "/1"
    response = client.get(request_url)
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "name": "KA",
        "year": 2020,
        "brand": "FORD"
    }


def test_read_cars():
    request_url = cars_route + "?skip=0&limit=1"
    response = client.get(request_url)
    assert response.status_code == 200
    assert response.json() == [
        {
        "id": 1,
        "name": "KA",
        "year": 2020,
        "brand": "FORD"
        }
    ]

