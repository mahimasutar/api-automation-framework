import allure
import pytest
from faker import Faker

from src.factories.booking_factory import build_booking

fake = Faker()


@allure.epic("Booking Management")
@allure.feature("End-to-End Scenarios")
class TestBookingE2E:

    @allure.story("Full Lifecycle")
    @allure.title("E2E-001: Complete guest booking lifecycle (Create -> Read -> Update -> Patch -> Delete)")
    @allure.severity(allure.severity_level.BLOCKER)
    @pytest.mark.smoke
    @pytest.mark.e2e
    @pytest.mark.regression
    def test_full_booking_lifecycle_e2e(self, anon_client, auth_client):
        # 1. Create booking
        initial_payload = build_booking(
            firstname="E2EGuest", lastname="Smith", additionalneeds="Quiet room"
        )
        create_resp = anon_client.create(initial_payload)
        assert create_resp.status_code == 200
        booking_id = create_resp.json()["bookingid"]

        try:
            # 2. Read booking
            get_resp = anon_client.get(booking_id)
            assert get_resp.status_code == 200
            assert get_resp.json()["firstname"] == "E2EGuest"

            # 3. Full Update (PUT)
            updated_payload = build_booking(
                firstname="E2EGuest", lastname="SmithUpdated", additionalneeds="Airport shuttle"
            )
            put_resp = auth_client.update(booking_id, updated_payload)
            assert put_resp.status_code == 200
            assert put_resp.json()["additionalneeds"] == "Airport shuttle"

            # 4. Partial Update (PATCH)
            patch_resp = auth_client.patch(booking_id, {"totalprice": 850})
            assert patch_resp.status_code == 200
            assert patch_resp.json()["totalprice"] == 850

            # 5. Verify filter query finds it
            filter_resp = anon_client.list_ids(firstname="E2EGuest")
            assert filter_resp.status_code == 200
            assert booking_id in [item["bookingid"] for item in filter_resp.json()]

            # 6. Delete booking
            del_resp = auth_client.delete(booking_id)
            assert del_resp.status_code == 201

            # 7. Confirm deleted
            verify_deleted = anon_client.get(booking_id)
            assert verify_deleted.status_code == 404
        except Exception:
            auth_client.delete(booking_id)
            raise

    @allure.story("Multi-Booking Isolation")
    @allure.title("E2E-002: Multiple bookings isolated and correctly queried by distinct filters")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.e2e
    @pytest.mark.regression
    def test_multiple_bookings_isolation_e2e(self, anon_client, auth_client):
        unique_tag_1 = f"GuestAlpha_{fake.uuid4()[:6]}"
        unique_tag_2 = f"GuestBeta_{fake.uuid4()[:6]}"

        b1_payload = build_booking(firstname=unique_tag_1, totalprice=100)
        b2_payload = build_booking(firstname=unique_tag_2, totalprice=200)

        r1 = anon_client.create(b1_payload)
        id1 = r1.json()["bookingid"]

        r2 = anon_client.create(b2_payload)
        id2 = r2.json()["bookingid"]

        try:
            # Query for Alpha
            alpha_resp = anon_client.list_ids(firstname=unique_tag_1)
            alpha_ids = [item["bookingid"] for item in alpha_resp.json()]
            assert id1 in alpha_ids
            assert id2 not in alpha_ids

            # Query for Beta
            beta_resp = anon_client.list_ids(firstname=unique_tag_2)
            beta_ids = [item["bookingid"] for item in beta_resp.json()]
            assert id2 in beta_ids
            assert id1 not in beta_ids
        finally:
            auth_client.delete(id1)
            auth_client.delete(id2)
