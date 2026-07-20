from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.auth import schemas, services
from app.core.database import get_db
from app.core.security import create_access_token

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.UserResponse,
)
def register_user_route(
    data: schemas.UserCreate,
    db: Session = Depends(get_db),
) -> schemas.UserResponse:
    user = services.create_user(db=db, user_data=data)
    return user


@router.post(
    "/login", status_code=status.HTTP_200_OK, response_model=schemas.TokenResponse
)
def login_user_route(
    data: schemas.LoginRequest, db: Session = Depends(get_db)
) -> schemas.TokenResponse:
    user = services.authenticate_user(db=db, login_data=data)
    access_token = create_access_token({"sub": str(user.id)})
    return schemas.TokenResponse(
        access_token=access_token,
        token_type="bearer",
    )
