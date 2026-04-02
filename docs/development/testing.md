# Testing

This project uses pytest for unit tests and doctests for docstring
examples.

## Run all tests

```bash
uv run invoke test
```

## Run only unit tests

```bash
uv run pytest tests/
```

## Run only doctests

```bash
uv run pytest --doctest-modules src/
```

## Coverage report

```bash
uv run pytest --cov=src/owi/metadatabase --cov-report=term-missing
```

The HTML coverage report is written to `htmlcov/`.
