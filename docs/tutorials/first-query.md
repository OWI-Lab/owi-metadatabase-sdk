# Your first API query

!!! example

    In this tutorial you will connect to the OWI Metadatabase API, retrieve a list
    of project sites, and fetch the asset locations for one of those sites. By the
    end you will understand the basic request/response cycle that every other SDK
    call builds on.

## Prerequisites

- Python 3.9 or higher
- The SDK installed (`pip install owi-metadatabase`)
- An API token (contact OWI-Lab for access)

## Steps

### 1. Import the API clients

```python
from owi.metadatabase.geometry.io import GeometryAPI
from owi.metadatabase.locations.io import LocationsAPI
```

### 2. Create an authenticated client

Every API client requires credentials. The simplest method is token
authentication:

```python
TOKEN = "your-api-token-here"

locations_api = LocationsAPI(token=TOKEN)
geometry_api = GeometryAPI(token=TOKEN)
```

### 3. Retrieve project sites

The `get_projectsites()` method returns a dictionary with a `"data"` key
holding a Pandas DataFrame and an `"exists"` key indicating whether any
records matched:

```python
sites = locations_api.get_projectsites()

print(f"Records found: {sites['exists']}")
print(sites["data"].head())
```

### 4. Retrieve asset locations for a project

Pass the project site title to `get_assetlocations()`:

```python
assets = locations_api.get_assetlocations(projectsite="Nobelwind")

print(f"Found {len(assets['data'])} asset locations")
print(assets["data"][["title", "id"]].head())
```

### 5. Retrieve geometry model definitions

Switch to the geometry client to query structural data:

```python
models = geometry_api.get_model_definitions(projectsite="Nobelwind")

print(f"Model definitions found: {models['exists']}")
print(models["data"].head())
```

### 6. Putting it all together

```python
from owi.metadatabase.geometry.io import GeometryAPI
from owi.metadatabase.locations.io import LocationsAPI

TOKEN = "your-api-token-here"
PROJECT = "Nobelwind"

# Initialise clients
locations_api = LocationsAPI(token=TOKEN)
geometry_api = GeometryAPI(token=TOKEN)

# Locations
sites = locations_api.get_projectsites()
print(f"Available sites: {len(sites['data'])}")

assets = locations_api.get_assetlocations(projectsite=PROJECT)
print(f"Asset locations in {PROJECT}: {len(assets['data'])}")

# Geometry
models = geometry_api.get_model_definitions(projectsite=PROJECT)
print(f"Model definitions in {PROJECT}: {len(models['data'])}")
```

## What you learned

- How to create authenticated API clients with `LocationsAPI` and
  `GeometryAPI`
- That every SDK query method returns a `dict` with `"data"` (DataFrame)
  and `"exists"` (bool) keys
- How to list project sites, asset locations, and model definitions

## Next steps

- [Processing turbine geometry](processing-geometry.md) — learn how to
  assemble a full turbine model
- [How to filter data](../how-to/filter-data.md) — narrow results with
  Django-style keyword arguments
