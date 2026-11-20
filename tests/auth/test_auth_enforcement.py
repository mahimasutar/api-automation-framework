import allure
import pytest

from src.factories.booking_factory import build_booking

CASES = [
    ("anon", "PUT", 403),
    ("anon", "PATCH", 403),
    ("anon", "DELETE", 403),
    ("bad_token", "PUT", 403),
    ("bad_token", "PATCH", 403),
    ("bad_token", "DELETE", 403),
]


@allure.epic("Authentication")
@allure.feature("Auth Enforcement Matrix")
class TestAuthEnforcementMatrix:

    @allure.story("Access Control Matrix")
    @allure.title("AUTH-MAT-{who}-{method}: Unauthorized {method} returns {expected}")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.auth
    @pytest.mark.regression
    @pytest.mark.parametrize("who,method,expected", CASES)
    def test_write_requires_valid_auth(
        self, who, method, expected, anon_client, bad_token_client, created_booking
    ):
        client = anon_client if who == "anon" else bad_token_client
        booking_id = created_booking["id"]
        original_payload = created_booking["payload"]

        if method == "PUT":
            payload = build_booking(firstname="Unauthorized")
            resp = client.update(booking_id, payload)
        elif method == "PATCH":
            payload = {"firstname": "Unauthorized"}
            resp = client.patch(booking_id, payload)
        elif method == "DELETE":
            resp = client.delete(booking_id)
        else:
            raise ValueError(f"Unknown method: {method}")

        assert resp.status_code == expected, (
            f"Expected {expected} for {who} {method}, got {resp.status_code}"
        )

        # Confirm booking state is untouched
        verify_resp = anon_client.get(booking_id)
        assert verify_resp.status_code == 200
        verify_data = verify_resp.json()
        assert verify_data["firstname"] == original_payload["firstname"]
        assert verify_data["lastname"] == original_payload["lastname"]
