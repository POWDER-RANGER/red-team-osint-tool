from __future__ import annotations
from typing import Iterable
import time
import logging
from bs4 import BeautifulSoup

from .base import Source, Item
from osinttool.utils.requests import RateLimitedSession

log = logging.getLogger("osinttool.sources.onion")

try:
    from stem import Signal
    from stem.control import Controller
except Exception:
    # Stem is optional; if unavailable, Tor circuit renewal is disabled
    Controller = None
    Signal = None


class OnionAllowlistSource(Source):
    """Defensive onion monitoring on an allowlist of .onion URLs.

    This source fetches content through a Tor SOCKS proxy. It renews
    circuits optionally via the Tor control port. Only URLs explicitly
    provided are fetched; no crawling occurs.
    """

    def __init__(
        self,
        name: str,
        url: str,
        tor_socks5: str,
        tor_control_port: int = 9051,
        renew_circuit: bool = False,
        timeout: int = 30,
    ) -> None:
        self.name = name
        self.url = url
        self.tor_socks5 = tor_socks5
        self.tor_control_port = tor_control_port
        self.renew_circuit = renew_circuit
        self.timeout = timeout
        self.session = RateLimitedSession(timeout=timeout)

    def _renew(self) -> None:
        """Request a new Tor circuit, if configured and supported."""
        if not self.renew_circuit:
            return
        if not Controller or not Signal:
            log.warning("stem not installed; cannot renew Tor circuits.")
            return
        try:
            with Controller.from_port(port=self.tor_control_port) as c:
                c.authenticate()
                c.signal(Signal.NEWNYM)
                # Wait for a new circuit to take effect
                time.sleep(c.get_newnym_wait())
        except Exception as e:
            log.warning(f"Tor circuit renewal failed: {e}")

    def fetch(self) -> Iterable[Item]:
        """Yield a single Item from the allowlisted onion URL."""
        self._renew()
        proxies = {"http": self.tor_socks5, "https": self.tor_socks5}
        r = self.session.get(self.url, proxies=proxies, timeout=self.timeout)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "lxml")
        text = soup.get_text(" ", strip=True)
        title = soup.title.get_text(strip=True) if soup.title else None
        yield Item(
            origin=self.url,
            title=title,
            text=text,
            extra={"type": "onion", "proxy": self.tor_socks5},
        )
