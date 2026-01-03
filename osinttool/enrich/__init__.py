"""
Enrichment package for the OSINT tool. Provides hashing, WHOIS/DNS lookups, diff computation, and IOC extraction.
"""
from .hashing import sha256_hex, sha256_text
from .whois_dns import extract_domain, dns_lookup, whois_lookup
from .diff import compute_diff
from .ioc import extract_iocs

__all__ = [
    "sha256_hex",
    "sha256_text",
    "extract_domain",
    "dns_lookup",
    "whois_lookup",
    "compute_diff",
    "extract_iocs",
]
