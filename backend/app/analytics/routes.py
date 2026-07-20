from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.analytics import schemas, services
from app.auth.dependencies import get_current_user
from app.core.database import get_db
from app.models import User

router = APIRouter(prefix="/analytics", tags=["Analytics"])


@router.get("/monthly", response_model=schemas.MonthlySummary)
def get_monthly_summary_route(
    month: Annotated[str, Query(pattern=r"\d{4}-\d{2}")],
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> schemas.MonthlySummary:
    """Return a monthly summary for income and expense."""
    return services.get_monthly_summary(db=db, month=month, current_user=current_user)


@router.get("/yearly", response_model=schemas.YearlySummary)
def get_yearly_summary_route(
    year: Annotated[str, Query(pattern=r"\d{4}")],
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> schemas.YearlySummary:
    """Return a yearly summary grouped by month."""
    return services.get_yearly_summary(db=db, year=year, current_user=current_user)


@router.get("/category", response_model=list[schemas.CategorySummary])
def get_category_summary_route(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
) -> list[schemas.CategorySummary]:
    "Retrun a summary of totals grouped by category."
    return services.get_category_summary(db=db, current_user=current_user)


@router.get("")
async def legacy_summary_route(
    month: Annotated[str | None, Query(pattern=r"\d{4}-\d{2}")] = None,
    year: Annotated[str | None, Query(pattern=r"\d{4}")] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> object:
    """Backward-compatible endpoint: /analytics?month=YYYY-MM or /analytics?year=YYYY

    Prefer the explicit `/monthly` and `/yearly` routes, but keep this for tests
    and older clients.
    """
    if month is not None:
        return services.get_monthly_summary(
            db=db, month=month, current_user=current_user
        )
    if year is not None:
        return services.get_yearly_summary(db=db, year=year, current_user=current_user)
    return []
