from decimal import Decimal

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.core.database import get_db
from app.models.user import User
from app.transactions import schemas, services

router = APIRouter(prefix="/transactions", tags=["Transactions"])


@router.get("", response_model=schemas.PaginatedResponse[schemas.TransactionResponse])
def get_transactions_route(
    transaction_type: schemas.TransactionType | None = None,
    category: str | None = None,
    min_amount: Decimal | None = None,
    max_amount: Decimal | None = None,
    limit: int = Query(20, ge=1, le=50),
    cursor: str | None = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> schemas.PaginatedResponse[schemas.TransactionResponse]:
    """Return paginated transaction with optional filters and cursor-based paging."""
    filters = schemas.TransactionFilter(
        transaction_type=transaction_type,
        category=category,
        min_amount=min_amount,
        max_amount=max_amount,
    )

    return services.get_transactions(
        db=db, limit=limit, cursor=cursor, filters=filters, current_user=current_user
    )


@router.get(
    "/{transaction_id}",
    response_model=schemas.TransactionResponse,
    status_code=status.HTTP_200_OK,
)
def get_transaction_route(
    transaction_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> schemas.TransactionResponse:
    """Return a single transaction by ID."""
    return services.get_transaction(
        db=db, transaction_id=transaction_id, current_user=current_user
    )


@router.post(
    "", response_model=schemas.TransactionResponse, status_code=status.HTTP_201_CREATED
)
def create_transaction_route(
    transaction: schemas.TransactionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> schemas.TransactionResponse:
    "Create a new transaction."
    return services.create_transaction(
        db=db, data=transaction, current_user=current_user
    )


@router.put(
    "/{transaction_id}",
    response_model=schemas.TransactionResponse,
    status_code=status.HTTP_200_OK,
)
def update_transaction_response(
    transaction_id: int,
    transaction: schemas.TransactionUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> schemas.TransactionResponse:
    """Update an existing transaction by ID."""
    return services.update_transaction(
        db=db,
        transaction_id=transaction_id,
        data=transaction,
        current_user=current_user,
    )


@router.patch(
    "/{transaction_id}",
    response_model=schemas.TransactionResponse,
    status_code=status.HTTP_200_OK,
)
def patch_transaction_route(
    transaction_id: int,
    transaction: schemas.TransactionPatch,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> schemas.TransactionResponse:
    """Apply a partial update to a transaction."""
    return services.patch_transaction(
        db=db,
        transaction_id=transaction_id,
        data=transaction,
        current_user=current_user,
    )


@router.delete("/{transaction_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_transaction_route(
    transaction_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Delete an existing transaction by ID."""
    return services.delete_transaction(
        db=db, transaction_id=transaction_id, current_user=current_user
    )
