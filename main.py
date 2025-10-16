import os
from typing import List

from email_sender import EmailConfig, send_email_smtp

# --- Built-in SMTP defaults (edit these to bake config into the script) ---
# Leave any value empty to keep it optional and safer by default.
DEFAULT_SMTP_HOST = ""  # e.g., "smtp.office365.com" or "smtp.gmail.com"
DEFAULT_SMTP_PORT = 587  # 587 for STARTTLS, 465 for SSL
DEFAULT_SMTP_USERNAME = ""  # e.g., "you@yourdomain.com"
DEFAULT_SMTP_PASSWORD = ""  # WARNING: committing real passwords to git is unsafe
DEFAULT_SMTP_FROM = ""      # if empty, falls back to DEFAULT_SMTP_USERNAME (or SMTP_USERNAME)
DEFAULT_SMTP_USE_SSL = False
DEFAULT_SMTP_USE_TLS = True  # typically True when not using SSL


def env(name: str, default: str | None = None) -> str | None:
    return os.environ.get(name, default)


def parse_bool(value: str | None, default: bool = False) -> bool:
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def main():
    # Target recipient and message per user request
    to_email = "EMoroney@foresightgroupau.com"
    subject = "Test Email"
    body = "Hello, this is a test"

    # SMTP configuration from environment variables
    smtp_host = env("SMTP_HOST") or DEFAULT_SMTP_HOST or ""
    smtp_port = int(env("SMTP_PORT") or DEFAULT_SMTP_PORT)
    smtp_user = env("SMTP_USERNAME") or DEFAULT_SMTP_USERNAME or None
    smtp_pass = env("SMTP_PASSWORD") or DEFAULT_SMTP_PASSWORD or None
    from_addr = env("SMTP_FROM") or (DEFAULT_SMTP_FROM or smtp_user or "")
    use_ssl = parse_bool(env("SMTP_USE_SSL"), DEFAULT_SMTP_USE_SSL)
    use_tls = parse_bool(env("SMTP_USE_TLS"), DEFAULT_SMTP_USE_TLS if not use_ssl else False)
    dry_run = parse_bool(env("DRY_RUN"), False)

    cfg = EmailConfig(
        host=smtp_host,
        port=smtp_port,
        username=smtp_user,
        password=smtp_pass,
        use_tls=use_tls,
        use_ssl=use_ssl,
        from_addr=from_addr,
        to_addrs=[to_email],
        subject=subject,
        body=body,
    )

    if dry_run or not smtp_host:
        print("[DRY RUN] Email would be sent with the following settings:")
        print(f"From: {cfg.from_addr}")
        print(f"To: {', '.join(cfg.to_addrs)}")
        print(f"Subject: {cfg.subject}")
        print(f"SMTP: host={cfg.host} port={cfg.port} use_tls={cfg.use_tls} use_ssl={cfg.use_ssl}")
        print("Body:")
        print(cfg.body)
        if not smtp_host:
            print("Note: Set SMTP_HOST to actually send the email.")
        return

    # Send the email
    try:
        send_email_smtp(cfg)
        print("Email sent successfully.")
    except Exception as e:
        # Provide a readable error
        print(f"Failed to send email: {e}")


if __name__ == "__main__":
    main()
