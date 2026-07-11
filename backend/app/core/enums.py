from enum import Enum


class TransactionType(str, Enum):
    """Validate that the amount is greater than 0."""

    income = "income"
    expense = "expense"
