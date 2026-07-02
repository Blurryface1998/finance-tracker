from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import Generic, TypeVar

from pydantic import BaseModel, ConfigDict, field_validator, model_validator

ResponseItem = TypeVar("ResponseItem")


class TransactionType(str, Enum):
    """Supported transaction categories used by the API."""

    income = "income"
    expense = "expense"


class TransactionBase(BaseModel):
    """Base schema for transaction data shared across request and response models."""

    description: str
    amount: Decimal
    category: str

    @field_validator("description", "category", mode="before")
    @classmethod
    def normalize_text(cls, value: str) -> str:
        """Normalize text values for description and category."""
        value = value.strip()

        if len(value) < 1 or len(value) > 50:
            raise ValueError("Must be between 1 and 50")

        return value.title()

    @field_validator("amount")
    @classmethod
    def validate_amount(cls, value: Decimal) -> Decimal:
        "Validate that the amount is greater than 0"
        if value <= 0:
            raise ValueError("Amount must be more than 0")
        return value


class TransactionCreate(TransactionBase):
    """Schema for creating a new transaction."""

    transaction_type: TransactionType


class TransactionResponse(TransactionBase):
    """Schema returned by the API for transaction records."""

    id: int
    transaction_type: TransactionType
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class TransactionUpdate(TransactionBase):
    """Schema used to update an existing transaction."""

    transaction_type: TransactionType


class TransactionPatch(BaseModel):
    """Schema for partial transaction updates."""

    description: str | None = None
    amount: Decimal | None = None
    category: str | None = None
    transaction_type: TransactionType | None = None


class TransactionFilter(BaseModel):
    """Schema for filters for transactions."""

    transaction_type: TransactionType | None = None
    category: str | None = None
    min_amount: Decimal | None = None
    max_amount: Decimal | None = None


class CategorySummary(BaseModel):
    """Schema for reporting category totals."""

    category: str
    total: Decimal


class MonthlySummary(BaseModel):
    """Schema for monthly income, expense, and balance summary data."""

    month: int
    income: Decimal
    expense: Decimal
    balance: Decimal


class YearlySummary(BaseModel):
    """Shema for yearly income by months"""

    year: int
    months: list[MonthlySummary]


class PaginationCursor(BaseModel):
    created_at: datetime
    id: int

    @model_validator(mode="after")
    def validate_cursor(self):
        if self.created_at is None or self.id is None:
            raise ValueError("Invalid pagination cursor: cursor must not be empty")
        return self


class PaginationResult(BaseModel, Generic[ResponseItem]):
    items: list[ResponseItem]
    next_cursor: PaginationCursor | None
    has_next: bool


class PaginatedResponse(BaseModel, Generic[ResponseItem]):
    """Generic paginated response payload for list endpoints."""

    items: list[ResponseItem]
    next_cursor: str | None
    has_next: bool

    model_config = ConfigDict(from_attributes=True)
