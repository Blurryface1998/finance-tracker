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
