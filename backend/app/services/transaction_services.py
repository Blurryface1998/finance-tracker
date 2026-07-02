"""Transaction service operations for CRUD, filtering, and pagination."""

from sqlalchemy.orm import Session
from sqlalchemy import tuple_

from app.models import Transaction
from app.schemas import (
    PaginatedResponse,
    PaginationCursor,
    TransactionCreate,
    TransactionFilter,
    TransactionPatch,
    TransactionResponse,
    TransactionUpdate,
)
from app.utils.cursor import encode_cursor


# Helper function
def _get_transaction(db: Session, transaction_id: int) -> Transaction | None:
    """Return a transaction by ID, or None if it does not exist."""
    return db.get(Transaction, transaction_id)


def create_transaction(db: Session, data: TransactionCreate) -> Transaction:
    """Create and save a new transaction.

    Args:
        db: SQLAlchemy session instance.
        data: Validated transaction payload.

    Returns:
        The saved Transaction instance.
    """
    transaction = Transaction(
        description=data.description,
        amount=data.amount,
        category=data.category,
        transaction_type=data.transaction_type,
    )
    db.add(transaction)
    db.commit()
    db.refresh(transaction)

    return transaction


def get_transactions(
    db: Session,
    limit: int = 20,
    cursor: PaginationCursor | None = None,
    filters: TransactionFilter | None = None,
) -> PaginatedResponse[TransactionResponse]:
    """Retrieve transactions with optional filters and cursor-based pagination.

    Args:
        db: SQLAlchemy session instance.
        limit: Maximum number of transactions to return per page.
        cursor: Pagination cursor identifying the last record from the previous page.
        filters: Optional filters to apply to the transaction query.

    Returns:
        A paginated response containing the transactions and pagination metadata.
    """

    query = db.query(Transaction).order_by(
        Transaction.created_at.desc(), Transaction.id.desc()
    )

    filters = filters or TransactionFilter()

    if filters.transaction_type:
        query = query.filter(Transaction.transaction_type == filters.transaction_type)

    if filters.category:
        query = query.filter(Transaction.category.ilike(f"%{filters.category}%"))

    if filters.min_amount is not None:
        query = query.filter(Transaction.amount >= filters.min_amount)

    if filters.max_amount is not None:
        query = query.filter(Transaction.amount <= filters.max_amount)

    if cursor:
        # Use SQLAlchemy's tuple_ construct for composite column comparison
        query = query.filter(
            tuple_(Transaction.created_at, Transaction.id)
            < (cursor.created_at, cursor.id)
        )
    rows = query.limit(limit + 1).all()

    has_next = len(rows) > limit
    items = rows[:limit]

    last = items[-1] if items else None

    next_cursor = (
        PaginationCursor(created_at=last.created_at, id=last.id)
        if has_next and last
        else None
    )

    return PaginatedResponse(
        items=items,
        next_cursor=encode_cursor(next_cursor) if next_cursor else None,
        has_next=has_next,
    )


def get_transaction(db: Session, transaction_id: int) -> Transaction | None:
    """Retrieve a single transaction by ID.

    Args:
        db: SQLAlchemy session instance.
        transaction_id: Primary key of the transaction.

    Returns:
        The Transaction instance, or None if not found.
    """
    return db.get(Transaction, transaction_id)


def update_transaction(
    db: Session, transaction_id: int, data: TransactionUpdate
) -> Transaction | None:
    """Update an existing transaction.

    Args:
        db: SQLAlchemy session instance.
        transaction_id: Primary key of the transaction.
        data: Validated transaction update payload.

    Returns:
        The updated Transaction instance, or None if not found.
    """
    transaction = _get_transaction(db, transaction_id)

    if not transaction:
        return None

    transaction.description = data.description
    transaction.amount = data.amount
    transaction.category = data.category
    transaction.transaction_type = data.transaction_type

    db.commit()
    db.refresh(transaction)

    return transaction


def delete_transaction(db: Session, transaction_id: int) -> Transaction | None:
    """Delete a transaction by ID.

    Args:
        db: SQLAlchemy session instance.
        transaction_id: Primary key of the transaction.

    Returns:
        The deleted Transaction instance, or None if not found.
    """
    transaction = _get_transaction(db, transaction_id)

    if not transaction:
        return None

    db.delete(transaction)
    db.commit()

    return transaction


def patch_transaction(
    db: Session, transaction_id: int, data: TransactionPatch
) -> Transaction | None:
    """Apply partial updates to an existing transaction.

    Args:
        db: SQLAlchemy session instance.
        transaction_id: Primary key of the transaction to modify.
        data: Partial transaction payload containing only the fields to update.

    Returns:
        The updated Transaction instance, or None if not found.
    """
    transaction = _get_transaction(db, transaction_id)

    if not transaction:
        return None

    if data.description is not None:
        transaction.description = data.description.strip().title()
    if data.amount is not None:
        transaction.amount = data.amount
    if data.category is not None:
        transaction.category = data.category.strip().title()
    if data.transaction_type is not None:
        transaction.transaction_type = data.transaction_type

    db.commit()
    db.refresh(transaction)

    return transaction
