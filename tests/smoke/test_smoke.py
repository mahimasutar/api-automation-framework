import pytest

from src.clients.booking_client import BookingClient


@pytest.mark.smoke
def test_ping_returns_success():
    """Health check: GET /ping should return 201 Created."""
    resp = BookingClient().ping()
    assert resp.status_code == 201, f"Ping failed: {resp.status_code}"


@pytest.mark.smoke
def test_auth_returns_token(token):
    """Auth check: valid credentials should produce a non-empty token string."""
    assert token is not None
    assert isinstance(token, str)
    assert len(token) > 0
