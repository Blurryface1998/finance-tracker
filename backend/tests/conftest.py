"""Test configuration and fixtures for the finance tracker backend."""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import StaticPool, create_engine
from sqlalchemy.orm import sessionmaker

from app.core.database import Base, get_db
from app.main import app
from app.models.user import User

TEST_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    TEST_DATABASE_URL, connect_args={"check_same_thread": False}, poolclass=StaticPool
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Create tables once
@pytest.fixture(scope="session", autouse=True)
def setup_database():
    """Create the test database schema once for the test session."""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def auth_headers(client):

    client.post(
        "/auth/register",
        json={
            "username": "john_doe",
            "email": "john_doe@example.com",
            "password": "Mypassword1234567",
        },
    )
    response = client.post(
        "/auth/login",
        json={"email": "john_doe@example.com", "password": "Mypassword1234567"},
    )
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def authenticated_client(client, auth_headers):
    client.headers = auth_headers
    return client


@pytest.fixture
def test_user(db):
    user = User(
        username="john_doe", email="john_doe@example.com", password_hash="fake_hash"
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


@pytest.fixture(autouse=True)
def reset_db():
    """Reset the in-memory database schema between test cases."""
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


# Dependency override (ONLY DB CONTROL POINT)
def override_get_db():
    """Provide a test database session for endpoint dependency injection."""
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.rollback()
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture
def db():
    """Provides a database session for tests."""
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.rollback()
        db.close()


# Test client
@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c
