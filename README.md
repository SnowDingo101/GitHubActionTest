# GitHubActionTest – Simple Email Sender

This repository contains a tiny Python script that sends a test email: "Hello, this is a test" to `EMoroney@foresightgroupau.com`.

It uses Python's built-in `smtplib` with environment variables for SMTP settings. A dry-run mode lets you preview without actually sending.

You can also bake default SMTP settings directly into `main.py` by editing these constants near the top of the file:

```
DEFAULT_SMTP_HOST = "smtp.office365.com"
DEFAULT_SMTP_PORT = 587
DEFAULT_SMTP_USERNAME = "you@yourdomain.com"
DEFAULT_SMTP_PASSWORD = "<avoid committing real secrets>"
DEFAULT_SMTP_FROM = "you@yourdomain.com"
DEFAULT_SMTP_USE_SSL = False
DEFAULT_SMTP_USE_TLS = True
```

Environment variables, if set, always override these defaults. If you leave `DEFAULT_SMTP_HOST` empty and don't set `SMTP_HOST`, the script will auto-switch to DRY_RUN and just print what it would do.

## Configure SMTP

Set the following environment variables before running:

- `SMTP_HOST` – SMTP server hostname (e.g., `smtp.office365.com` or `smtp.gmail.com`).
- `SMTP_PORT` – Port number. Common: `587` (STARTTLS) or `465` (SSL). Default: `587`.
- `SMTP_USERNAME` – SMTP username (often your email address).
- `SMTP_PASSWORD` – SMTP password. For Gmail/Office365, use an app password if required by your org.
- `SMTP_FROM` – From address. If omitted, falls back to `SMTP_USERNAME`.
- `SMTP_USE_SSL` – `true/false`. Use implicit SSL (port 465). Default: `false`.
- `SMTP_USE_TLS` – `true/false`. Use STARTTLS after connect (port 587). Default: `true` unless SSL is enabled.
- `DRY_RUN` – `true/false`. When true or when `SMTP_HOST` is missing, prints what would be sent instead of sending.

## Quick start (Windows PowerShell)

Dry run (no email sent):

```powershell
$env:DRY_RUN = "true"; python .\main.py
```

Send via Office 365 (example):

```powershell
$env:SMTP_HOST = "smtp.office365.com";
$env:SMTP_PORT = "587";
$env:SMTP_USERNAME = "you@yourdomain.com";
$env:SMTP_PASSWORD = "<app-or-mail-password>";
$env:SMTP_FROM = "you@yourdomain.com";
$env:SMTP_USE_TLS = "true";
python .\main.py
```

Send via Gmail (requires App Password if 2FA):

```powershell
$env:SMTP_HOST = "smtp.gmail.com";
$env:SMTP_PORT = "587";
$env:SMTP_USERNAME = "you@gmail.com";
$env:SMTP_PASSWORD = "<app-password>";
$env:SMTP_FROM = "you@gmail.com";
$env:SMTP_USE_TLS = "true";
python .\main.py
```

## Notes

- The script sends to a fixed recipient `EMoroney@foresightgroupau.com` with body "Hello, this is a test".
- If your provider requires SSL on port 465, set `SMTP_USE_SSL=true` and optionally `SMTP_USE_TLS=false`.
- Ensure your Python version meets `pyproject.toml` (>= 3.13) or run with a compatible interpreter.
- Do not commit real passwords to source control. Prefer environment variables, key vaults, or user secrets. The defaults are provided for convenience and local testing only.

## Excel Report Workflow

This project includes a complete automated Excel reporting workflow:

### Scripts:
1. **`update_excel.py`** - Adds timestamp, random number, and status to `data_report.xlsx`
2. **`email_excel_contents.py`** - Reads the Excel file and emails a formatted report

### Local testing:
```powershell
# Install dependencies
pip install openpyxl

# Update Excel file
python update_excel.py

# Send report (dry run)
$env:DRY_RUN = "true"
python email_excel_contents.py
```

### Automated workflow:
`.github/workflows/excel-workflow.yml` runs daily at 4am Sydney time and:
1. Updates the Excel file with new data
2. Commits the updated file to the repository
3. Emails the report contents to `EMoroney@foresightgroupau.com`

The workflow requires the same Gmail secrets as the email workflow.

This project also includes `timestamp_logger.py`, which appends the current UTC timestamp to `timestamps.log`.

Run locally:

```powershell
python .\timestamp_logger.py
Get-Content .\timestamps.log
```

### Automated runs with GitHub Actions

A workflow at `.github/workflows/timestamp.yml` runs every 5 minutes and commits the updated `timestamps.log` back to the repository using the default `GITHUB_TOKEN` with `contents: write` permissions.

Notes:
- The workflow is also manually triggerable via the "Run workflow" button.
- Commits are skipped when there are no changes.
- The workflow adds `[skip ci]` to the commit message to prevent re-trigger loops if you have other CI.

### About email files

The email functionality is now available! Set up GitHub secrets to enable automated email sending via GitHub Actions:

1. Go to your repo → Settings → Secrets and variables → Actions
2. Add these repository secrets:
   - `GMAIL_USERNAME`: Your Gmail address (e.g., you@gmail.com)
   - `GMAIL_APP_PASSWORD`: Your Gmail app password (not your regular password)

The email workflow at `.github/workflows/email.yml` runs daily at 4am Sydney time and sends "Hello, this is a test" to `EMoroney@foresightgroupau.com`.
