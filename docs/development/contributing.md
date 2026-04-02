# Contributing

## Setup

```bash
git clone https://github.com/OWI-Lab/owi-metadatabase-sdk.git
cd owi-metadatabase-sdk
uv sync --dev
```

## Quality checks

```bash
uv run invoke qa
```

This runs `ruff format`, `ruff check`, and `ty check`.

## Tests

```bash
uv run invoke test
```

This runs pytest with doctests and coverage.

## Pull requests

- Keep changes focused and well-scoped
- Add or update tests for behaviour changes
- Update documentation when behaviour changes
- Follow the existing code style (120-char lines, NumPy docstrings)
