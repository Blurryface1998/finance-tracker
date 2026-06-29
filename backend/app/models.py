from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Numeric, Integer, DateTime
from decimal import Decimal
from app.database import Base
from datetime import datetime

class Transaction(Base):
    """SQLAlchemy model representing a financial transaction."""

    __tablename__ = "transactions"

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    description: Mapped[str] = mapped_column(String(50))
    category: Mapped[str] = mapped_column(String(50))

    amount: Mapped[Decimal] = mapped_column(Numeric(10,2))

    type: Mapped[str] = mapped_column(String(10))