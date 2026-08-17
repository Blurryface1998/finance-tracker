from datetime import UTC, datetime


def utc_now():
    """Return the current time in UTC."""
    return datetime.now(UTC)
