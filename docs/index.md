# OWI-metadatabase SDK

**Core Python SDK for the OWI-Lab metadatabase: geometry and location data**

[![PyPI version](https://img.shields.io/pypi/v/owi-metadatabase)](https://pypi.org/project/owi-metadatabase/)
[![Python versions](https://img.shields.io/pypi/pyversions/owi-metadatabase)](https://pypi.org/project/owi-metadatabase/)
[![License](https://img.shields.io/github/license/owi-lab/owi-metadatabase-sdk)](https://github.com/OWI-Lab/owi-metadatabase-sdk/blob/main/LICENSE)
[![Documentation](https://img.shields.io/badge/docs-mkdocs-blue)](https://owi-lab.github.io/owi-metadatabase-sdk/)

## Overview

The OWI-metadatabase SDK provides a Python interface to interact with the OWI-Lab metadatabase for offshore wind installations. This core package includes modules for:

- **Geometry**: Processing and analysis of offshore wind turbine geometry data
- **Locations**: Handling location and site data for offshore wind farms

## Quick Start

### Installation

```bash
pip install owi-metadatabase
```

### Basic Usage

```python
from owi.metadatabase.geometry.io import GeometryAPI
from owi.metadatabase.locations.io import LocationsAPI

# Initialize APIs
geometry_api = GeometryAPI(token="your-token")
locations_api = LocationsAPI(token="your-token")

# Get geometry data
turbines = geometry_api.get_turbines(projectsite="YourProject")

# Get location data
locations = locations_api.get_locations(projectsite="YourProject")
```

## Namespace Package Structure

This package follows PEP 420 namespace conventions, allowing for modular extensions:

```python
# Core package
from owi.metadatabase.geometry import GeometryAPI
from owi.metadatabase.locations import LocationsAPI

# Future extensions (when available)
# from owi.metadatabase.fatigue import FatigueAPI
# from owi.metadatabase.soil import SoilAPI
```

## Documentation

- **[Getting Started](getting-started/installation.md)** - Installation and quickstart guide
- **[User Guide](user-guide/overview.md)** - Detailed usage documentation
- **[API Reference](api/index.md)** - Complete API documentation

## Requirements

- Python 3.9+
- numpy
- pandas
- requests
- plotly
- matplotlib
- tqdm

## License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](https://github.com/OWI-Lab/owi-metadatabase-sdk/blob/main/LICENSE) file for details.

## Citation

If you use this package in your research, please cite:

```bibtex
@software{owi_metadatabase_sdk,
  author = {OWI-Lab},
  title = {OWI-metadatabase SDK},
  year = {2026},
  url = {https://github.com/OWI-Lab/owi-metadatabase-sdk},
  doi = {10.5281/zenodo.10620568}
}
```

## Acknowledgements

This package was developed as part of the [ETF Smartlife (FOD165)](https://owi-lab.be/projects/smartlife) and [WILLOW (EUAR157)](https://willow-project.eu/) projects.

## Support

- **Issues**: [GitHub Issues](https://github.com/OWI-Lab/owi-metadatabase-sdk/issues)
- **Discussions**: [GitHub Discussions](https://github.com/OWI-Lab/owi-metadatabase-sdk/discussions)
- **Email**: [OWI-Lab Contact](mailto:info@owi-lab.be)
