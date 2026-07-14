from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.analytics import schemas, services
from app.core.database import get_db

router = APIRouter(prefix="/analytics", tags=["Analytics"])


@router.get("/monthly", response_model=schemas.MonthlySummary)
async def get_monthly_summary_route(
    month: Annotated[str, Query(pattern=r"\d{4}-\d{2}")], db: Session = Depends(get_db)
) -> schemas.MonthlySummary:
    """Return a monthly summary for income and expense."""
    return services.get_monthly_summary(db=db, month=month)


@router.get("/yearly", response_model=schemas.YearlySummary)
async def get_yearly_summary_route(
    year: Annotated[str, Query(pattern=r"\d{4}")], db: Session = Depends(get_db)
) -> schemas.YearlySummary:
    """Return a yearly summary grouped by month."""
    return services.get_yearly_summary(db=db, year=year)


@router.get("/category", response_model=list[schemas.CategorySummary])
async def get_category_summary_route(
    db: Session = Depends(get_db),
) -> list[schemas.CategorySummary]:
    "Retrun a summary of totals grouped by category."
    return services.get_category_summary(db=db)


@router.get("")
async def legacy_summary_route(
    month: Annotated[str | None, Query(pattern=r"\d{4}-\d{2}")] = None,
    year: Annotated[str | None, Query(pattern=r"\d{4}")] = None,
    db: Session = Depends(get_db),
) -> object:
    """Backward-compatible endpoint: /analytics?month=YYYY-MM or /analytics?year=YYYY

    Prefer the explicit `/monthly` and `/yearly` routes, but keep this for tests
    and older clients.
    """
    if month is not None:
        return services.get_monthly_summary(db=db, month=month)
    if year is not None:
        return services.get_yearly_summary(db=db, year=year)
    return []
