# OWI Metadatabase SDK

[![PyPI version](https://img.shields.io/pypi/v/owi-metadatabase)](https://pypi.org/project/owi-metadatabase/)
[![Python versions](https://img.shields.io/pypi/pyversions/owi-metadatabase)](https://pypi.org/project/owi-metadatabase/)
[![License](https://img.shields.io/github/license/owi-lab/owi-metadatabase-sdk)](https://github.com/OWI-Lab/owi-metadatabase-sdk/blob/main/LICENSE)
[![Documentation](https://img.shields.io/badge/docs-zensical-blue)](https://owi-lab.github.io/owi-metadatabase-sdk/)

!!! abstract "What is the OWI Metadatabase SDK?"
    The OWI Metadatabase SDK is a Python package that provides tools for accessing and processing geometry and location data from the OWI-Lab metadatabase for offshore wind installations. It serves as the core package in a modular namespace architecture, with extension packages available for additional domains like soil and results data.

    - **Geometry** — offshore wind turbine geometry data and structural processing
    - **Locations** — project site and asset location queries

## Get started

```bash
pip install owi-metadatabase
```

```python
from owi.metadatabase.geometry.io import GeometryAPI
from owi.metadatabase.locations.io import LocationsAPI

geometry_api = GeometryAPI(token="your-token")
locations_api = LocationsAPI(token="your-token")
```

<div class="grid cards" markdown>

-   :lucide-backpack:{ .lg .middle } **Tutorials**

    ---

    Step-by-step lessons to get started

    [:octicons-arrow-right-24: Start learning](tutorials/index.md)

-   :lucide-gamepad-directional:{ .lg .middle } **How-to guides**

    ---

    Recipes for specific tasks

    [:octicons-arrow-right-24: Find a guide](how-to/index.md)

-   :lucide-book-open:{ .lg .middle } **Reference**

    ---

    Complete API documentation

    [:octicons-arrow-right-24: Browse reference](reference/index.md)

-   :lucide-lightbulb:{ .lg .middle } **Explanation**

    ---

    Architecture and design decisions

    [:octicons-arrow-right-24: Understand the SDK](explanation/index.md)

</div>

## Extension packages

The SDK uses [namespace packages](explanation/namespace-packages.md) so
additional domains can be installed alongside the core:

| Extension | Install | Import |
|-----------|---------|--------|
| [Soil](https://pypi.org/project/owi-metadatabase-soil/) | `pip install "owi-metadatabase[soil]"` | `from owi.metadatabase.soil.io import SoilAPI` |
| [Results](https://pypi.org/project/owi-metadatabase-results/) | `pip install owi-metadatabase-results` | `from owi.metadatabase.results.io import ResultsAPI` |

## Citation

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
- **Email**: [OWI-Lab Contact](mailto:pietro.dantuono@vub.be)
