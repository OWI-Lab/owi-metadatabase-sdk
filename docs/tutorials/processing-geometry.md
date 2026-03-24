# Processing turbine geometry

!!! example
    In this tutorial you will retrieve raw geometry data from the API and use
    the processing classes to assemble a complete offshore wind turbine (OWT)
    model. You will then inspect its structural components (tower, transition
    piece, monopile) and plot the result.

## Prerequisites

- Completed [Your first API query](first-query.md)
- A valid API token

## Steps

### 1. Initialise the geometry API

```python
from owi.metadatabase.geometry.io import GeometryAPI

TOKEN = "your-api-token-here"
PROJECT = "Nobelwind"

api = GeometryAPI(token=TOKEN)
```

### 2. Create an OWT processor

The `get_owt_geometry_processor()` method returns an `OWT` object
pre-loaded with data for a single turbine:

```python
owt = api.get_owt_geometry_processor(
    projectsite=PROJECT,
    assetlocation="BBB01",
)
```

### 3. Process the structure

Before accessing derived attributes you must call `process_structure()`.
This step resolves sub-assemblies and building blocks into coherent
component tables:

```python
owt.process_structure()
```

### 4. Inspect the components

After processing, the `OWT` object exposes DataFrames for each structural
component:

```python
# Tower geometry
print(owt.tower.head())

# Transition piece geometry
print(owt.tp.head())

# Monopile geometry
print(owt.mp.head())

# RNA (Rotor-Nacelle Assembly) data
print(owt.rna)
```

### 5. Process multiple turbines

Use `OWTs` to handle a batch of turbines in a single call:

```python
from owi.metadatabase.geometry.processing import OWTs
from owi.metadatabase.locations.io import LocationsAPI

loc_api = LocationsAPI(token=TOKEN)
assets = loc_api.get_assetlocations(projectsite=PROJECT)
turbine_names = assets["data"]["title"].tolist()

owts = OWTs(
    turbines=turbine_names,
    api=api,
    projectsite=PROJECT,
)

owts.process_structures()

# Aggregated tower data across all turbines
print(owts.tower.head())
```

### 6. Visualise the geometry

Plot all processed turbines with the built-in Plotly visualisation:

```python
fig = api.plot_turbines(owts=owts)
fig.show()
```

## What you learned

- How to create an `OWT` processor from the geometry API
- That `process_structure()` must be called before accessing component
  DataFrames
- How to batch-process turbines with `OWTs`
- How to generate a Plotly figure of turbine geometries

## Next steps

- [How to query geometry data](../how-to/query-geometry.md) — lower-level
  geometry queries
- [Geometry API reference](../reference/api/geometry.md) — complete
  method signatures
