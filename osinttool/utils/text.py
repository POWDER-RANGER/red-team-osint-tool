import re
from typing import Iterable, List, Tuple


def normalize_text(s: str) -> str:
    """Normalize and clean input text by stripping null bytes and whitespace."""
    s = s or ""
    s = s.replace("\x00", "")
    return s.strip()


def find_matches(text: str, keywords: Iterable[str], regexes: Iterable[str]) -> Tuple[List[str], List[str]]:
    """Find keyword and regex matches in the given text.

    Returns a tuple of (keyword hits, regex hits). Invalid regex patterns are skipped.
    """
    text_l = (text or "").lower()
    kw_hits: List[str] = []
    for kw in keywords:
        if kw and kw.lower() in text_l:
            kw_hits.append(kw)

    rx_hits: List[str] = []
    for rx in regexes:
        if not rx:
            continue
        try:
            if re.search(rx, text):
                rx_hits.append(rx)
        except re.error:
            # Skip invalid patterns without crashing
            continue

    return kw_hits, rx_hits


def make_snippet(text: str, max_chars: int = 280) -> str:
    """Return a length-limited snippet of the text with ellipsis if truncated."""
    t = normalize_text(text)
    if len(t) <= max_chars:
        return t
    return t[: max_chars - 3] + "..."
