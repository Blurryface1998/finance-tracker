"""Test helpers for generating transaction payloads and requests."""

TRANSACTIONS_URL = "/transactions"


def transaction_payload(**overides):
    """Build a default transaction payload and apply any overrides."""
    base = {
        "description": "salary",
        "amount": "100.00",
        "category": "income",
        "transaction_type": "income",
    }
    base.update(overides)
    return base


def create_transaction(client, **overrides):
    """Send a create transaction request through the test client."""
    return client.post(TRANSACTIONS_URL, json=transaction_payload(**overrides))


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


def expense_transaction(**overides):
    """Build a payload for an expense transaction."""
    return transaction_payload(
        transaction_type="expense", category="expense", **overides
    )
