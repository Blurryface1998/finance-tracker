MIN_PASSWORD_LENGTH = 16
MAX_PASSWORD_LENGTH = 128


def validate_name(value: str, max_length: int) -> str:

    value = " ".join(value.split())

    if len(value) < 1 or len(value) > max_length:
        raise ValueError(f"Name must be between 1 and {max_length}")

    if not all((char.isalpha() or char in " -'") for char in value):
        raise ValueError(
            "Name can only contain letters, spaces, hyphens, and apostrophes"
        )

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
