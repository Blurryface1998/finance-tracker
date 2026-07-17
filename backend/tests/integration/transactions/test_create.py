"""Create transaction integration tests."""

from tests.helpers import TRANSACTIONS_URL, create_transaction


def test_create(authenticated_client):
    """Verify creating a transaction returns HTTP 201 and the transaction is listed."""
    response = create_transaction(client=authenticated_client, amount="200.00")

    assert response.status_code == 201

    data = authenticated_client.get(TRANSACTIONS_URL).json()

    assert len(data["items"]) == 1
    assert data["items"][0]["amount"] == "200.00"


def test_create_amount_zero_fails(authenticated_client):
    """Verify zero amounts are rejected with validation errors."""
    response = create_transaction(authenticated_client, amount="0")

    assert response.status_code == 422


def test_create_negative_amount_fails(authenticated_client):
    """Verify negative amounts are rejected with validation errors."""
    response = create_transaction(authenticated_client, amount="-100")

    assert response.status_code == 422


def test_create_empty_description_fails(authenticated_client):
    """Verify empty descriptions are rejected with validation errors."""
    response = create_transaction(authenticated_client, description="")

    assert response.status_code == 422


def test_create_invalid_type_fails(authenticated_client):
    """Verify invalid transaction types are rejected with validation errors."""
    response = create_transaction(authenticated_client, transaction_type="invalid")

    assert response.status_code == 422


def test_create_transaction_type_non_string_fails(authenticated_client):
    """Ensure non-string transaction type values are rejected."""
    response = create_transaction(authenticated_client, transaction_type=123)

    assert response.status_code == 422


def test_create_invalid_description_length_fails(authenticated_client):
    """Ensure overly long descriptions are rejected."""
    response = create_transaction(authenticated_client, description="a" * 51)

    assert response.status_code == 422


def test_create_invalid_category_length_fails(authenticated_client):
    """Ensure overly long categories are rejected."""
    response = create_transaction(authenticated_client, category="b" * 51)

    assert response.status_code == 422


def test_create_whitespace_only_description_fails(authenticated_client):
    """Ensure whitespace-only descriptions are rejected."""
    response = create_transaction(authenticated_client, description="   ")

    assert response.status_code == 422


def test_create_whitespace_only_category_fails(authenticated_client):
    """Ensure whitespace-only categories are rejected."""
    response = create_transaction(authenticated_client, category="   ")

    assert response.status_code == 422


def test_create_normalization(authenticated_client):
    """Ensure create requests normalize text fields properly."""
    response = create_transaction(
        authenticated_client, description="  salary payment  ", category="  income  "
    )

    data = response.json()

    assert data["description"] == "Salary Payment"
    assert data["category"] == "Income"


def test_create_accepts_integer_amount(authenticated_client):
    """Ensure integer amounts are accepted and formatted as decimals."""
    response = create_transaction(authenticated_client, amount=100)

    assert response.status_code == 201
    assert response.json()["amount"] == "100.00"


def test_create_keeps_decimal_precision(authenticated_client):
    """Ensure decimal precision is preserved during creation."""
    response = create_transaction(authenticated_client, amount="100.5")

    assert response.json()["amount"] == "100.50"


def test_create_missing_fields_fails(authenticated_client):
    """Ensure missing required fields are rejected."""
    response = authenticated_client.post(TRANSACTIONS_URL, json={})

    assert response.status_code == 422


def test_multiple_create(authenticated_client):
    """Verify multiple transactions are created and returned in descending order."""
    create_transaction(authenticated_client, amount="100.00")
    create_transaction(authenticated_client, amount="200.00")
    create_transaction(authenticated_client, amount="300.00")

    data = authenticated_client.get(TRANSACTIONS_URL).json()

    assert len(data["items"]) == 3

    amounts = [item["amount"] for item in data["items"]]

    assert amounts == ["300.00", "200.00", "100.00"]


def test_multiple_create_ids_unique(authenticated_client):
    """Ensure each created transaction receives a unique ID."""
    create_transaction(authenticated_client, amount="100.00")
    create_transaction(authenticated_client, amount="200.00")
    create_transaction(authenticated_client, amount="300.00")

    data = authenticated_client.get(TRANSACTIONS_URL).json()
    ids = [item["id"] for item in data["items"]]

    assert len(ids) == len(set(ids))


def test_multiple_create_fields_present(authenticated_client):
    """Ensure created transactions include the expected response fields."""
    create_transaction(authenticated_client, amount="100.00")

    data = authenticated_client.get(TRANSACTIONS_URL).json()
    item = data["items"][0]

    required_fields = {
        "id",
        "description",
        "amount",
        "category",
        "transaction_type",
        "created_at",
    }

    assert required_fields.issubset(item.keys())


def test_multiple_create_decimal_formats(authenticated_client):
    """Ensure different numeric formats are normalized consistently."""
    create_transaction(authenticated_client, amount="100")
    create_transaction(authenticated_client, amount="200.5")

    data = authenticated_client.get(TRANSACTIONS_URL).json()
    amounts = [item["amount"] for item in data["items"]]

    assert "100.00" in amounts
    assert "200.50" in amounts


def test_multiple_create_many_items(authenticated_client):
    """Ensure many transactions can be created and returned together."""
    for i in range(20):
        create_transaction(authenticated_client, amount=str(i + 1))

    data = authenticated_client.get(f"{TRANSACTIONS_URL}?limit=50").json()

    assert len(data["items"]) == 20
