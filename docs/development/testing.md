# Testing

This project uses pytest for unit tests and doctest for docstring
examples.

## Run Tests

```
uv run pytest
```

## Run Doctests

```
uv run pytest --doctest-modules src/
```

## Coverage

```
uv run pytest --cov=src/owi/metadatabase --cov-report=term-missing
```
