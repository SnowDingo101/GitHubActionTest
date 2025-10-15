from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path


LOG_FILE = Path("timestamps.log")


def append_timestamp() -> str:
    """Append an ISO 8601 UTC timestamp to the log file and return the line written."""
    ts = datetime.now(timezone.utc).isoformat()
    line = ts + "\n"
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    with LOG_FILE.open("a", encoding="utf-8") as f:
        f.write(line)
    return line.strip()


def main() -> None:
    written = append_timestamp()
    print(f"Appended timestamp: {written}")


if __name__ == "__main__":
    main()
