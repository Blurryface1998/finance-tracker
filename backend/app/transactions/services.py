from sqlalchemy import tuple_
from sqlalchemy.orm import Session

from app.core.exceptions import (DatabaseError, InvalidCursorError,
                                 TransactionNotFoundError)
from app.core.logging import logger
from app.models import Transaction, User
from app.transactions import schemas
from app.utils.cursor import decode_cursor, encode_cursor


def _get_user_transaction(
    db: Session, transaction_id: int, current_user: User
) -> Transaction:
    """Return a transaction by ID or raise a not-found exception."""
    transaction = (
        db.query(Transaction)
        .filter(
            Transaction.id == transaction_id, Transaction.user_id == current_user.id
        )
        .one_or_none()
    )

    if not transaction:
        raise TransactionNotFoundError(transaction_id)
    return transaction


def create_transaction(
    db: Session, data: schemas.TransactionCreate, current_user: User
) -> Transaction:
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
        category=data.category,
        transaction_type=data.transaction_type,
        user_id=current_user.id,
    )

    try:
        db.add(transaction)
        db.commit()
        db.refresh(transaction)
    except Exception as exc:
        logger.exception("Failed to create transaction")
        raise DatabaseError() from exc

    logger.info("Transaction created successfully: id=%s", transaction.id)
    return transaction


def get_transactions(
    db: Session,
    current_user: User,
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
    # Decode cursor only when provided
    if cursor is not None:
        try:
            cursor = decode_cursor(cursor)
        except ValueError as exc:
            raise InvalidCursorError(cursor) from exc

    logger.info(
        "Fetching transactions: user_id=%s limit=%s cursor=%s filters=%s",
        current_user.id,
        limit,
        cursor is not None,
        filters,
    )

    query = (
        db.query(Transaction)
        .filter(Transaction.user_id == current_user.id)
        .order_by(Transaction.created_at.desc(), Transaction.id.desc())
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


def get_transaction(
    db: Session, transaction_id: int, current_user: User
) -> Transaction:
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
    return _get_user_transaction(
        db=db, transaction_id=transaction_id, current_user=current_user
    )


def update_transaction(
    db: Session,
    transaction_id: int,
    data: schemas.TransactionUpdate,
    current_user: User,
) -> Transaction:
    """Update an existing transaction.

    Args:
        db: SQLAlchemy session instance.
        transaction_id: Primary key of the transaction.
        data: Validated transaction update payload.

    Returns:
        The updated Transaction instance, or None if not found.
    """
    logger.info("Updating transaction: id=%s", transaction_id)
    transaction = _get_user_transaction(
        db=db, transaction_id=transaction_id, current_user=current_user
    )

    transaction.description = data.description
    transaction.amount = data.amount
    transaction.category = data.category
    transaction.transaction_type = data.transaction_type

    db.commit()
    db.refresh(transaction)

    return transaction


def delete_transaction(db: Session, transaction_id: int, current_user: User) -> None:
    """Delete a transaction by ID and persist the change.

    Args:
        db: SQLAlchemy session instance.
        transaction_id: Primary key of the transaction.
    """
    logger.info("Deleting transaction: id=%s", transaction_id)
    transaction = _get_user_transaction(db, transaction_id, current_user=current_user)

    db.delete(transaction)
    db.commit()
    logger.info(
        "Transaction deleted successfully: id=%s user_id=%s",
        transaction_id,
        current_user.id,
    )


def patch_transaction(
    db: Session,
    transaction_id: int,
    data: schemas.TransactionPatch,
    current_user: User,
) -> Transaction:
    """Apply partial updates to an existing transaction.

    Args:
        db: SQLAlchemy session instance.
        transaction_id: Primary key of the transaction to modify.
        data: Partial transaction payload containing only the fields to update.

    Returns:
        The updated Transaction instance, or None if not found.
    """
    logger.info("Patching transaction: id=%s", transaction_id)
    transaction = _get_user_transaction(db, transaction_id, current_user=current_user)

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
