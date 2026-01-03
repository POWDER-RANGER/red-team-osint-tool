from __future__ import annotations
from dataclasses import dataclass
from typing import Iterable, Dict, Any


@dataclass
class Item:
    origin: str
    title: str | None
    text: str
    extra: Dict[str, Any]


class Source:
    """Base class for all OSINT sources.

    Subclasses should implement the `fetch` method and populate
    `self.name` with a descriptive identifier.
    """
    name: str

    def fetch(self) -> Iterable[Item]:
        """Yield items from this source.

        Implementations should return an iterable of `Item` objects. This
        abstract method is meant to be overridden in subclasses.
        """
        raise NotImplementedError
