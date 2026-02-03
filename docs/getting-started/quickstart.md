# Quick Start

This guide will help you get started with the OWI Metadatabase SDK in just a few minutes.

## Prerequisites

- OWI Metadatabase API token (contact OWI-Lab for access)
- Python 3.9 or higher installed
- Package installed (see [Installation](installation.md))

## Basic Workflow

### 1. Import the Required Modules

```python
from owi.metadatabase.geometry.io import GeometryAPI
from owi.metadatabase.locations.io import LocationsAPI
```

### 2. Initialize API Clients

```python
# Using token authentication
TOKEN = "your-api-token-here"

geometry_api = GeometryAPI(token=TOKEN)
locations_api = LocationsAPI(token=TOKEN)
```

### 3. Retrieve Location Data

```python
# Get all turbine locations for a project
locations = locations_api.get_locations(
    projectsite="YourProjectName"
)

print(f"Found {len(locations)} turbines")
print(locations.head())
```

### 4. Retrieve Geometry Data

```python
# Get geometry data for specific turbines
turbines = ["TURB01", "TURB02", "TURB03"]

for turbine in turbines:
    geometry = geometry_api.get_turbine_geometry(
        assetlocation=turbine,
        projectsite="YourProjectName"
    )
    print(f"Turbine: {turbine}")
    print(f"  Hub height: {geometry['hub_height']} m")
    print(f"  Tower base: {geometry['tower_base']} mLAT")
```

### 5. Process Geometry

```python
from owi.metadatabase.geometry.processing import OWT

# Create OWT object for detailed processing
owt = OWT(
    turbine="TURB01",
    projectsite="YourProjectName",
    api=geometry_api
)

# Process structure
owt.process_structure()

# Access processed data
print(owt.tower.head())         # Tower geometry
print(owt.monopile.head())      # Monopile geometry
print(owt.rna)                  # RNA (Rotor-Nacelle-Assembly) data
```

## Complete Example

Here's a complete example that demonstrates the workflow:

```python
from owi.metadatabase.geometry.io import GeometryAPI
from owi.metadatabase.locations.io import LocationsAPI
from owi.metadatabase.geometry.processing import OWT

# Configuration
TOKEN = "your-api-token"
PROJECT = "YourProjectName"
TURBINE = "TURB01"

# Initialize APIs
geo_api = GeometryAPI(token=TOKEN)
loc_api = LocationsAPI(token=TOKEN)

# Get locations
locations = loc_api.get_locations(projectsite=PROJECT)
print(f"Project has {len(locations)} turbines")

# Get and process geometry for one turbine
owt = OWT(
    turbine=TURBINE,
    projectsite=PROJECT,
    api=geo_api
)

owt.process_structure()

# Display results
print(f"\n{TURBINE} Geometry Summary:")
print(f"  Tower segments: {len(owt.tower)}")
print(f"  Monopile segments: {len(owt.monopile)}")
print(f"  RNA mass: {owt.rna['Mass [t]'].sum():.2f} tonnes")
```

## Working with Multiple Turbines

Process multiple turbines efficiently:

```python
from owi.metadatabase.geometry.processing import OWTs

# Get locations first
locations = loc_api.get_locations(projectsite=PROJECT)
turbine_list = locations['title'].tolist()

# Process all turbines
owts = OWTs(
    turbines=turbine_list,
    api=geo_api,
    projectsite=PROJECT
)

owts.process_structures()

# Access aggregated data
print(owts.all_turbines)  # Summary of all turbines
print(owts.tower)          # All tower data concatenated
```

## Next Steps

- **[User Guide](../user-guide/overview.md)** - Detailed documentation
- **[API Reference](../api/index.md)** - Complete API documentation

## Common Patterns

### Authentication

```python
# Token authentication (recommended)
api = GeometryAPI(token="your-token")

# Username/password authentication
api = GeometryAPI(uname="username", password="password")
```

### Error Handling

```python
from owi.metadatabase._utils.exceptions import (
    APIConnectionError,
    DataProcessingError
)

try:
    data = geometry_api.get_turbine_geometry(
        assetlocation="TURB01",
        projectsite="Project"
    )
except APIConnectionError as e:
    print(f"Connection failed: {e}")
except DataProcessingError as e:
    print(f"Data processing error: {e}")
```

### Filtering Data

```python
# Django-style filtering
locations = loc_api.get_locations(
    projectsite="Project",
    title__icontains="A01"  # Turbines containing "A01"
)
```
