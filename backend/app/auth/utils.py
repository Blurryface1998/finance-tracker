import re

MIN_PASSWORD_LENGTH = 16
MAX_PASSWORD_LENGTH = 128


def validate_username(value: str) -> str:
    value = value.strip().lower()

    if len(value) < 3 or len(value) > 50:
        raise ValueError("Username must be between 3 and 50")

    if not re.match(r"^[a-z0-9_]+$", value):
        raise ValueError("Username can only contain letters, numbers, and underscores")
    return value


def validate_email(value: str) -> str:
    return value.strip().lower()


def validate_password(value: str) -> str:
    if not value.strip():
        raise ValueError("Password cannot be empty")

    if len(value) < MIN_PASSWORD_LENGTH or len(value) > MAX_PASSWORD_LENGTH:
        raise ValueError(
            f"password must be between {MIN_PASSWORD_LENGTH} and {MAX_PASSWORD_LENGTH}"
        )
    return value
