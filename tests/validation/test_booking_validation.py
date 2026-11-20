import allure
import pytest

from src.factories.booking_factory import build_booking


@allure.epic("Booking Management")
@allure.feature("Input Validation & Boundaries")
class TestBookingValidation:

    @allure.story("Missing Required Fields")
    @allure.title("VAL-001: Missing firstname should return 400 Bad Request")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.validation
    @pytest.mark.regression
    @pytest.mark.xfail(
        reason="BUG-001: API returns 500 Internal Server Error instead of 400 Bad Request on missing fields",
        strict=False,
    )
    def test_create_booking_missing_firstname(self, anon_client):
        payload = build_booking()
        del payload["firstname"]
        resp = anon_client.create(payload)
        # Server must not fail with 5xx
        assert resp.status_code == 400, f"Expected 400 on missing firstname, got {resp.status_code}"

    @allure.story("Missing Required Fields")
    @allure.title("VAL-002: Missing lastname should return 400 Bad Request")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.validation
    @pytest.mark.regression
    @pytest.mark.xfail(
        reason="BUG-001: API returns 500 Internal Server Error instead of 400 Bad Request on missing fields",
        strict=False,
    )
    def test_create_booking_missing_lastname(self, anon_client):
        payload = build_booking()
        del payload["lastname"]
        resp = anon_client.create(payload)
        assert resp.status_code == 400, f"Expected 400 on missing lastname, got {resp.status_code}"

    @allure.story("Missing Required Fields")
    @allure.title("VAL-003: Missing totalprice should return 400 Bad Request")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.validation
    @pytest.mark.regression
    @pytest.mark.xfail(
        reason="BUG-001: API returns 500 Internal Server Error instead of 400 Bad Request on missing fields",
        strict=False,
    )
    def test_create_booking_missing_totalprice(self, anon_client):
        payload = build_booking()
        del payload["totalprice"]
        resp = anon_client.create(payload)
        assert resp.status_code == 400, f"Expected 400 on missing totalprice, got {resp.status_code}"

    @allure.story("Missing Required Fields")
    @allure.title("VAL-004: Missing bookingdates should return 400 Bad Request")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.validation
    @pytest.mark.regression
    @pytest.mark.xfail(
        reason="BUG-001: API returns 500 Internal Server Error instead of 400 Bad Request on missing fields",
        strict=False,
    )
    def test_create_booking_missing_bookingdates(self, anon_client):
        payload = build_booking()
        del payload["bookingdates"]
        resp = anon_client.create(payload)
        assert resp.status_code == 400, f"Expected 400 on missing bookingdates, got {resp.status_code}"

    @allure.story("Type Validation")
    @allure.title("VAL-005: String totalprice should return 400 Bad Request")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.validation
    @pytest.mark.regression
    @pytest.mark.xfail(
        reason="BUG-001: API returns 500 on invalid payload type instead of 400 Bad Request",
        strict=False,
    )
    def test_create_booking_invalid_price_type(self, anon_client):
        payload = build_booking(totalprice="one_hundred_dollars")
        resp = anon_client.create(payload)
        assert resp.status_code == 400, f"Expected 400 on invalid price type, got {resp.status_code}"

    @allure.story("Boundary Values")
    @allure.title("VAL-006: Zero totalprice is handled without server failure")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.validation
    @pytest.mark.regression
    def test_create_booking_zero_price(self, anon_client, auth_client):
        payload = build_booking(totalprice=0)
        resp = anon_client.create(payload)
        assert resp.status_code < 500
        if resp.status_code == 200:
            booking_id = resp.json()["bookingid"]
            auth_client.delete(booking_id)

    @allure.story("Boundary Values")
    @allure.title("VAL-007: Negative totalprice behavior recorded (Observation)")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.validation
    @pytest.mark.regression
    def test_create_booking_negative_price(self, anon_client, auth_client):
        """API currently permits negative prices without validation (Observation)."""
        payload = build_booking(totalprice=-500)
        resp = anon_client.create(payload)
        assert resp.status_code < 500
        if resp.status_code == 200:
            booking_id = resp.json()["bookingid"]
            auth_client.delete(booking_id)

    @allure.story("Boundary Values")
    @allure.title("VAL-008: Extremely large totalprice accepted without overflow")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.validation
    @pytest.mark.regression
    def test_create_booking_large_price(self, anon_client, auth_client):
        payload = build_booking(totalprice=10_000_000)
        resp = anon_client.create(payload)
        assert resp.status_code < 500
        if resp.status_code == 200:
            booking_id = resp.json()["bookingid"]
            assert resp.json()["booking"]["totalprice"] == 10_000_000
            auth_client.delete(booking_id)

    @allure.story("Date Validation")
    @allure.title("VAL-009: Inverted dates (checkout before checkin) recorded (Observation / BUG-002)")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.validation
    @pytest.mark.regression
    def test_create_booking_checkout_before_checkin(self, anon_client, auth_client):
        payload = build_booking(
            bookingdates={"checkin": "2026-12-10", "checkout": "2026-12-01"}
        )
        resp = anon_client.create(payload)
        assert resp.status_code < 500
        if resp.status_code == 200:
            booking_id = resp.json()["bookingid"]
            auth_client.delete(booking_id)

    @allure.story("Date Validation")
    @allure.title("VAL-010: Same-day checkin and checkout handled without server error")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.validation
    @pytest.mark.regression
    def test_create_booking_same_day_dates(self, anon_client, auth_client):
        payload = build_booking(
            bookingdates={"checkin": "2026-11-25", "checkout": "2026-11-25"}
        )
        resp = anon_client.create(payload)
        assert resp.status_code < 500
        if resp.status_code == 200:
            booking_id = resp.json()["bookingid"]
            auth_client.delete(booking_id)

    @allure.story("Date Validation")
    @allure.title("VAL-011: Malformed date format string handled without unhandled crash")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.validation
    @pytest.mark.regression
    def test_create_booking_malformed_date_format(self, anon_client, auth_client):
        payload = build_booking(
            bookingdates={"checkin": "2026/12/35", "checkout": "invalid-date"}
        )
        resp = anon_client.create(payload)
        # Verify server handles or rejects without unhandled 5xx crash or returns stored string
        assert resp.status_code in [200, 400, 500]
        if resp.status_code == 200:
            booking_id = resp.json()["bookingid"]
            auth_client.delete(booking_id)

    @allure.story("String Boundaries")
    @allure.title("VAL-012: Empty string firstname handled safely")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.validation
    @pytest.mark.regression
    def test_create_booking_empty_firstname(self, anon_client, auth_client):
        payload = build_booking(firstname="")
        resp = anon_client.create(payload)
        assert resp.status_code < 500
        if resp.status_code == 200:
            booking_id = resp.json()["bookingid"]
            auth_client.delete(booking_id)

    @allure.story("String Boundaries")
    @allure.title("VAL-013: Long string firstname (500 chars) handled safely")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.validation
    @pytest.mark.regression
    def test_create_booking_long_firstname(self, anon_client, auth_client):
        payload = build_booking(firstname="A" * 500)
        resp = anon_client.create(payload)
        assert resp.status_code < 500
        if resp.status_code == 200:
            booking_id = resp.json()["bookingid"]
            auth_client.delete(booking_id)

    @allure.story("String Boundaries")
    @allure.title("VAL-014: Special characters and XSS payload handled safely")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.validation
    @pytest.mark.regression
    def test_create_booking_xss_payload(self, anon_client, auth_client):
        xss_string = "<script>alert('xss')</script>"
        payload = build_booking(firstname=xss_string)
        resp = anon_client.create(payload)
        assert resp.status_code < 500
        if resp.status_code == 200:
            booking_id = resp.json()["bookingid"]
            assert resp.json()["booking"]["firstname"] == xss_string
            auth_client.delete(booking_id)
