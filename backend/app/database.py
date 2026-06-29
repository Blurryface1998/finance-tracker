from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

# SqLite database file
DATABASE_URL = "sqlite:///./finance.db"


# Engine = connection to DB
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} # needed for SqLite
)

# Session factory used to create database sessions
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

class Base(DeclarativeBase):
    """Base class for SQLAlchemy ORM models."""
    pass


def get_db():
    """Yield a database session and ensure the session is closed after use."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()