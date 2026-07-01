from sqlalchemy import or_, and_
from typing import TypeVar, Callable
from app.schemas import PaginationCursor, PaginationResult

ModelType = TypeVar("ModelType")


def apply_cursor_filter(query, cursor, order_spec):
    conditions = []

    for field in order_spec.fields:
        column = getattr(Transaction, field.name)
        value = cursor.values(field.name)

        if field.direction == "desc":
            conditions.append(column < value)
        else:
            conditions.append(column > value)
    return query.filter(or_(*conditions))


def paginate(
    query,
    limit: int,
    cursor,
    order_spec,
    apply_cursor_filter,
    build_cursor,
) -> PaginationResult[ModelType]:
    """Generic keyset pagination engine"""
    if cursor:
        query = apply_cursor_filter(query, cursor, order_spec)

    rows = query.limit(limit + 1).all()

    items = rows[:limit]
    has_next = len(rows) > limit

    last_item = items[-1] if items else None

    next_cursor = build_cursor(last_item) if has_next and last_item else None

    return PaginationResult(
        items=items,
        next_cursor=next_cursor,
        has_next=has_next,
    )
