from sqlalchemy import tuple_
from sqlalchemy.orm import Session

from app.core.exceptions import DatabaseError, TransactionNotFoundError
from app.core.logging import logger
from app.models import Transaction
from app.transactions import schemas
from app.utils.cursor import encode_cursor


def _get_transaction(db: Session, transaction_id: int) -> Transaction:
    """Return a transaction by ID or raise a not-found exception."""
    transaction = db.get(Transaction, transaction_id)

    if not transaction:
        raise TransactionNotFoundError(transaction_id)
    return transaction


def create_transaction(db: Session, data: schemas.TransactionCreate) -> Transaction:
    """Create and save a new transaction.

    Args:
        db: SQLAlchemy session instance.
        data: Validated transaction payload.

    Returns:
        The saved Transaction instance.
    """
    logger.info(
        "Creating transaction: category=%s amount=%s type=%s",
        data.category,
        data.amount,
        data.transaction_type,
    )
    transaction = Transaction(
        description=data.description,
        amount=data.amount,
        categor=data.category,
        transaction_type=data.transaction_type,
    )

    try:
        db.add(transaction)
        db.commit()
        db.refresh(transaction)
    except Exception:
        logger.exception("Failed to create transaction")
        raise DatabaseError("Database Error")

    logger.info("Transaction created successfully: id=%s", transaction.id)
    return transaction


def get_transactions(
    db: Session,
    limit: int = 20,
    cursor: schemas.PaginationCursor | None = None,
    filters: schemas.TransactionFilter | None = None,
) -> schemas.PaginatedResponse[schemas.TransactionResponse]:
    """Retrieve transactions with optional filters and cursor-based pagination.

    Args:
        db: SQLAlchemy session instance.
        limit: Maximum number of transactions to return per page.
        cursor: Pagination cursor identifying the last record from the previous page.
        filters: Optional filters to apply to the transaction query.

    Returns:
        A paginated response containing the transactions and pagination metadata.
    """
    logger.info(
        "Fetching transactions: limit=%s cursor=%s filters=%s",
        limit,
        cursor is not None,
        filters,
    )

    query = db.query(Transaction).order_by(
        Transaction.created_at.desc(), Transaction.id.desc()
    )

    filters = filters or schemas.TransactionFilter()

    if filters.transaction_type:
        query = query.filter(Transaction.transaction_type == filters.transaction_type)

    if filters.category is not None:
        query = query.filter(Transaction.category.ilike(f"%{filters.category}%"))
    if filters.min_amount:
        query = query.filter(Transaction.amount >= filters.min_amount)
    if filters.max_amount is not None:
        query = query.filter(Transaction.amount <= filters.max_amount)

    if cursor:
        query = query.filter(
            tuple_(Transaction.created_at, Transaction.id)
            < (cursor.created_at, cursor.cursor_id)
        )
    rows = query.limit(limit + 1).all()

    has_next = len(rows) > limit
    items = rows[:limit]

    last = items[-1] if items else None

    next_cursor = (
        schemas.PaginationCursor(created_at=last.created_at, cursor_id=last.id)
        if has_next and last
        else None
    )

    logger.info(
        "Returned %s transactions with has_next=%s",
        len(items),
        has_next,
    )

    return schemas.PaginatedResponse(
        items=items,
        next_cursor=encode_cursor(next_cursor) if next_cursor else None,
        has_next=has_next,
    )


def get_transaction(db: Session, transaction_id: int) -> Transaction:
    """Retrieve a single transaction by ID.

    Args:
        db: SQLAlchemy session instance.
        transaction_id: Primary key of the transaction.

    Returns:
        The Transaction instance.

    Raises:
        TransactionNotFoundError: If the transaction does not exist.
    """
    logger.info("Fetching transaction: id=%s", transaction_id)
    return _get_transaction(db, transaction_id)


def update_transaction(
    db: Session, transaction_id: int, data: schemas.TransactionUpdate
) -> Transaction | None:
    """Update an existing transaction.

    Args:
        db: SQLAlchemy session instance.
        transaction_id: Primary key of the transaction.
        data: Validated transaction update payload.

    Returns:
        The updated Transaction instance, or None if not found.
    """
    logger.info("Updating transaction: id=%s", transaction_id)
    transaction = _get_transaction(db, transaction_id)

    transaction.description = data.description
    transaction.amount = data.amount
    transaction.category = data.category
    transaction.transaction_type = data.transaction_type

    db.commit()
    db.refresh(transaction)

    return transaction


def delete_transaction(db: Session, transaction_id: int) -> None:
    """Delete a transaction by ID and persist the change.

    Args:
        db: SQLAlchemy session instance.
        transaction_id: Primary key of the transaction.
    """
    logger.info("Deleting transaction: id=%s", transaction_id)
    transaction = _get_transaction(db, transaction_id)

    db.delete(transaction)
    db.commit()
    logger.info("Transaction deleted successfully: id=%s", transaction_id)


def patch_transaction(
    db: Session, transaction_id: int, data: schemas.TransactionPatch
) -> Transaction | None:
    """Apply partial updates to an existing transaction.

    Args:
        db: SQLAlchemy session instance.
        transaction_id: Primary key of the transaction to modify.
        data: Partial transaction payload containing only the fields to update.

    Returns:
        The updated Transaction instance, or None if not found.
    """
    logger.info("Patching transaction: id=%s", transaction_id)
    transaction = _get_transaction(db, transaction_id)

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
