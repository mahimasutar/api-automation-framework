import allure
import pytest
from faker import Faker

from src.factories.booking_factory import build_booking

fake = Faker()


@allure.epic("Booking Management")
@allure.feature("Filters & Querying")
class TestBookingFilters:

    @allure.story("Filter by Names")
    @allure.title("FILTER-001: Filter bookings by unique firstname")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.filters
    @pytest.mark.regression
    def test_filter_by_firstname(self, anon_client, auth_client):
        unique_firstname = f"UniqueFirst_{fake.uuid4()[:8]}"
        payload = build_booking(firstname=unique_firstname)
        resp = anon_client.create(payload)
        booking_id = resp.json()["bookingid"]

        try:
            filter_resp = anon_client.list_ids(firstname=unique_firstname)
            assert filter_resp.status_code == 200
            results = filter_resp.json()
            returned_ids = [item["bookingid"] for item in results]
            assert booking_id in returned_ids
        finally:
            auth_client.delete(booking_id)

    @allure.story("Filter by Names")
    @allure.title("FILTER-002: Filter bookings by unique lastname")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.filters
    @pytest.mark.regression
    def test_filter_by_lastname(self, anon_client, auth_client):
        unique_lastname = f"UniqueLast_{fake.uuid4()[:8]}"
        payload = build_booking(lastname=unique_lastname)
        resp = anon_client.create(payload)
        booking_id = resp.json()["bookingid"]

        try:
            filter_resp = anon_client.list_ids(lastname=unique_lastname)
            assert filter_resp.status_code == 200
            results = filter_resp.json()
            returned_ids = [item["bookingid"] for item in results]
            assert booking_id in returned_ids
        finally:
            auth_client.delete(booking_id)

    @allure.story("Filter Combinations")
    @allure.title("FILTER-003: Filter bookings by combined firstname and lastname")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.filters
    @pytest.mark.regression
    def test_filter_by_firstname_and_lastname(self, anon_client, auth_client):
        first = f"ComboFirst_{fake.uuid4()[:6]}"
        last = f"ComboLast_{fake.uuid4()[:6]}"
        payload = build_booking(firstname=first, lastname=last)
        resp = anon_client.create(payload)
        booking_id = resp.json()["bookingid"]

        try:
            filter_resp = anon_client.list_ids(firstname=first, lastname=last)
            assert filter_resp.status_code == 200
            results = filter_resp.json()
            returned_ids = [item["bookingid"] for item in results]
            assert booking_id in returned_ids
        finally:
            auth_client.delete(booking_id)

    @allure.story("Filter by Dates")
    @allure.title("FILTER-004: Filter bookings by checkin date range (strictly greater than)")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.filters
    @pytest.mark.regression
    def test_filter_by_checkin_date(self, anon_client, auth_client):
        """Restful-Booker filters checkin as strictly greater than (>), so query prior day."""
        payload = build_booking(
            bookingdates={"checkin": "2027-01-15", "checkout": "2027-01-20"}
        )
        resp = anon_client.create(payload)
        booking_id = resp.json()["bookingid"]

        try:
            filter_resp = anon_client.list_ids(checkin="2027-01-14")
            assert filter_resp.status_code == 200
            returned_ids = [item["bookingid"] for item in filter_resp.json()]
            assert booking_id in returned_ids
        finally:
            auth_client.delete(booking_id)

    @allure.story("Filter by Dates")
    @allure.title("FILTER-005: Filter bookings by checkout date range")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.filters
    @pytest.mark.regression
    def test_filter_by_checkout_date(self, anon_client, auth_client):
        payload = build_booking(
            bookingdates={"checkin": "2027-02-10", "checkout": "2027-02-18"}
        )
        resp = anon_client.create(payload)
        booking_id = resp.json()["bookingid"]

        try:
            filter_resp = anon_client.list_ids(checkout="2027-02-18")
            assert filter_resp.status_code == 200
            returned_ids = [item["bookingid"] for item in filter_resp.json()]
            assert booking_id in returned_ids
        finally:
            auth_client.delete(booking_id)

    @allure.story("Filter Negative")
    @allure.title("FILTER-006: Filter with no matching criteria returns empty list, not error")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.filters
    @pytest.mark.regression
    def test_filter_nonexistent_returns_empty_list(self, anon_client):
        bogus_name = f"Nonexistent_{fake.uuid4()}"
        resp = anon_client.list_ids(firstname=bogus_name)
        assert resp.status_code == 200
        assert resp.json() == []
