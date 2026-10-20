import logging

import httpx

from config.settings import settings

log = logging.getLogger(__name__)


class BaseClient:
    """Wrapper around httpx.Client with logging, timeout, and retry."""

    def __init__(self, token: str | None = None):
        headers = {"Accept": "application/json", "Content-Type": "application/json"}
        if token:
            headers["Cookie"] = f"token={token}"
        self.http = httpx.Client(
            base_url=settings.base_url,
            headers=headers,
            timeout=settings.request_timeout,
            transport=httpx.HTTPTransport(retries=2),  # retries connection errors only
        )

    def request(self, method: str, path: str, **kwargs) -> httpx.Response:
        resp = self.http.request(method, path, **kwargs)
        log.info(
            "%s %s -> %s (%.0f ms)",
            method,
            path,
            resp.status_code,
            resp.elapsed.total_seconds() * 1000,
        )
        return resp
