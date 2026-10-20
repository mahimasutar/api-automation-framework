from src.clients.base_client import BaseClient


class BookingClient(BaseClient):
    """Client for all /booking and /ping endpoints."""

    def ping(self):
        return self.request("GET", "/ping")

    def list_ids(self, **filters):
        return self.request("GET", "/booking", params=filters)

    def get(self, booking_id):
        return self.request("GET", f"/booking/{booking_id}")

    def create(self, payload):
        return self.request("POST", "/booking", json=payload)

    def update(self, booking_id, payload):
        return self.request("PUT", f"/booking/{booking_id}", json=payload)

    def patch(self, booking_id, payload):
        return self.request("PATCH", f"/booking/{booking_id}", json=payload)

    def delete(self, booking_id):
        return self.request("DELETE", f"/booking/{booking_id}")
