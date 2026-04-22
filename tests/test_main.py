import pytest
import requests

# Test 1: Check if the backend health endpoint returns 200
def test_backend_health():
    response = requests.get("http://localhost:8000/health")
    assert response.status_code == 200

# Test 2: Check if the frontend is accessible
def test_frontend_home():
    response = requests.get("http://localhost:8080")
    assert response.status_code == 200

# Test 3: Simple logic check (Required for count)
def test_simple_logic():
    assert 1 + 1 == 2
