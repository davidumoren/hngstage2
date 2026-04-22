import time
import requests


def wait_for_service(url, timeout=60):
    """Wait until a service becomes available"""
    start = time.time()

    while time.time() - start < timeout:
        try:
            response = requests.get(url)
            if response.status_code == 200:
                return True
        except requests.exceptions.ConnectionError:
            pass

        time.sleep(2)

    raise Exception(f"Service {url} not ready after {timeout}s")


def test_backend_health():
    url = "http://localhost:8000/health"
    wait_for_service(url)

    response = requests.get(url)
    assert response.status_code == 200


def test_frontend_home():
    # ⚠️ FIXED PORT → must match docker-compose
    url = "http://localhost:3000"
    wait_for_service(url)

    response = requests.get(url)
    assert response.status_code == 200


def test_simple_logic():
    assert 1 + 1 == 2