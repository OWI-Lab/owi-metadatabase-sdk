# Doctest Style Guide

All public functions should include executable doctest examples.

## Requirements

- Include 2 to 3 examples per public function
- Cover basic usage and edge cases
- Use `# doctest: +SKIP` for live API calls
- Prefer simple, deterministic output

## Template

```
def function_name(param1: int, param2: str) -> bool:
    """
    Short description.

    Parameters
    ----------
    param1 : int
        Description of param1.
    param2 : str
        Description of param2.

    Returns
    -------
    bool
        Description of return value.

    Examples
    --------
    Basic usage:

    >>> function_name(1, "ok")
    True

    Edge case:

    >>> function_name(0, "")
    False
    """
```

## Output Handling

Use these doctest flags when needed:

- `+ELLIPSIS` for long output
- `+NORMALIZE_WHITESPACE` for whitespace differences
- `+IGNORE_EXCEPTION_DETAIL` for platform-specific messages

## Fixtures

Common fixtures are injected into doctests via `tests/conftest.py`.
Use them to avoid repeating large test data.
