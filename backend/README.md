# Finance Tracker Backend

The backend API for Finance Tracker, built with FastAPI and SQLAlchemy.

## Overview

The API provides authenticated endpoints for:

- User registration and authentication
- Transaction CRUD operations
- Transaction filtering
- Cursor-based pagination
- Monthly and yearly financial summaries
- User-owned data access control

## Tech Stack

- Python
- FastAPI
- SQLAlchemy
- Pydantic
- SQLite
- Alembic
- JWT
- Argon2
- Pytest

## Structure

```text
backend/
├── app/
│   ├── analytics/
│   ├── auth/
│   ├── core/
│   ├── models/
│   └── transactions/
├── alembic/
├── tests/
├── requirements.txt
└── pytest.ini
```

### Main Components

**Auth**

Handles registration, authentication, password hashing, token creation, and authenticated request dependencies.

**Transactions**

Provides transaction creation, retrieval, updating, deletion, filtering, pagination, and ownership enforcement.

**Analytics**

Provides aggregated financial data and monthly/yearly summaries.

**Core**

Contains application configuration, database setup, security utilities, exceptions, logging, and shared enums.

**Tests**

Contains unit and integration tests covering authentication, transactions, filtering, pagination, summaries, and ownership.

## Local Setup

From the backend directory:

```bash
python3 -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt
```

Create a `.env` file:

```env
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

Start the development server:

```bash
uvicorn app.main:app --reload
```

The API will be available at:

```text
http://localhost:8000
```

## Testing

Run the test suite:

```bash
pytest
```

## Database

SQLite is currently used for local persistence.

Database schema changes are managed with Alembic migrations.

## Development

The backend is developed incrementally alongside the React frontend, with automated tests used to validate core application behavior.
