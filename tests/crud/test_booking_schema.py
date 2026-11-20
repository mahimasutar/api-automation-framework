import allure
import pytest

from src.factories.booking_factory import build_booking
from src.schemas.booking_schema import BookingPayload, BookingResponse


@allure.epic("Booking Management")
@allure.feature("Schema Validation")
class TestBookingSchema:

    @allure.story("Schema Conformity")
    @allure.title("SCHEMA-001: GET /booking/{id} response strictly conforms to BookingPayload schema")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.schema
    @pytest.mark.crud
    @pytest.mark.regression
    def test_get_booking_matches_schema(self, anon_client, created_booking):
        resp = anon_client.get(created_booking["id"])
        assert resp.status_code == 200
        validated = BookingPayload.model_validate(resp.json())
        assert validated.firstname == created_booking["payload"]["firstname"]
        assert validated.lastname == created_booking["payload"]["lastname"]
        assert isinstance(validated.totalprice, int)
        assert isinstance(validated.depositpaid, bool)
        assert isinstance(validated.bookingdates.checkin, str)
        assert isinstance(validated.bookingdates.checkout, str)

    @allure.story("Schema Conformity")
    @allure.title("SCHEMA-002: POST /booking response conforms to BookingResponse schema")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.schema
    @pytest.mark.crud
    @pytest.mark.regression
    def test_create_booking_matches_schema(self, anon_client, auth_client):
        payload = build_booking()
        resp = anon_client.create(payload)
        assert resp.status_code == 200

        validated = BookingResponse.model_validate(resp.json())
        assert validated.bookingid > 0
        assert validated.booking.firstname == payload["firstname"]
        assert validated.booking.lastname == payload["lastname"]

        auth_client.delete(validated.bookingid)

    @allure.story("Schema Conformity")
    @allure.title("SCHEMA-003: GET /booking list items contain valid integer bookingid")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.schema
    @pytest.mark.crud
    @pytest.mark.regression
    def test_list_booking_ids_schema(self, anon_client):
        resp = anon_client.list_ids()
        assert resp.status_code == 200
        items = resp.json()
        assert isinstance(items, list)
        if len(items) > 0:
            sample = items[0]
            assert "bookingid" in sample
            assert isinstance(sample["bookingid"], int)
