from __future__ import annotations
from typing import Iterable
from bs4 import BeautifulSoup

from .base import Source, Item
from osinttool.utils.requests import RateLimitedSession


class RssSource(Source):
    """Fetches and parses items from an RSS feed."""

    def __init__(self, name: str, url: str, timeout: int = 15) -> None:
        self.name = name
        self.url = url
        self.timeout = timeout
        self.session = RateLimitedSession(timeout=timeout)

    def fetch(self) -> Iterable[Item]:
        """Yield items from the RSS feed."""
        r = self.session.get(self.url, timeout=self.timeout)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "xml")
        for it in soup.find_all("item"):
            title = it.find("title").get_text(strip=True) if it.find("title") else None
            link = it.find("link").get_text(strip=True) if it.find("link") else None
            desc = it.find("description").get_text(" ", strip=True) if it.find("description") else ""
            if not link:
                continue
            yield Item(
                origin=link,
                title=title,
                text=desc or title or "",
                extra={"feed": self.url},
            )
