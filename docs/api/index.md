# API Reference

Complete API documentation for owi-metadatabase.

## Modules

The owi-metadatabase package provides the following modules:

### [Geometry](geometry.md)
Tools for working with offshore wind turbine geometry data.

- `GeometryAPI` - API client for geometry data
- `OWT` - Single turbine geometry processor
- `OWTs` - Multiple turbine geometry processor

### [Locations](locations.md)
Tools for working with offshore wind site location data.

- `LocationsAPI` - API client for location/site data

### [I/O](io.md)
Low-level I/O utilities for API communication.

- `RequestData` - Base class for API requests

### [Utilities](utils.md)
Internal utilities and exceptions.

- Exception classes
- Helper functions

## Auto-Generated Documentation

This section provides automatically generated API documentation
extracted from docstrings using mkdocstrings.

## Quick Links

| Module | Description | Key Classes |
|--------|-------------|-------------|
| [geometry.io](geometry.md) | Geometry API client | `GeometryAPI` |
| [geometry.processing](geometry.md) | Geometry data processing | `OWT`, `OWTs` |
| [geometry.structures](geometry.md) | Geometry data structures | Various dataclasses |
| [locations.io](locations.md) | Locations API client | `LocationsAPI` |
| [io](io.md) | Base I/O utilities | `RequestData` |
| [_utils](utils.md) | Internal utilities | Exception classes |

## Usage Examples

### Geometry API

```python
from owi.metadatabase.geometry.io import GeometryAPI

api = GeometryAPI(api_root="https://api.example.com")
turbine_data = api.get_turbine_data(turbine_id="OWT001")
```

### Locations API

```python
from owi.metadatabase.locations.io import LocationsAPI

api = LocationsAPI(api_root="https://api.example.com")
location_data = api.get_location_data(project_id="PRJ001")
```

## Type Hints

All public APIs include complete type hints for improved IDE support
and static analysis:

```python
from owi.metadatabase.geometry.processing import OWT
from pandas import DataFrame

def process_turbine(data: DataFrame) -> OWT:
    """Process turbine geometry data."""
    return OWT(data)
```

## Documentation Style

All docstrings follow the NumPy documentation style:

```python
def function(arg1: int, arg2: str) -> bool:
    """
    Short description.

    Longer description with more details about what the
    function does and how to use it.

    Parameters
    ----------
    arg1 : int
        Description of arg1.
    arg2 : str
        Description of arg2.

    Returns
    -------
    bool
        Description of return value.

    Examples
    --------
    >>> function(42, "test")
    True
    """
    return True
```
