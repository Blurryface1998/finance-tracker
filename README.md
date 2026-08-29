# Finance Tracker

A full-stack personal finance application for managing transactions, tracking income and expenses, and analyzing financial activity over time.

The application uses a React frontend and a FastAPI backend, with a focus on modular architecture, secure authentication, data ownership, and responsive UI.

## Features

- User registration and authentication
- Secure password hashing with Argon2
- Cookie-based authentication
- Transaction creation, editing, deletion, and listing
- Transaction filtering by type, category, and amount range
- Cursor-based pagination
- User-owned transaction access control
- Monthly and yearly financial summaries
- Responsive dashboard interface
- Reusable React components
- Automated backend tests

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

The application is divided into two main parts.

The **FastAPI backend** provides the REST API and handles authentication, authorization, transaction management, database operations, and financial calculations.

The **React frontend** handles application routing, user interaction, API integration, and presentation.

## Testing

The backend includes unit and integration tests covering authentication, transactions, filtering, pagination, summaries, and data ownership.

## Development

Database schema changes are managed with Alembic migrations.

The backend and frontend are developed together, with the frontend consuming the REST API provided by the backend.

## Learning & Development

This project was developed as a hands-on learning process. ChatGPT was used as a learning and development aid to research concepts, explain unfamiliar technologies, troubleshoot implementation issues, review approaches, and explore alternative solutions.

The implementation and technical decisions were developed throughout the project, with ChatGPT serving as a supplementary tool for learning and problem-solving.
