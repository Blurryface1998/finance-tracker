from pydantic import EmailStr
from sqlalchemy.orm import Session

from app.core.exceptions import InvalidCredentialsError, UserAlreadyExistsError
from app.core.security import hash_password, verify_password
from app.models.user import User

from . import schemas


def _get_user_by_email(db: Session, email: EmailStr) -> User | None:
    return db.query(User).filter(User.email == email).one_or_none()


def create_user(db: Session, user_data: schemas.UserCreate) -> User:
    # Check if email exists, if it exists then raise exception
    existing_user = _get_user_by_email(db=db, email=user_data.email)

    if existing_user:
        raise UserAlreadyExistsError()

    # hash password
    hashed_password = hash_password(user_data.password)
    # create user
    user = User(
        username=user_data.username,
        email=user_data.email,
        password_hash=hashed_password,
    )
    # save to database

    db.add(user)
    db.commit()
    db.refresh(user)

    # return user
    return user


def authenticate_user(db: Session, login_data: schemas.LoginRequest) -> User:
    existing_user = _get_user_by_email(db=db, email=login_data.email)

    if not existing_user:
        raise InvalidCredentialsError()

    is_password_valid = verify_password(
        login_data.password, existing_user.password_hash
    )

    if not is_password_valid:
        raise InvalidCredentialsError()

    return existing_user
