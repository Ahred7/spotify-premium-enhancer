import socket
import requests
import logging
from typing import Optional

logger = logging.getLogger(__name__)

class SpotifyNetworkInterceptor:
    """Intercepts and modifies Spotify network requests."""

    def __init__(self, proxy_host: str = "127.0.0.1", proxy_port: int = 8888):
        self.proxy_host = proxy_host
        self.proxy_port = proxy_port
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "SpotifyPremiumEnhancer/1.0",
            "X-Premium-Unlock": "true"
        })

    def redirect_to_premium(self, url: str) -> Optional[str]:
        """Redirect premium check endpoints to fake server."""
        premium_endpoints = [
            "https://api.spotify.com/v1/me/premium",
            "https://spclient.wg.spotify.com/premium",
            "https://www.spotify.com/premium/check"
        ]
        if any(endpoint in url for endpoint in premium_endpoints):
            fake_url = f"http://{self.proxy_host}:{self.proxy_port}/premium/ok"
            logger.info(f"Redirecting {url} -> {fake_url}")
            return fake_url
        return None

    def mock_premium_response(self) -> dict:
        """Return fake premium status."""
        return {
            "premium": True,
            "product": "premium",
            "country": "US",
            "account_type": "premium",
            "subscription": {
                "type": "premium",
                "valid_until": "2099-12-31T23:59:59Z"
            }
        }

    def intercept_request(self, method: str, url: str, **kwargs) -> requests.Response:
        """Intercept and potentially modify a request."""
        redirected = self.redirect_to_premium(url)
        if redirected:
            return self.session.request(method, redirected, **kwargs)
        return self.session.request(method, url, **kwargs)

    def health_check(self) -> bool:
        """Check if local proxy is running."""
        try:
            with socket.create_connection((self.proxy_host, self.proxy_port), timeout=2):
                return True
        except (socket.timeout, ConnectionRefusedError):
            logger.warning("Proxy not available")
            return False