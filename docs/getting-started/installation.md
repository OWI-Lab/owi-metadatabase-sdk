# Installation

## Requirements

- Python 3.9 or higher
- pip or uv package manager

## Install from PyPI

The recommended way to install the OWI Metadatabase SDK is via pip:

```bash
pip install owi-metadatabase
```

### Using uv (recommended for development)

If you're using [uv](https://github.com/astral-sh/uv), you can install with:

```bash
uv pip install owi-metadatabase
```

## Install from Source

For development or to get the latest features:

```bash
git clone https://github.com/OWI-Lab/owi-metadatabase-sdk.git
cd owi-metadatabase-sdk
uv sync --dev
```

This will install the package in editable mode with all development dependencies.

## Verify Installation

Check that the package is installed correctly:

```python
import owi.metadatabase
print(owi.metadatabase.__version__)
# Output: 0.11.0
```

Test basic imports:

```python
from owi.metadatabase.geometry import GeometryAPI
from owi.metadatabase.locations import LocationsAPI

print("✓ Installation successful!")
```

## Optional Dependencies

### Documentation

To build documentation locally:

```bash
pip install owi-metadatabase[docs]
```

Or with uv:

```bash
uv sync --group docs
```

### Development

For contributing to the project:

```bash
pip install owi-metadatabase[dev]
```

Or with uv:

```bash
uv sync --dev
```

## Troubleshooting

### Import Errors

If you encounter import errors, ensure you're using the new import paths:

```python
# ✗ Old (v0.10.x)
from owimetadatabase_preprocessor.geometry import GeometryAPI

# ✓ New (v0.11.0+)
from owi.metadatabase.geometry.io import GeometryAPI
```

### Namespace Package Issues

If you have issues with the namespace package structure, ensure you don't have any old installations:

```bash
pip uninstall owi-metadatabase-sdk owimetadatabase-preprocessor
pip install owi-metadatabase
```

## Next Steps

- [Quick Start Guide](quickstart.md)
- [Migration from v0.10.x](migration.md)
- [User Guide](../user-guide/overview.md)
