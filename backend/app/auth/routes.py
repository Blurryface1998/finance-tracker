from fastapi import APIRouter, Depends, status, Response
from sqlalchemy.orm import Session

from app.auth import schemas, services, dependencies
from app.models import User
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
    "/login", status_code=status.HTTP_200_OK, response_model=schemas.LoginResponse
)
def login_user_route(
    data: schemas.LoginRequest, response: Response, db: Session = Depends(get_db)
) -> schemas.LoginResponse:
    user = services.authenticate_user(db=db, login_data=data)
    access_token = create_access_token({"sub": str(user.id)})
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=False,
        samesite="lax",
    )
    return schemas.LoginResponse(
        message="Login successful",
    )


@router.get("/me", status_code=status.HTTP_200_OK, response_model=schemas.UserResponse)
def get_current_user_route(curret_user: User = Depends(dependencies.get_current_user)):
    return curret_user
