import pytest

from config.settings import settings
from src.clients.auth_client import AuthClient
from src.clients.booking_client import BookingClient
from src.factories.booking_factory import build_booking


@pytest.fixture
def token():
    """Fresh auth token per test to protect against 10-minute public sandbox database resets."""
    resp = AuthClient().login(settings.rb_username, settings.rb_password)
    assert resp.status_code == 200, f"Auth failed: {resp.status_code} {resp.text}"
    return resp.json()["token"]


@pytest.fixture
def anon_client():
    """Unauthenticated BookingClient."""
    return BookingClient()


@pytest.fixture
def auth_client(token):
    """Authenticated BookingClient (has valid token cookie)."""
    return BookingClient(token=token)


@pytest.fixture
def bad_token_client():
    """BookingClient with an invalid token."""
    return BookingClient(token="invalid_token_99999")


@pytest.fixture
def booking_data():
    """Returns a raw booking payload dict without calling the API."""
    return build_booking()


@pytest.fixture
def created_booking(anon_client, auth_client):
    """Creates a fresh booking via anon_client and guarantees teardown deletion via auth_client."""
    payload = build_booking()
    resp = anon_client.create(payload)
    assert resp.status_code == 200, f"Setup booking creation failed: {resp.status_code} {resp.text}"
    booking_id = resp.json()["bookingid"]
    yield {"id": booking_id, "payload": payload}
    auth_client.delete(booking_id)
