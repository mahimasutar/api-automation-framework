import allure
import pytest

from src.factories.booking_factory import build_booking


@allure.epic("Booking Management")
@allure.feature("Persistence Round-Trips")
class TestBookingPersistence:

    @allure.story("Round-Trip Integrity")
    @allure.title("PERSIST-001: Create and GET round-trip guarantees all fields persisted exactly")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.persistence
    @pytest.mark.regression
    def test_create_and_get_persistence(self, anon_client, auth_client):
        payload = build_booking(additionalneeds="Ocean View")
        create_resp = anon_client.create(payload)
        assert create_resp.status_code == 200
        booking_id = create_resp.json()["bookingid"]

        try:
            get_resp = anon_client.get(booking_id)
            assert get_resp.status_code == 200
            saved = get_resp.json()

            assert saved["firstname"] == payload["firstname"]
            assert saved["lastname"] == payload["lastname"]
            assert saved["totalprice"] == payload["totalprice"]
            assert saved["depositpaid"] == payload["depositpaid"]
            assert saved["bookingdates"]["checkin"] == payload["bookingdates"]["checkin"]
            assert saved["bookingdates"]["checkout"] == payload["bookingdates"]["checkout"]
            assert saved["additionalneeds"] == "Ocean View"
        finally:
            auth_client.delete(booking_id)

    @allure.story("Round-Trip Integrity")
    @allure.title("PERSIST-002: PUT updates persisted fields while preserving bookingid identity")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.persistence
    @pytest.mark.regression
    def test_update_persistence_roundtrip(self, anon_client, auth_client, created_booking):
        booking_id = created_booking["id"]
        updated_payload = build_booking(
            firstname="PersistFirst",
            lastname="PersistLast",
            totalprice=777,
        )

        put_resp = auth_client.update(booking_id, updated_payload)
        assert put_resp.status_code == 200

        # Read back via unauthenticated client
        get_resp = anon_client.get(booking_id)
        assert get_resp.status_code == 200
        saved = get_resp.json()

        assert saved["firstname"] == "PersistFirst"
        assert saved["lastname"] == "PersistLast"
        assert saved["totalprice"] == 777

    @allure.story("Round-Trip Integrity")
    @allure.title("PERSIST-003: PATCH updates targeted field and preserves untouched fields")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.persistence
    @pytest.mark.regression
    def test_patch_persistence_preserves_untouched_fields(
        self, anon_client, auth_client, created_booking
    ):
        booking_id = created_booking["id"]
        original = created_booking["payload"]

        patch_resp = auth_client.patch(booking_id, {"additionalneeds": "Late Checkout"})
        assert patch_resp.status_code == 200

        get_resp = anon_client.get(booking_id)
        assert get_resp.status_code == 200
        saved = get_resp.json()

        assert saved["additionalneeds"] == "Late Checkout"
        assert saved["firstname"] == original["firstname"]
        assert saved["lastname"] == original["lastname"]
        assert saved["totalprice"] == original["totalprice"]
        assert saved["depositpaid"] == original["depositpaid"]

    @allure.story("Round-Trip Integrity")
    @allure.title("PERSIST-004: Created booking ID is discoverable in GET /booking list")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.persistence
    @pytest.mark.regression
    def test_created_id_appears_in_booking_list(self, anon_client, created_booking):
        booking_id = created_booking["id"]
        list_resp = anon_client.list_ids()
        assert list_resp.status_code == 200
        id_list = [item["bookingid"] for item in list_resp.json()]
        assert booking_id in id_list

    @allure.story("Round-Trip Integrity")
    @allure.title("PERSIST-005: Deleted booking is purged from both GET and list index")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.persistence
    @pytest.mark.regression
    def test_delete_purges_record_from_get_and_list(self, anon_client, auth_client):
        payload = build_booking()
        create_resp = anon_client.create(payload)
        booking_id = create_resp.json()["bookingid"]

        del_resp = auth_client.delete(booking_id)
        assert del_resp.status_code == 201

        # Direct GET verification
        get_resp = anon_client.get(booking_id)
        assert get_resp.status_code == 404

        # List index verification
        list_resp = anon_client.list_ids()
        assert list_resp.status_code == 200
        id_list = [item["bookingid"] for item in list_resp.json()]
        assert booking_id not in id_list

    @allure.story("Round-Trip Integrity")
    @allure.title("PERSIST-006: Failed creation request does not contaminate booking index")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.persistence
    @pytest.mark.regression
    def test_failed_create_does_not_add_record(self, anon_client):
        # Count current ids for unique bogus name
        unique_name = "GhostRecord999"
        initial_resp = anon_client.list_ids(firstname=unique_name)
        assert initial_resp.status_code == 200
        assert len(initial_resp.json()) == 0

        # Attempt invalid creation with this unique name
        anon_client.create({"firstname": unique_name})

        # Verify no record was inserted
        after_resp = anon_client.list_ids(firstname=unique_name)
        assert after_resp.status_code == 200
        assert len(after_resp.json()) == 0
