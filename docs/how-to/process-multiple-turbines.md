# How to process multiple turbines

## Collect turbine names

First retrieve the asset locations for your project site:

```python
from owi.metadatabase.geometry.io import GeometryAPI
from owi.metadatabase.locations.io import LocationsAPI

TOKEN = "your-token"
PROJECT = "Nobelwind"

loc_api = LocationsAPI(token=TOKEN)
geo_api = GeometryAPI(token=TOKEN)

assets = loc_api.get_assetlocations(projectsite=PROJECT)
turbine_names = assets["data"]["title"].tolist()
```

## Create and process an OWTs batch

```python
from owi.metadatabase.geometry.processing import OWTs

owts = OWTs(
    turbines=turbine_names,
    api=geo_api,
    projectsite=PROJECT,
)

owts.process_structures()
```

## Access aggregated data

After processing, `OWTs` provides concatenated DataFrames across all
turbines:

```python
# All tower segments from every turbine
print(owts.tower.head())

# All monopile segments
print(owts.mp.head())
```

## Plot all turbines

```python
fig = geo_api.plot_turbines(owts=owts)
fig.show()
```
