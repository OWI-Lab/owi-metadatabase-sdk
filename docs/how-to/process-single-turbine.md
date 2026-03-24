# How to process a single turbine

## Create an OWT processor from the API

The fastest path is `get_owt_geometry_processor()`, which fetches and
wraps the data in a single call:

```python
from owi.metadatabase.geometry.io import GeometryAPI

api = GeometryAPI(token="your-token")

owt = api.get_owt_geometry_processor(
    projectsite="Nobelwind",
    assetlocation="BBB01",
)
```

## Process the structure

You **must** call `process_structure()` before accessing component
DataFrames:

```python
owt.process_structure()
```

## Access component data

```python
# Tower segments
print(owt.tower.head())

# Transition piece segments
print(owt.tp.head())

# Monopile segments
print(owt.mp.head())

# Rotor-Nacelle Assembly
print(owt.rna)
```

## Handle missing data gracefully

If a turbine has no geometry data, `process_structure()` will still
succeed but some component DataFrames may be empty:

```python
if owt.tower.empty:
    print("No tower data available for this turbine")
```
