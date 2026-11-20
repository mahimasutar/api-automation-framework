import allure
import pytest

from src.factories.booking_factory import build_booking


@allure.epic("Booking Management")
@allure.feature("CRUD Operations")
class TestBookingCRUD:

    @allure.story("Create Booking")
    @allure.title("CRUD-001: Create booking returns 200 with bookingid and payload")
    @allure.severity(allure.severity_level.BLOCKER)
    @pytest.mark.smoke
    @pytest.mark.crud
    @pytest.mark.regression
    def test_create_booking_success(self, anon_client, auth_client):
        payload = build_booking()
        resp = anon_client.create(payload)

        assert resp.status_code == 200
        data = resp.json()
        assert "bookingid" in data
        assert isinstance(data["bookingid"], int)
        booking_id = data["bookingid"]

        booking = data["booking"]
        assert booking["firstname"] == payload["firstname"]
        assert booking["lastname"] == payload["lastname"]
        assert booking["totalprice"] == payload["totalprice"]
        assert booking["depositpaid"] == payload["depositpaid"]
        assert booking["bookingdates"] == payload["bookingdates"]
        assert booking["additionalneeds"] == payload["additionalneeds"]

        # Teardown
        auth_client.delete(booking_id)

    @allure.story("Read Booking")
    @allure.title("CRUD-002: Get booking by ID returns all booking fields")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.crud
    @pytest.mark.regression
    def test_get_booking_by_id_success(self, anon_client, created_booking):
        booking_id = created_booking["id"]
        expected = created_booking["payload"]

        resp = anon_client.get(booking_id)
        assert resp.status_code == 200
        actual = resp.json()

        assert actual["firstname"] == expected["firstname"]
        assert actual["lastname"] == expected["lastname"]
        assert actual["totalprice"] == expected["totalprice"]
        assert actual["depositpaid"] == expected["depositpaid"]
        assert actual["bookingdates"] == expected["bookingdates"]
        assert actual["additionalneeds"] == expected["additionalneeds"]

    @allure.story("Update Booking")
    @allure.title("CRUD-003: PUT completely replaces booking details")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.crud
    @pytest.mark.regression
    def test_put_update_booking_success(self, auth_client, anon_client, created_booking):
        booking_id = created_booking["id"]
        updated_payload = build_booking(
            firstname="UpdatedFirst",
            lastname="UpdatedLast",
            totalprice=999,
            depositpaid=False,
            additionalneeds="Late Checkout",
        )

        resp = auth_client.update(booking_id, updated_payload)
        assert resp.status_code == 200
        data = resp.json()
        assert data["firstname"] == "UpdatedFirst"
        assert data["lastname"] == "UpdatedLast"
        assert data["totalprice"] == 999
        assert data["depositpaid"] is False
        assert data["additionalneeds"] == "Late Checkout"

        # Verify through read client
        get_resp = anon_client.get(booking_id)
        assert get_resp.status_code == 200
        assert get_resp.json()["firstname"] == "UpdatedFirst"

    @allure.story("Partial Update Booking")
    @allure.title("CRUD-004: PATCH updates only specified fields")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.crud
    @pytest.mark.regression
    def test_patch_partial_update_success(self, auth_client, anon_client, created_booking):
        booking_id = created_booking["id"]
        original = created_booking["payload"]
        patch_payload = {"firstname": "PatchedName", "totalprice": 450}

        resp = auth_client.patch(booking_id, patch_payload)
        assert resp.status_code == 200
        data = resp.json()

        assert data["firstname"] == "PatchedName"
        assert data["totalprice"] == 450
        # Untouched fields must stay unchanged
        assert data["lastname"] == original["lastname"]
        assert data["depositpaid"] == original["depositpaid"]
        assert data["bookingdates"] == original["bookingdates"]

    @allure.story("Delete Booking")
    @allure.title("CRUD-005: DELETE booking returns success and subsequent GET returns 404")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    @pytest.mark.crud
    @pytest.mark.regression
    def test_delete_booking_lifecycle(self, anon_client, auth_client):
        # Create dedicated booking to test delete
        payload = build_booking()
        create_resp = anon_client.create(payload)
        booking_id = create_resp.json()["bookingid"]

        del_resp = auth_client.delete(booking_id)
        assert del_resp.status_code == 201

        # Subsequent GET should return 404 Not Found
        get_resp = anon_client.get(booking_id)
        assert get_resp.status_code == 404

    @allure.story("Read Booking Negative")
    @allure.title("CRUD-006: GET nonexistent booking ID returns 404")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.crud
    @pytest.mark.regression
    def test_get_nonexistent_id_returns_404(self, anon_client):
        resp = anon_client.get(999999999)
        assert resp.status_code == 404

    @allure.story("Read Booking Negative")
    @allure.title("CRUD-007: GET non-numeric booking ID returns 404")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.crud
    @pytest.mark.regression
    def test_get_invalid_id_type_returns_404(self, anon_client):
        resp = anon_client.get("invalid_id_format")
        assert resp.status_code == 404

    @allure.story("Delete Booking Negative")
    @allure.title("CRUD-008: DELETE nonexistent booking ID returns 405")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.crud
    @pytest.mark.regression
    def test_delete_nonexistent_id(self, auth_client):
        """Restful-Booker returns 405 Method Not Allowed when attempting DELETE on missing ID."""
        resp = auth_client.delete(999999999)
        assert resp.status_code in [404, 405]

    @allure.story("Update Booking Negative")
    @allure.title("CRUD-009: PUT with missing required fields returns 400 Bad Request")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.crud
    @pytest.mark.regression
    def test_put_missing_required_fields_rejected(self, auth_client, created_booking):
        booking_id = created_booking["id"]
        resp = auth_client.update(booking_id, {"firstname": "Incomplete"})
        assert resp.status_code == 400
