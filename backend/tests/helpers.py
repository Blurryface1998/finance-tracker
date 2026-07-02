def create_transaction(client, **overrides):
    data = {
        "description": "salary",
        "amount": "100.00",
        "category": "income",
        "transaction_type": "income",
    }
    data.update(overrides)
    return client.post("/transactions", json=data)
