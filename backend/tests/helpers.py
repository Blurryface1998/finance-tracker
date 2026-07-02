"""Test helpers for generating transaction payloads and requests."""


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
    return client.post("/transactions", json=transaction_payload(**overrides))


def income_payload(**overides):
    """Build a payload for an income transaction."""
    return transaction_payload(transaction_type="income", category="income", **overides)


def expense_transaction(**overides):
    """Build a payload for an expense transaction."""
    return transaction_payload(
        transaction_type="expense", category="expense", **overides
    )
