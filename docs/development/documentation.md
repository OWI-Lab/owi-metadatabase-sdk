# Documentation

Documentation is built with [Zensical](https://zensical.dev/) and
configured in `zensical.toml`. API reference pages are auto-generated
from NumPy-style docstrings via mkdocstrings.

## Build

```bash
uv run invoke docs.build
```

## Serve locally

```bash
uv run invoke docs.serve
```

The server is available at `http://localhost:8001/owi-metadatabase-sdk/`.

## Structure

The documentation follows the [Diátaxis](https://diataxis.fr/) framework:

| Section | Purpose | Directory |
|---------|---------|-----------|
| Tutorials | Learning-oriented lessons | `docs/tutorials/` |
| How-to guides | Problem-oriented recipes | `docs/how-to/` |
| Reference | Information-oriented descriptions | `docs/reference/` |
| Explanation | Understanding-oriented discussions | `docs/explanation/` |
