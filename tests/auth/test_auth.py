import allure
import pytest

from config.settings import settings
from src.clients.auth_client import AuthClient
from src.clients.booking_client import BookingClient
from src.factories.booking_factory import build_booking


@allure.epic("Authentication")
@allure.feature("Token Generation")
class TestAuth:

    @allure.story("Login")
    @allure.title("AUTH-001: Valid credentials generate auth token")
    @allure.severity(allure.severity_level.BLOCKER)
    @pytest.mark.smoke
    @pytest.mark.auth
    @pytest.mark.regression
    def test_login_valid_credentials_success(self):
        client = AuthClient()
        resp = client.login(settings.rb_username, settings.rb_password)
        assert resp.status_code == 200
        body = resp.json()
        assert "token" in body
        assert isinstance(body["token"], str)
        assert len(body["token"]) > 0

    @allure.story("Login Negative")
    @allure.title("AUTH-002: Invalid password returns bad credentials reason")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.auth
    @pytest.mark.regression
    def test_login_invalid_password_rejected(self):
        client = AuthClient()
        resp = client.login(settings.rb_username, "wrong_password_xyz")
        assert resp.status_code == 200
        body = resp.json()
        assert body.get("reason") == "Bad credentials"

    @allure.story("Login Negative")
    @allure.title("AUTH-003: Unknown username returns bad credentials reason")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.auth
    @pytest.mark.regression
    def test_login_unknown_username_rejected(self):
        client = AuthClient()
        resp = client.login("nonexistent_user_999", settings.rb_password)
        assert resp.status_code == 200
        body = resp.json()
        assert body.get("reason") == "Bad credentials"

    @allure.story("Login Negative")
    @allure.title("AUTH-004: Empty JSON body returns bad credentials")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.auth
    @pytest.mark.regression
    def test_login_empty_body(self):
        client = AuthClient()
        resp = client.request("POST", "/auth", json={})
        assert resp.status_code == 200
        assert resp.json().get("reason") == "Bad credentials"

    @allure.story("Login Negative")
    @allure.title("AUTH-005: Missing password field returns bad credentials")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.auth
    @pytest.mark.regression
    def test_login_missing_password(self):
        client = AuthClient()
        resp = client.request("POST", "/auth", json={"username": settings.rb_username})
        assert resp.status_code == 200
        assert resp.json().get("reason") == "Bad credentials"

    @allure.story("Login Negative")
    @allure.title("AUTH-006: Missing username field returns bad credentials")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.auth
    @pytest.mark.regression
    def test_login_missing_username(self):
        client = AuthClient()
        resp = client.request("POST", "/auth", json={"password": settings.rb_password})
        assert resp.status_code == 200
        assert resp.json().get("reason") == "Bad credentials"

    @allure.story("Auth Mechanisms")
    @allure.title("AUTH-007: Basic auth header vs cookie token support on PUT")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.auth
    @pytest.mark.regression
    def test_basic_auth_header_accepted(self, anon_client, auth_client, created_booking):
        """Restful-Booker docs specify Basic Auth is also supported via Authorization header."""
        booking_id = created_booking["id"]
        updated_payload = build_booking(firstname="BasicAuthUser")

        # Basic Auth: admin:password123 base64 encoded is YWRtaW46cGFzc3dvcmQxMjM=
        resp = anon_client.request(
            "PUT",
            f"/booking/{booking_id}",
            json=updated_payload,
            headers={"Authorization": "Basic YWRtaW46cGFzc3dvcmQxMjM="},
        )
        assert resp.status_code == 200
        assert resp.json()["firstname"] == "BasicAuthUser"

    @allure.story("Auth Mechanisms")
    @allure.title("AUTH-008: Invalid Bearer Authorization header rejected")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.auth
    @pytest.mark.regression
    def test_bearer_token_not_accepted(self, anon_client, token, created_booking):
        """Restful-Booker does not use standard Bearer authorization header."""
        booking_id = created_booking["id"]
        resp = anon_client.request(
            "PUT",
            f"/booking/{booking_id}",
            json=build_booking(),
            headers={"Authorization": f"Bearer {token}"},
        )
        assert resp.status_code == 403
