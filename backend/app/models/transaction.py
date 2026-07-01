from sqlalchemy import DateTime, Enum, Integer, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base
from datetime import UTC, datetime
from decimal import Decimal
from app.schemas import TransactionType


class Transaction(Base):
    """SQLAlchemy model representing a financial transaction."""

    __tablename__ = "transactions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(UTC))

    description: Mapped[str] = mapped_column(String(50))
    category: Mapped[str] = mapped_column(String(50), index=True)
    amount: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    transaction_type: Mapped[TransactionType] = mapped_column(
        Enum(TransactionType), index=True
    )
