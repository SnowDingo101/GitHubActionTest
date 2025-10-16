from __future__ import annotations

from dataclasses import dataclass
from email.message import EmailMessage
import smtplib
import ssl
from typing import Iterable, Sequence


@dataclass
class EmailConfig:
    """Configuration for sending an email via SMTP.

    Fields:
    - host/port: SMTP server connection details.
    - username/password: Optional SMTP credentials. If provided, will login.
    - use_tls: Use STARTTLS after connecting (default True).
    - use_ssl: Connect using implicit SSL (SMTPS) (default False).
    - from_addr: Sender email address.
    - to_addrs: One or more recipient email addresses.
    - subject/body: Email content.
    """

    host: str
    port: int
    username: str | None = None
    password: str | None = None
    use_tls: bool = True
    use_ssl: bool = False
    from_addr: str = ""
    to_addrs: Sequence[str] = ()
    subject: str = ""
    body: str = ""


def send_email_smtp(cfg: EmailConfig, timeout: float = 30.0) -> None:
    """Send an email using SMTP based on the provided configuration.

    Raises ValueError for missing required fields.
    Raises smtplib.SMTPException on SMTP errors.
    """

    if not cfg.host:
        raise ValueError("SMTP host is required")
    if not cfg.port:
        raise ValueError("SMTP port is required")
    if not cfg.from_addr:
        raise ValueError("Sender address (from_addr) is required")
    if not cfg.to_addrs:
        raise ValueError("At least one recipient (to_addrs) is required")

    msg = EmailMessage()
    msg["From"] = cfg.from_addr
    msg["To"] = ", ".join(cfg.to_addrs)
    msg["Subject"] = cfg.subject or "(no subject)"
    msg.set_content(cfg.body or "")

    context = ssl.create_default_context()

    if cfg.use_ssl:
        # Implicit SSL (e.g., port 465)
        with smtplib.SMTP_SSL(cfg.host, cfg.port, timeout=timeout, context=context) as server:
            if cfg.username and cfg.password:
                server.login(cfg.username, cfg.password)
            server.send_message(msg)
    else:
        # Plain SMTP with optional STARTTLS (e.g., port 587)
        with smtplib.SMTP(cfg.host, cfg.port, timeout=timeout) as server:
            server.ehlo()
            if cfg.use_tls:
                server.starttls(context=context)
                server.ehlo()
            if cfg.username and cfg.password:
                server.login(cfg.username, cfg.password)
            server.send_message(msg)
