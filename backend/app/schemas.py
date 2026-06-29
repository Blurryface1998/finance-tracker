from pydantic import BaseModel, field_validator
from decimal import Decimal
from typing import Literal

class TransactionBase(BaseModel):
    """Base schema for transaction data shared across request and response models."""

    description: str
    amount: Decimal
    category: str

    @field_validator('description', 'category', mode='before')
    @classmethod
    def clean_text(cls, value: str) -> str:
        """Normalize text values for description and category."""
        value = value.strip()

        if len(value) < 1 or len(value) > 50:
            raise ValueError("Must be between 1 and 50")
        
        return value.title()

    @field_validator('amount')
    @classmethod
    def validate(cls, value: Decimal) -> Decimal:
        "Normalize decimal value for amount"
        if value <= 0:
            raise ValueError("Amount must be more than 0")
        return value

class TransactionCreate(TransactionBase):
    """Schema for creating a new transaction."""

    type: Literal["income", "expense"]
    

class TransactionResponse(TransactionBase):
    """Schema returned by the API for transaction records."""

    id: int
    type: str


class TransactionUpdate(TransactionBase):
    """Schema used to update an existing transaction."""

    type: Literal["income", "expenses"]


class CategorySummary(BaseModel):
    """Schema for reporting category totals."""

    category: str
    total: Decimal