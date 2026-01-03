from __future__ import annotations
import os
import random
import time
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# Pool of user agents for polite requests (non-evasive)
UA_POOL = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36",
]


def _env_float(key: str, default: float) -> float:
    """Resolve an environment variable as a float with a default fallback."""
    v = os.getenv(key)
    if not v:
        return default
    try:
        return float(v)
    except ValueError:
        return default


class RateLimitedSession:
    """
    Defensive HTTP session with jittered delays, retries, and simple UA rotation.

    This class is designed to avoid hammering servers while still being resilient
    to transient errors. It is *not* intended to circumvent rate limits or
    detection; it simply makes automated fetching more polite.
    """
    def __init__(
        self,
        min_delay: float | None = None,
        max_delay: float | None = None,
        timeout: int = 20,
        total_retries: int = 3,
    ) -> None:
        self.session = requests.Session()
        self.min_delay = min_delay if min_delay is not None else _env_float("OSINT_MIN_DELAY", 1.0)
        self.max_delay = max_delay if max_delay is not None else _env_float("OSINT_MAX_DELAY", 3.0)
        self.timeout = timeout
        self.last_request_ts = 0.0

        retry = Retry(
            total=total_retries,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["GET", "HEAD"],
            raise_on_status=False,
        )
        adapter = HTTPAdapter(max_retries=retry, pool_connections=20, pool_maxsize=20)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)

    def _sleep_if_needed(self) -> None:
        elapsed = time.time() - self.last_request_ts
        delay = random.uniform(self.min_delay, self.max_delay)
        if elapsed < delay:
            time.sleep(delay - elapsed)

    def get(self, url: str, *, headers: dict | None = None, proxies: dict | None = None, timeout: int | None = None):
        """Perform a rate-limited GET request with optional headers and proxies."""
        self._sleep_if_needed()
        self.last_request_ts = time.time()
        h = dict(headers or {})
        # rotate UA for each request
        h.setdefault("User-Agent", random.choice(UA_POOL))
        return self.session.get(url, headers=h, proxies=proxies, timeout=timeout or self.timeout)
