import pytest


@pytest.mark.smoke
def test_created_booking_fixture_lifecycle(anon_client, auth_client, created_booking):
    """Verify Phase 2 done criterion: one-line access to clients and fresh booking with cleanup."""
    booking_id = created_booking["id"]
    payload = created_booking["payload"]

    assert booking_id > 0
    resp = anon_client.get(booking_id)
    assert resp.status_code == 200
    data = resp.json()
    assert data["firstname"] == payload["firstname"]
    assert data["lastname"] == payload["lastname"]
    assert data["totalprice"] == payload["totalprice"]
    assert data["bookingdates"] == payload["bookingdates"]
