# How to authenticate with the API

All API clients require credentials. The SDK supports two authentication
methods.

## Token authentication (recommended)

Pass your API token when creating a client:

```python
from owi.metadatabase.geometry.io import GeometryAPI

api = GeometryAPI(token="your-api-token")
```

You can also pass a pre-built header dictionary:

```python
api = GeometryAPI(header={"Authorization": "Token your-api-token"})
```

## Username and password authentication

```python
api = GeometryAPI(uname="your-username", password="your-password")
```

## Store credentials securely

Avoid hard-coding tokens in source files. Use environment variables instead:

```python
import os
from owi.metadatabase.geometry.io import GeometryAPI

TOKEN = os.environ["OWI_API_TOKEN"]
api = GeometryAPI(token=TOKEN)
```

!!! warning
    Never commit real API tokens to version control.
