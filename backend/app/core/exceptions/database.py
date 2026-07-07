"""Database-related application exceptions."""

from app.core.exceptions.base import AppException


class DatabaseError(AppException):
    """Raised when a database operation fails."""

    def __init__(self) -> None:
        """Create a standard database failure response payload."""
        super().__init__(
            message="A database error occurred",
            status_code=500,
            error_code="database_error",
        )
