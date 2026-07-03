"""Summary-related transaction integration tests."""

from datetime import datetime

from tests.helpers import SUMMARY_URL, create_transaction


def test_monthly_summary_income_only(client):
    """Verify monthly summary returns total income for the requested month."""
    create_transaction(client, amount="100")
    create_transaction(client, amount="200")

    response = client.get(f"{SUMMARY_URL}?month=2026-07")

    assert response.status_code == 200

    data = response.json()

    assert data["income"] == "300.00"
    assert data["expense"] == "0.00"
    assert data["balance"] == "300.00"


def test_monthly_expense_only(client):
    create_transaction(client, amount="150.00", transaction_type="expense")
    create_transaction(client, amount="50.00", transaction_type="expense")

    response = client.get(f"{SUMMARY_URL}?month=2026-07")

    assert response.status_code == 200

    data = response.json()

    assert data["income"] == "0.00"
    assert data["expense"] == "200.00"
    assert data["balance"] == "-200.00"


def test_monthly_summary_income_and_expenses(client):
    create_transaction(client, amount=2000, transaction_type="income")
    create_transaction(client, amount=500, transaction_type="expense")

    response = client.get(f"{SUMMARY_URL}?month=2026-07")

    assert response.status_code == 200

    data = response.json()

    assert data["income"] == "2000.00"
    assert data["expense"] == "500.00"
    assert data["balance"] == "1500.00"


def test_monthly_summary_empty(client):
    response = client.get(f"{SUMMARY_URL}?month=2026-07")
    data = response.json()

    assert response.status_code == 200

    expected_keys = {"income", "expense", "balance"}
    assert expected_keys.issubset(data.keys())

    assert data["month"] == 7


def test_summary_ignores_other_months(client, db):
    create_transaction(client, amount="1000")

    create_transaction(client, db=db, amount="500", created_at=datetime(2026, 6, 15))

    response = client.get(f"{SUMMARY_URL}?month=2026-07")

    data = response.json()

    assert data["income"] == "1000.00"


def test_summary_decimal_precision(client):
    create_transaction(client, amount="10.25")
    create_transaction(client, amount="20.75")

    response = client.get(f"{SUMMARY_URL}?month=2026-07")

    data = response.json()

    assert data["income"] == "31.00"


def test_invalid_month_format(client):
    response = client.get(f"{SUMMARY_URL}?month=2026/07")

    assert response.status_code == 422

    response = client.get(f"{SUMMARY_URL}?month=abc")

    assert response.status_code == 422

    response = client.get(f"{SUMMARY_URL}?month=2026-07")

    assert response.status_code == 200


def test_yearly_summary(client):
    """Verify yearly summary includes the expected income for the current month."""
    response = client.get(f"{SUMMARY_URL}/yearly?year=2026")
    data = response.json()

    assert response.status_code == 200

    assert data["year"] == 2026
    assert len(data["months"]) == 12

    for month in data["months"]:
        assert month["income"] == "0.00"
        assert month["expense"] == "0.00"
        assert month["balance"] == "0.00"


def test_yearly_summary_single_transaction(client):
    create_transaction(client, amount="1000", created_at=datetime(2026, 7, 10))

    response = client.get(f"{SUMMARY_URL}/yearly?year=2026")
    data = response.json()

    july = next(month_data for month_data in data["months"] if month_data["month"] == 7)

    assert july["income"] == "1000.00"
    assert july["expense"] == "0.00"
    assert july["balance"] == "1000.00"


def test_yearly_summary_multiple_months(client):
    create_transaction(client, amount="1000", created_at=datetime(2026, 6, 10))
    create_transaction(client, amount="500", created_at=datetime(2026, 7, 10))

    response = client.get(f"{SUMMARY_URL}/yearly?year=2026")
    data = response.json()

    june = next(month_data for month_data in data["months"] if month_data["month"] == 6)
    july = next(month_data for month_data in data["months"] if month_data["month"] == 7)

    print(
        create_transaction(
            client, amount="1000", created_at=datetime(2026, 6, 10)
        ).json()
    )

    assert june["income"] == "1000.00"
    assert july["income"] == "500.00"


def test_yearly_summary_ignores_other_years(client):
    create_transaction(client, amount="1000", created_at=datetime(2025, 7, 10))
    create_transaction(client, amount="500", created_at=datetime(2026, 7, 10))

    response = client.get(f"{SUMMARY_URL}/yearly?year=2026")
    data = response.json()

    july = next(month_data for month_data in data["months"] if month_data["month"] == 7)
    assert july["income"] == "500.00"


def test_yearly_summary_invalid_year(client):
    response = client.get(f"{SUMMARY_URL}/yearly?year=20xx")

    assert response.status_code == 422


def test_category_summary(client):
    create_transaction(client, amount="100.00", category="Food")
    create_transaction(client, amount="50.00", category="Food")
    create_transaction(client, amount="1000.00", category="Salary")

    response = client.get(f"{SUMMARY_URL}/category")

    assert response.status_code == 200

    data = response.json()

    food = next(item for item in data if item["category"] == "Food")
    salary = next(item for item in data if item["category"] == "Salary")

    assert food["total"] == "150.00"
    assert salary["total"] == "1000.00"


def test_category_summary_empty(client):
    response = client.get(f"{SUMMARY_URL}/category")

    assert response.status_code == 200
    assert response.json() == []


def test_category_summary_multiple_transactions_same_category(client):
    create_transaction(client, amount="25.00", category="Food")
    create_transaction(client, amount="75.00", category="Food")
    create_transaction(client, amount="100.00", category="Food")

    response = client.get(f"{SUMMARY_URL}/category")

    data = response.json()

    food = next(item for item in data if item["category"] == "Food")

    assert food["total"] == "200.00"


def test_category_summary_nomralization(client):
    create_transaction(client, amount="100.00", category="food")
    create_transaction(client, amount="50.00", category="  FOOD  ")

    response = client.get(f"{SUMMARY_URL}/category")

    data = response.json()

    food = next(item for item in data if item["category"] == "Food")

    assert food["total"] == "150.00"


def test_category_summary_decimal_precision(client):
    create_transaction(client, amount="10.25", category="Food")
    create_transaction(client, amount="20.75", category="Food")

    response = client.get(f"{SUMMARY_URL}/category")

    data = response.json()

    food = next(item for item in data if item["category"] == "Food")

    assert food["total"] == "31.00"
