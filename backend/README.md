# Finance Tracker Backend

This folder contains the backend API for the finance tracker project.

## Terminal commands

### Activate the virtual environment

From `finance-tracker/backend` run:

```bash
source ../.venv/bin/activate
```

If you prefer direct invocation, use:

```bash
/home/djordje/Desktop/pyton_project/finance-tracker/.venv/bin/python
```

### Start the API (if you have a FastAPI runner configured)

Use your preferred FastAPI startup command, for example:

```bash
uvicorn app.main:app --reload
```

### Format code

Run `isort` to sort imports:

```bash
isort app tests
isort .
```

Run `ruff` to lint and fix issues:

```bash
ruff check app tests
ruff check app tests --fix
ruff check . --fix
```

### Notes

- Keep this file focused on backend runtime and tooling commands.
- Use `backend/tests/README.md` for test-specific instructions.
