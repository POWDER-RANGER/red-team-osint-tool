from __future__ import annotations
from typing import Iterable
from bs4 import BeautifulSoup

from .base import Source, Item
from osinttool.utils.requests import RateLimitedSession


class HttpPageSource(Source):
    """Fetches and parses a static HTML page."""

    def __init__(self, name: str, url: str, timeout: int = 20) -> None:
        self.name = name
        self.url = url
        self.timeout = timeout
        self.session = RateLimitedSession(timeout=timeout)

    def fetch(self) -> Iterable[Item]:
        r = self.session.get(self.url, timeout=self.timeout)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "lxml")
        text = soup.get_text(" ", strip=True)
        title = soup.title.get_text(strip=True) if soup.title else None
        yield Item(
            origin=self.url,
            title=title,
            text=text,
            extra={"type": "http"},
        )
