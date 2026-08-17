"""SQLAlchemy model definitions for financial transactions."""

from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, Enum, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.core.enums import TransactionType
from app.models.utils import utc_now

if TYPE_CHECKING:
    from app.models import User


class Transaction(Base):
    """SQLAlchemy model representing a financial transaction."""

    __tablename__ = "transactions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utc_now)

    description: Mapped[str] = mapped_column(String(50))
    category: Mapped[str] = mapped_column(String(50), index=True)
    amount: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    transaction_type: Mapped[TransactionType] = mapped_column(
        Enum(TransactionType), index=True
    )
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    user: Mapped["User"] = relationship(back_populates="transactions")
