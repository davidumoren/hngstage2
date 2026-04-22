import pytest
import requests

def test_backend_health():
    # Use port 8000 as mapped in docker-compose
    response = requests.get("http://localhost:8000/health")
    assert response.status_code == 200

def test_frontend_home():
    # CHANGE THIS: Use port 80 (the host port)
    response = requests.get("http://localhost:80") 
    assert response.status_code == 200

def test_simple_logic():
    assert 1 + 1 == 2