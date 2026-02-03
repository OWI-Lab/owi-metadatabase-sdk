# User Guide

Welcome to the OWI Metadatabase SDK user guide. This guide provides comprehensive information on using the package to interact with the OWI Metadatabase API.

## What is OWI Metadatabase SDK?

The OWI Metadatabase SDK is a Python package that simplifies interaction with the OWI Metadatabase, a centralized repository for offshore wind turbine data. The SDK handles:

- **Geometry Data**: Offshore wind turbine geometries, components, and structures
- **Location Data**: Geographic locations and site information
- **API Authentication**: Automatic token management and request handling
- **Data Processing**: Utilities for processing and transforming data

## Core Modules

### Geometry Module

The `geometry` module provides access to offshore wind turbine geometries:

```python
from owi.metadatabase.geometry.io import GeometryAPI
from owi.metadatabase.geometry.processing import OWT, OWTs

# Initialize API
geometry_api = GeometryAPI(API_key='your-api-key')

# Fetch turbine geometry
turbine = geometry_api.get_geometry_turbine(turbine_id)

# Process geometry
owt = OWT(turbine_data)
```

Key features:

- Retrieve turbine geometries, substructures and components
- Process and transform geometry data
- Work with building blocks, subassemblies, and complete structures

### Locations Module

The `locations` module handles geographic location data:

```python
from owi.metadatabase.locations.io import LocationsAPI

# Initialize API
locations_api = LocationsAPI(API_key='your-api-key')

# Get location information
location = locations_api.get_location(location_id)
```

Key features:

- Retrieve location data for wind farms and sites
- Access geographic coordinates and metadata
- Query available locations

## Package Structure

```
owi.metadatabase/
├── geometry/          # Geometry data handling
│   ├── io.py         # GeometryAPI class
│   ├── processing.py # OWT, OWTs processing classes
│   └── structures.py # Data structures
├── locations/         # Location data handling
│   └── io.py         # LocationsAPI class
└── _utils/           # Internal utilities
    ├── exceptions.py # Custom exceptions
    └── utils.py      # Utility functions
```

## Authentication

All API clients require an API key for authentication:

```python
from owi.metadatabase.geometry.io import GeometryAPI

# Set API key directly
api = GeometryAPI(API_key='your-api-key-here')

# Or use environment variable
import os
os.environ['OWI_API_KEY'] = 'your-api-key-here'
api = GeometryAPI()
```

Store your API key securely, for example using environment variables.

## Error Handling

The SDK provides custom exceptions for different error scenarios:

```python
from owi.metadatabase._utils.exceptions import (
    APIConnectionError,      # API connection failures
    DataProcessingError,     # Data processing errors
    InvalidParameterError,   # Invalid parameters
)

try:
    turbine = geometry_api.get_geometry_turbine(turbine_id)
except APIConnectionError as e:
    print(f"Failed to connect: {e}")
except DataProcessingError as e:
    print(f"Failed to process data: {e}")
```

## Common Workflows

### 1. Fetching Turbine Geometry

```python
from owi.metadatabase.geometry.io import GeometryAPI

# Initialize
api = GeometryAPI(API_key='your-key')

# Get turbine
turbine = api.get_geometry_turbine(turbine_id=123)

# Access components
print(turbine['name'])
print(turbine['components'])
```

### 2. Processing Multiple Turbines

```python
from owi.metadatabase.geometry.processing import OWTs

# Process multiple turbines
turbines_data = [...]  # List of turbine data
owts = OWTs(turbines_data)

# Perform calculations
owts.calculate_properties()
owts.export_processed_data()
```

### 3. Location Queries

```python
from owi.metadatabase.locations.io import LocationsAPI

# Initialize
api = LocationsAPI(API_key='your-key')

# Get locations
locations = api.get_all_locations()

# Filter by criteria
offshore_locations = [
    loc for loc in locations
    if loc['type'] == 'offshore'
]
```

## Next Steps

- **[API Reference](../api/index.md)** - Complete API documentation
- **[Getting Started](../getting-started/installation.md)** - Installation and quickstart guides

## Tips and Best Practices

1. **Cache API responses** - Avoid redundant API calls by caching responses
2. **Use environment variables** - Store API keys securely in environment variables
3. **Handle errors gracefully** - Always wrap API calls in try-except blocks
4. **Validate inputs** - Check parameters before making API requests
5. **Close connections** - Properly close API connections when done

## Getting Help

If you encounter issues or have questions:

- Check the [API Reference](../api/index.md) for detailed documentation
- Report bugs on [GitHub Issues](https://github.com/OWI-Lab/owi-metadatabase-sdk/issues)
- Ask questions in [GitHub Discussions](https://github.com/OWI-Lab/owi-metadatabase-sdk/discussions)
