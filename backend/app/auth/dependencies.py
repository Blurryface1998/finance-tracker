from fastapi import Depends, Cookie
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.exceptions import InvalidCredentialsError
from app.core.security import decode_access_token
from app.models.user import User


def get_current_user(
    access_token: str | None = Cookie(default=None), db: Session = Depends(get_db)
) -> User:
    if access_token is None:
        raise InvalidCredentialsError()

    payload = decode_access_token(access_token)

    user_id = payload.get("sub")
    if user_id is None:
        raise InvalidCredentialsError()

    user = db.query(User).filter(User.id == user_id).one_or_none()

    if user is None:
        raise InvalidCredentialsError()

    return user
