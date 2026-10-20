import pytest

from config.settings import settings
from src.clients.auth_client import AuthClient
from src.clients.booking_client import BookingClient


@pytest.fixture(scope="session")
def token():
    """Session-scoped auth token from Restful-Booker."""
    resp = AuthClient().login(settings.rb_username, settings.rb_password)
    assert resp.status_code == 200, f"Auth failed: {resp.status_code} {resp.text}"
    return resp.json()["token"]


@pytest.fixture
def anon_client():
    """Unauthenticated BookingClient."""
    return BookingClient()


@pytest.fixture
def auth_client(token):
    """Authenticated BookingClient (has token cookie)."""
    return BookingClient(token=token)
