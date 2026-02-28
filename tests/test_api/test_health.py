from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

health_route = "/api/v1/system"


def test_health_check():
    """Test basic health check endpoint"""
    response = client.get(f"{health_route}/health")
    assert response.status_code == 200
    response_data = response.json()
    assert response_data['status'] == 'healthy'
    assert 'timestamp' in response_data
    assert 'checks' in response_data


def test_liveness_probe():
    """Test Kubernetes liveness probe"""
    response = client.get(f"{health_route}/health/live")
    assert response.status_code == 200
    response_data = response.json()
    assert response_data['status'] == 'alive'


def test_readiness_probe():
    """Test Kubernetes readiness probe"""
    response = client.get(f"{health_route}/health/ready")
    assert response.status_code == 200
    response_data = response.json()
    assert response_data['status'] == 'ready'


def test_info_endpoint():
    """Test service info endpoint"""
    response = client.get(f"{health_route}/info")
    assert response.status_code == 200
    response_data = response.json()
    assert 'service' in response_data
    assert 'technology' in response_data
    assert 'environment' in response_data
    
    service_info = response_data['service']
    assert 'name' in service_info
    assert 'version' in service_info
    assert 'description' in service_info


def test_api_root():
    """Test API root endpoint"""
    response = client.get("/api/v1/")
    assert response.status_code == 200
    response_data = response.json()
    assert 'message' in response_data
    assert 'version' in response_data
    assert 'docs' in response_data
    assert 'info' in response_data
    assert 'health' in response_data
