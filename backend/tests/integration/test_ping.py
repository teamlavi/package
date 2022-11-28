import httpx

from .config import BASE_URL


def test_ping():
    """Test the /ping endpoint."""
    result = httpx.get(f"{BASE_URL}/ping")
    assert result.status_code == 200
    assert result.text == "pong"
