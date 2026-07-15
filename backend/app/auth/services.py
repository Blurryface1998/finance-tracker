from sqlalchemy.orm import Session

from app.models.user import User

from . import schemas


def create_user(db: Session, user_data: schemas.UserCreate) -> User:
    pass
