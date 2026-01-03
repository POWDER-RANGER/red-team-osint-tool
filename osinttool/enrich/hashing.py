import hashlib


def sha256_hex(data: bytes) -> str:
    """Return SHA-256 hash of bytes as a hexadecimal string."""
    return hashlib.sha256(data).hexdigest()


def sha256_text(s: str) -> str:
    """Return SHA-256 hash of a string as a hexadecimal string."""
    # Encode the string to bytes using UTF-8 with error replacement
    return sha256_hex((s or "").encode("utf-8", errors="replace"))
