from __future__ import annotations
from typing import List
import smtplib
from email.message import EmailMessage


def send_email(
    host: str,
    port: int,
    username: str,
    password: str,
    from_addr: str,
    to_addrs: List[str],
    subject: str,
    body: str,
) -> None:
    """Send an email using SMTP with TLS.

    Args:
        host: SMTP server hostname.
        port: Port number for the SMTP server.
        username: Username for SMTP authentication.
        password: Password for SMTP authentication.
        from_addr: Sender email address.
        to_addrs: List of recipient email addresses.
        subject: Email subject line.
        body: Plain text body of the email.

    Raises:
        smtplib.SMTPException: If sending fails.
    """
    msg = EmailMessage()
    msg["From"] = from_addr
    msg["To"] = ", ".join(to_addrs)
    msg["Subject"] = subject
    msg.set_content(body)

    with smtplib.SMTP(host, port, timeout=15) as s:
        s.starttls()
        s.login(username, password)
        s.send_message(msg)
