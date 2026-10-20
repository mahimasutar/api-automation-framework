from src.clients.base_client import BaseClient


class AuthClient(BaseClient):
    """Client for the /auth endpoint."""

    def login(self, username: str, password: str):
        return self.request(
            "POST",
            "/auth",
            json={"username": username, "password": password},
        )
