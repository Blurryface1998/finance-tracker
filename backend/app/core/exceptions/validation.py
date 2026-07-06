from decimal import Decimal

from app.core.exceptions.base import AppException


class InvalidTransactionAmountError(AppException):
    def __init__(self, amount: Decimal) -> None:
        super().__init__(
            message=f"Invalid transaction amount: {amount}",
            status_code=400,
            error_code="invalid_transaction_amount",
        )


class InvalidCurrencyError(AppException):
    def __init__(self, currency: str) -> None:
        super().__init__(
            message=f"Unsupported currency: {currency}",
            status_code=400,
            error_code="invalid_currency",
        )


class InvalidCursorError(AppException):
    def __init__(self, cursor: str) -> None:
        super().__init__(
            message=f"Invalid cursor: {cursor}",
            status_code=422,
            error_code="invalid_cursor",
        )


class InvalidYearError(AppException):
    def __init__(self, year: str) -> None:
        super().__init__(
            message=f"Year '{year}' is outside the supported range (2001-2099).",
            status_code=422,
            error_code="invalid_year",
        )


class InvalidMonthError(AppException):
    def __init__(self, month: str) -> None:
        super().__init__(
            message=f"Month '{month}' is outside the supported range (01-12)",
            status_code=422,
            error_code="invalid_year",
        )
