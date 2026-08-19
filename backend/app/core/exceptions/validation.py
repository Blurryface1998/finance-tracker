"""Validation-related application exceptions for request payloads."""

from decimal import Decimal

from app.core.exceptions.base import AppException


class InvalidTransactionAmountError(AppException):
    """Raised when a transaction amount is zero or negative."""

    def __init__(self, amount: Decimal) -> None:
        """Create an error response for an invalid amount value."""
        super().__init__(
            message=f"Invalid transaction amount: {amount}",
            status_code=400,
            error_code="invalid_transaction_amount",
        )


class InvalidCurrencyError(AppException):
    """Raised when the provided currency is not supported."""

    def __init__(self, currency: str) -> None:
        """Create an error response for an unsupported currency value."""
        super().__init__(
            message=f"Unsupported currency: {currency}",
            status_code=400,
            error_code="invalid_currency",
        )


class InvalidCursorError(AppException):
    """Raised when a pagination cursor cannot be decoded."""

    def __init__(self, cursor: str) -> None:
        """Create an error response for an invalid or malformed cursor."""
        super().__init__(
            message=f"Invalid cursor: {cursor}",
            status_code=422,
            error_code="invalid_cursor",
        )


class InvalidYearError(AppException):
    """Raised when a year is outside the supported range."""

    def __init__(self, year: str) -> None:
        """Create an error response for an unsupported year value."""
        super().__init__(
            message=f"Year '{year}' is outside the supported range (2001-2099).",
            status_code=422,
            error_code="invalid_year",
        )


class InvalidMonthError(AppException):
    """Raised when a month value is outside the supported range."""

    def __init__(self, month: str) -> None:
        """Create an error response for an unsupported month value."""
        super().__init__(
            message=f"Month '{month}' is outside the supported range (01-12)",
            status_code=422,
            error_code="invalid_month",
        )
