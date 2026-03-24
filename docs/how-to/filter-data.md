# How to filter data with Django-style parameters

The OWI Metadatabase backend is built with Django. All SDK query methods
accept additional keyword arguments that are forwarded as Django-style
query filters.

## Basic filtering

Pass extra keyword arguments to any `get_*` method:

```python
from owi.metadatabase.locations.io import LocationsAPI

api = LocationsAPI(token="your-token")

# Only asset locations whose title contains "BB"
assets = api.get_assetlocations(
    projectsite="Nobelwind",
    title__icontains="BB",
)
```

## Common filter lookups

| Lookup | Meaning | Example |
|--------|---------|---------|
| `__exact` | Exact match (default) | `title__exact="BBB01"` |
| `__icontains` | Case-insensitive contains | `title__icontains="bb"` |
| `__startswith` | Starts with | `title__startswith="BB"` |
| `__gt` / `__lt` | Greater / less than | `id__gt=100` |

## Combining filters

Multiple keyword arguments are combined with AND logic:

```python
assets = api.get_assetlocations(
    projectsite="Nobelwind",
    title__startswith="BB",
    id__gt=50,
)
```

## Using filters with geometry queries

The same pattern works on geometry endpoints:

```python
from owi.metadatabase.geometry.io import GeometryAPI

geo_api = GeometryAPI(token="your-token")

subs = geo_api.get_subassemblies(
    projectsite="Nobelwind",
    subassembly_type="TW",  # Tower sub-assemblies only
)
```

!!! note
    The available filter fields depend on the backend Django model.
    Refer to the [Geometry query examples](../reference/query-examples/geometry.md)
    and [Locations query examples](../reference/query-examples/locations.md)
    for the complete filter paths.
