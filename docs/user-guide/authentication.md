# API Authentication

The SDK supports API key authentication via the `API_key` argument.

## Basic Usage

- Pass `API_key` when creating an API client
- Store the key securely in your environment or secrets manager

## Example

Initialize a client with an API key:

```
from owi.metadatabase.geometry.io import GeometryAPI

api = GeometryAPI(API_key="your-api-key")
```

## Notes

- Do not hardcode real keys in source control
- Use `# doctest: +SKIP` for examples that require live API access
