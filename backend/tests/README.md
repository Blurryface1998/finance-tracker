# Backend Tests

This folder contains tests for the backend API.

## Run tests

From `finance-tracker/backend`:

```bash
pytest
```

Or use the project Python directly:

```bash
/home/djordje/Desktop/pyton_project/finance-tracker/.venv/bin/python -m pytest
```

## Run a single test file

```bash
pytest tests/integration/transactions/test_create.py
pytest tests/integration/transactions/test_list.py
pytest tests/integration/pagination/test_pagination.py
pytest tests/integration/filters/test_filters.py
pytest tests/integration/summary/test_summary.py
```

## Run one test function only

```bash
pytest tests/integration/transactions/test_create.py::test_create_invalid_description_length_fails
```

## Run one test directory

```bash
pytest tests/integration/transactions
pytest tests/integration/summary
pytest tests/integration/pagination
pytest tests/integration/filters
```

## Helpful options

- `-q` : quiet output
- `-v` : verbose output
- `-k "keyword"` : run tests that match a keyword

Example:

```bash
pytest -q tests/integration/transactions/test_list.py -k "combined_filters"
```

## Tips

- Run smaller test sets when developing to get faster feedback.
- Use `pytest -k` when you want to focus on a specific scenario.
- If a test fails, rerun only that file or function.
