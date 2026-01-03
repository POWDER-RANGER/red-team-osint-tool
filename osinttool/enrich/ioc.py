from __future__ import annotations
import re
from typing import Dict, List

# Regular expression patterns for common indicators of compromise (IOCs)
IOC_PATTERNS: Dict[str, str] = {
    "ipv4": r"\b(?:\d{1,3}\.){3}\d{1,3}\b",
    "domain": r"\b(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z]{2,}\b",
    "email": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b",
    "md5": r"\b[a-f0-9]{32}\b",
    "sha256": r"\b[a-f0-9]{64}\b",
    "btc": r"\b[13][a-km-zA-HJ-NP-Z1-9]{25,34}\b",
}


def extract_iocs(text: str) -> Dict[str, List[str]]:
    """Extract indicators of compromise (IOCs) from the provided text.

    The function searches for IPv4 addresses, domains, email addresses, hash
    values (MD5 and SHA-256), and Bitcoin addresses using predefined
    regular expressions.

    Args:
        text: The text to search for IOCs.

    Returns:
        A dictionary mapping IOC types to lists of unique matches found.
    """
    out: Dict[str, List[str]] = {}
    for key, pattern in IOC_PATTERNS.items():
        hits = re.findall(pattern, text or "", flags=re.IGNORECASE)
        if hits:
            out[key] = sorted(set(hits))
    return out
