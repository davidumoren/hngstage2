import pytest
from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient


@pytest.fixture
def mock_redis():
    mock = MagicMock()
    mock.ping.return_value = True
    return mock


@pytest.fixture
def client(mock_redis):
    with patch("main.r", mock_redis):
        from main import app
        yield TestClient(app), mock_redis


def test_health_returns_ok(client):
    test_client, mock_r = client
    response = test_client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_create_job_returns_job_id(client):
    test_client, mock_r = client
    response = test_client.post("/jobs")
    assert response.status_code == 200
    assert "job_id" in response.json()


def test_create_job_pushes_to_redis(client):
    test_client, mock_r = client
    response = test_client.post("/jobs")
    job_id = response.json()["job_id"]
    mock_r.lpush.assert_called_once_with("jobs", job_id)


def test_create_job_sets_status_queued(client):
    test_client, mock_r = client
    response = test_client.post("/jobs")
    job_id = response.json()["job_id"]
    mock_r.hset.assert_called_once_with(f"job:{job_id}", "status", "queued")


def test_get_job_found(client):
    test_client, mock_r = client
    mock_r.hget.return_value = b"completed"
    response = test_client.get("/jobs/test-job-123")
    assert response.status_code == 200
    assert response.json()["status"] == "completed"


def test_get_job_not_found(client):
    test_client, mock_r = client
    mock_r.hget.return_value = None
    response = test_client.get("/jobs/nonexistent")
    assert response.json()["error"] == "not found"


def test_health_fails_when_redis_down(client):
    test_client, mock_r = client
    mock_r.ping.side_effect = Exception("Connection refused")
    response = test_client.get("/health")
    assert response.status_code == 503