"""Alert backends for OSINT tool."""

from .webhook import send_webhook
from .email_smtp import send_email

__all__ = ["send_webhook", "send_email"]
