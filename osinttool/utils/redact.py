import re

SECRET_RX = re.compile(r"(?i)\b(api[_-]?key|token|password)\b\s*[:=]\s*([^\s]{6,})")


def redact_text(s: str) -> str:
    """Redacts API keys, tokens, or passwords in a string.

    This uses a case-insensitive regex to detect common secret patterns such as
    API keys, tokens, or passwords defined as key=value pairs. The secret value
    is replaced with a placeholder indicating the original length to avoid
    leaking the secret while retaining context.

    Args:
        s: The input string potentially containing secrets.

    Returns:
        The redacted string with secrets obfuscated.
    """
    if not s:
        return s

    def repl(match: re.Match[str]) -> str:
        key = match.group(1)
        secret_value = match.group(2) or ""
        return f"{key}=<redacted:{len(secret_value)}>"

    return SECRET_RX.sub(repl, s)
