# How to query location data

## List all project sites

```python
from owi.metadatabase.locations.io import LocationsAPI

api = LocationsAPI(token="your-token")
sites = api.get_projectsites()

print(sites["data"])  # DataFrame of all project sites
print(sites["exists"])  # True if any records were returned
```

## Get details for a single project site

```python
detail = api.get_projectsite_detail(projectsite="Nobelwind")

print(detail["data"])  # DataFrame with one row
print(detail["id"])    # Integer ID of the project site
```

## List asset locations for a project

```python
assets = api.get_assetlocations(projectsite="Nobelwind")

print(assets["data"][["title", "id"]].head())
```

## Get details for a single asset location

```python
asset = api.get_assetlocation_detail(
    projectsite="Nobelwind",
    assetlocation="BBB01",
)

print(asset["data"])
print(asset["id"])
```

## Plot asset locations on a map

```python
fig = api.plot_assetlocations(projectsite="Nobelwind")
fig.show()
```
