# How to query geometry data

## List model definitions

```python
from owi.metadatabase.geometry.io import GeometryAPI

api = GeometryAPI(token="your-token")
models = api.get_model_definitions(projectsite="Nobelwind")

print(models["data"].head())
```

## Get a single model definition by ID

```python
model = api.get_modeldefinition_id(modeldefinition_id=42)

print(model["data"])
print(model["id"])
```

## List sub-assemblies

```python
subs = api.get_subassemblies(
    projectsite="Nobelwind",
    assetlocation="BBB01",
)

print(subs["data"][["title", "subassembly_type"]].head())
```

## List building blocks

```python
blocks = api.get_buildingblocks(
    projectsite="Nobelwind",
    assetlocation="BBB01",
)

print(blocks["data"].head())
```

## List materials

```python
materials = api.get_materials()

print(materials["data"][["title", "id"]].head())
```

## Get sub-assembly objects (structured)

```python
sa_objects = api.get_subassembly_objects(
    projectsite="Nobelwind",
    assetlocation="BBB01",
)

# Returns SubAssembly dataclass instances
for sa in sa_objects:
    print(sa.title, sa.subassembly_type)
```
