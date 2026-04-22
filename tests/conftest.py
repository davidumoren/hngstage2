import pytest
from unittest.mock import MagicMock
import redis

@pytest.fixture(autouse=True)
def mock_redis(monkeypatch):
    # This intercepts the redis.Redis call and returns a fake object
    mock_red = MagicMock()
    monkeypatch.setattr(redis, "Redis", lambda **kwargs: mock_red)
    return mock_red
