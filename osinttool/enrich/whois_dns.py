from __future__ import annotations
from typing import Dict, Any, Optional
from urllib.parse import urlparse

import dns.resolver
import whois


def extract_domain(url: str) -> Optional[str]:
    """Extract the hostname from a URL. Returns None if parsing fails."""
    try:
        host = urlparse(url).hostname
        return host
    except Exception:
        return None


def dns_lookup(domain: str) -> Dict[str, Any]:
    """Resolve DNS records (A, AAAA, MX) for a domain.

    Returns a dictionary containing lists of A, AAAA, and MX records.
    Exceptions are suppressed to ensure robust operation.
    """
    out: Dict[str, Any] = {"domain": domain, "a": [], "aaaa": [], "mx": []}
    try:
        out["a"] = [r.to_text() for r in dns.resolver.resolve(domain, "A")]
    except Exception:
        pass
    try:
        out["aaaa"] = [r.to_t [r.to_text() for r in dns.resolver.resolve(domain, "AAAA")]

    except Exception:
        pass
    try:
        out["mx"] = [r.exchange.to_text() for r in dns.resolver.resolve(domain, "MX")]
    except Exception:
        pass
    return out


def whois_lookup(domain: str) -> Dict[str, Any]:
    """Perform a WHOIS lookup for a domain and return fields as a dictionary.

    The WHOIS library returns a dict-like object with mixed values; values are
    truncated to 2000 characters to avoid bloating output.
    """
    try:
        w = whois.whois(domain)
        return {k: (str(v)[:2000] if v is not None else None) for k, v in dict(w).items()}
    except Exception:
        return {"error": "whois_failed"}
