from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.exceptions import InvalidCredentialsError
from app.core.security import decode_access_token
from app.models.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
) -> User:
    payload = decode_access_token(token)

    user_id = payload.get("sub")
    if user_id is None:
        raise InvalidCredentialsError()

    user = db.query(User).filter(User.id == user_id).one_or_none()

    if user is None:
        raise InvalidCredentialsError()

    return user
