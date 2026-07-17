"""Test helpers for generating transaction payloads and requests."""

from app.models import Transaction
from app.models import User

TRANSACTIONS_URL = "/transactions"
SUMMARY_URL = "/analytics"
AUTHENTICATION_URL = "/auth"


def transaction_payload(**overrides):
    """Build a default transaction payload and apply any overrides."""
    base = {
        "description": "salary",
        "amount": "100.00",
        "category": "income",
        "transaction_type": "income",
    }
    base.update(overrides)
    return base


def user_payload(**overrides):
    """Build a default registration payload and apply any overrides."""
    base = {
        "username": "john_doe",
        "email": "john_doe@example.com",
        "password": "Mypassword1234567",
    }
    base.update(overrides)
    return base


def user_login_payload(**overrides):
    """Build a default login payload and apply any overrides."""
    base = {
        "email": "john_doe@example.com",
        "password": "Mypassword1234567",
    }
    base.update(overrides)
    return base


def create_transaction(client, headers=None, db=None, created_at=None, **overrides):
    """Send a create transaction request through the test client."""
    payload_overrides = {k: v for k, v in overrides.items() if k != "created_at"}

    response = client.post(
        TRANSACTIONS_URL,
        json=transaction_payload(**payload_overrides),
        headers=headers,
    )

    if created_at is not None and db is None:
        raise ValueError("db is required when created_at is provided")

    if db is not None and created_at is not None:
        transaction_id = response.json()["id"]

        transaction = db.get(Transaction, transaction_id)
        transaction.created_at = created_at

        db.commit()
        db.refresh(transaction)

    return response


def create_user(client, db=None, **overrides):
    """Register a user through the auth endpoint for tests.

    Uses the default registration payload and applies any overrides.
    If a database session is provided, the created user is refreshed from the DB.
    """
    payload = user_payload(**overrides)
    response = client.post(f"{AUTHENTICATION_URL}/register", json=payload)

    if db is not None and response.status_code == 201:
        user = db.query(User).filter(User.email == payload["email"]).one()
        db.refresh(user)

    return response


def login_user(client, **overrides):
    """Log in a test user through the auth login endpoint."""
    return client.post(
        f"{AUTHENTICATION_URL}/login", json=user_login_payload(**overrides)
    )


def create_transaction_json(client, **overrides):
    """Create a transaction and return its JSON payload directly."""
    return create_transaction(client=client, **overrides).json()


def transactions_url(transaction_id: int | str | None = None):
    """Build the transaction endpoint URL, optionally with a transaction id."""
    if transaction_id is None:
        return TRANSACTIONS_URL
    return f"{TRANSACTIONS_URL}/{transaction_id}"


def income_payload(**overides):
    """Build a payload for an income transaction."""
    return transaction_payload(transaction_type="income", category="income", **overides)


def expense_payload(**overides):
    """Build a payload for an expense transaction."""
    return transaction_payload(
        transaction_type="expense", category="expense", **overides
    )
