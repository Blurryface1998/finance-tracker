# Finance Tracker

A full-stack personal finance application for managing transactions, tracking income and expenses, and analyzing financial activity over time.

The application is built with a React frontend and a FastAPI backend, with a focus on modular architecture, secure authentication, data ownership, and a responsive user interface.

## Features

- User registration and authentication
- Secure password hashing with Argon2
- Cookie-based authentication
- Transaction creation, editing, deletion, and listing
- Transaction filtering by type, category, and amount range
- Cursor-based transaction pagination
- User-owned transaction access control
- Monthly and yearly financial summaries
- Responsive dashboard interface
- Reusable React components
- Backend automated tests

## Tech Stack

### Backend

- Python
- FastAPI
- SQLAlchemy
- Pydantic
- SQLite
- Alembic
- JWT
- Argon2
- Pytest

### Frontend

- React
- Vite
- React Router
- Axios
- React Hook Form
- SCSS
- ESLint

## Architecture

The project is separated into two main applications:

```text
finance-tracker/
├── backend/
│   ├── app/
│   │   ├── analytics/
│   │   ├── auth/
│   │   ├── core/
│   │   ├── models/
│   │   └── transactions/
│   ├── alembic/
│   ├── tests/
│   ├── requirements.txt
│   └── README.md
│
├── frontend/
│   ├── src/
│   │   ├── app/
│   │   ├── features/
│   │   ├── services/
│   │   ├── shared/
│   │   └── styles/
│   ├── public/
│   ├── package.json
│   └── README.md
│
├── .gitignore
└── README.md
```

The backend exposes the API used by the React frontend. Authentication, authorization, transaction management, and financial calculations are handled by the backend, while the frontend is responsible for routing, user interaction, and presentation.

## Local Setup

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd finance-tracker
```

### 2. Backend

```bash
cd backend

python3 -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt
```

Create a `.env` file inside `backend/`:

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

### 3. Frontend

In another terminal:

```bash
cd frontend

npm install
npm run dev
```

The frontend will be available at:

```text
http://localhost:5173
```

## Testing

Backend tests are written with Pytest.

Run the test suite from the backend directory:

```bash
pytest
```

## Development

The application is being developed incrementally, with the backend API and frontend interface evolving together.

Database schema changes are managed with Alembic migrations, and the backend includes unit and integration tests for core functionality.

## Learning & Development

This project was developed as a hands-on learning process. **ChatGPT was used as a learning and development aid** throughout the project to help research concepts, explain unfamiliar technologies, troubleshoot implementation issues, review approaches, and explore alternative solutions.

The implementation, project structure, decisions, and integration of the resulting code were developed as part of the project's development process.
