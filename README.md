# OWI-metadatabase SDK

[![version](https://img.shields.io/pypi/v/owi-metadatabase)](https://pypi.org/project/owi-metadatabase/)
[![python versions](https://img.shields.io/pypi/pyversions/owi-metadatabase)](https://pypi.org/project/owi-metadatabase/)
[![license](https://img.shields.io/github/license/owi-lab/owi-metadatabase-sdk)](https://github.com/OWI-Lab/owi-metadatabase-sdk/blob/main/LICENSE)
[![pytest](https://img.shields.io/github/actions/workflow/status/owi-lab/owi-metadatabase-sdk/ci.yml?label=pytest)](https://github.com/OWI-Lab/owi-metadatabase-sdk/actions/workflows/ci.yml)
[![lint](https://img.shields.io/github/actions/workflow/status/owi-lab/owi-metadatabase-sdk/ci.yml?label=lint)](https://github.com/OWI-Lab/owi-metadatabase-sdk/actions/workflows/ci.yml)
[![issues](https://img.shields.io/github/issues/owi-lab/owi-metadatabase-sdk)](https://github.com/OWI-Lab/owi-metadatabase-sdk/issues)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.17531273.svg)](https://doi.org/10.5281/zenodo.10620568)
![Coverage](https://img.shields.io/badge/coverage-90%25-brightgreen)
[![Documentation](https://img.shields.io/badge/docs-zensical-blue)](https://owi-lab.github.io/owi-metadatabase-sdk/)

**Core SDK for OWI-Lab metadatabase geometry and location workflows, with optional extras for soil, results, and SHM.**

A modern Python namespace package providing tools for working with offshore wind turbine geometry and location data from the OWI-metadatabase. The core package stays focused on shared APIs and data access, while optional extras install the soil, results, and structural health monitoring extensions into the same `owi.metadatabase` namespace.

📚 **[Read the Documentation](https://owi-lab.github.io/owi-metadatabase-sdk/)**

## Features

- **Geometry Module**: Process offshore wind turbine geometries, components, and structures
- **Locations Module**: Handle geographic location and site data
- **API Integration**: Seamless connection to OWI-metadatabase API
- **Extensible**: Namespace package architecture supports deployed domain extensions
  - [`owi-metadatabase-soil`](https://github.com/OWI-Lab/owi-metadatabase-soil-sdk)
  - [`owi-metadatabase-results`](https://github.com/OWI-Lab/owi-metadatabase-results-sdk)
  - [`owi-metadatabase-shm`](https://github.com/OWI-Lab/owi-metadatabase-shm-sdk)
  - [`owi-metadatabase-ext-sdk-tpl`](https://github.com/OWI-Lab/owi-metadatabase-ext-sdk-tpl) for scaffolding new extensions
  - `owi-metadatabase-fatigue` (planned)

## Installation

### Quick Install

Using pip:

```bash
pip install owi-metadatabase
```

Using uv (recommended for development):

```bash
uv pip install owi-metadatabase
```

### Install optional extras

Using pip:

```bash
pip install "owi-metadatabase[soil]"
pip install "owi-metadatabase[results]"
pip install "owi-metadatabase[shm]"
```

Using uv:

```bash
uv pip install "owi-metadatabase[soil]"
uv pip install "owi-metadatabase[results]"
uv pip install "owi-metadatabase[shm]"
```

Install multiple extras together when you need more than one extension:

```bash
pip install "owi-metadatabase[soil,results,shm]"
```

In `zsh`, keep extras in quotes because `[` and `]` are treated as glob characters.

### Development Installation

For contributing to the package:

```bash
# Clone the repository
git clone https://github.com/OWI-Lab/owi-metadatabase-sdk.git
cd owi-metadatabase-sdk

# Install with uv (recommended)
uv sync --dev

# Or with pip
pip install -e ".[dev]"
```

## Quick Start

```python
from owi.metadatabase.geometry.io import GeometryAPI
from owi.metadatabase.locations.io import LocationsAPI

# Initialize API clients
geometry_api = GeometryAPI(API_key='your-api-key')
locations_api = LocationsAPI(API_key='your-api-key')

# Fetch turbine geometry
turbine = geometry_api.get_geometry_turbine(turbine_id=123)

# Get location data
location = locations_api.get_location(location_id=456)
```

See the [How To Guide](https://owi-lab.github.io/owi-metadatabase-sdk/how-to/) for more examples.

## 🔄 Migration from v0.10.x

If you're migrating from `pwimetadatabase-preprocessor` v0.10.x, see our [Migration Guide](https://owi-lab.github.io/owi-metadatabase-sdk/how-to/migrate/).

**Key Changes:**

- Package name: `owi-metadatabase-sdk` → `owi-metadatabase`
- Import path: `owimetadatabase_preprocessor.*` → `owi.metadatabase.*`
- Removed modules: `fatigue`, `soil`, and `results` (available as package extensions)
- Extension extras now available from the core package: `soil`, `results`, and `shm`

## Development

This project uses modern Python tooling:

- **[uv](https://github.com/astral-sh/uv)**: Fast Python package manager
- **[invoke](https://www.pyinvoke.org/)**: Task automation
- **[ruff](https://github.com/astral-sh/ruff)**: Linting and formatting
- **[pytest](https://pytest.org/)**: Testing with extensive doctest coverage
- **[Zensical](https://zensical.org/)**: Documentation

### Common Tasks

```bash
# Run tests and serve coverage report
uv run inv test

# Build documentation
uv run inv docs.build

# Serve documentation locally
uv run inv docs.serve

# Run code quality checks
uv run inv quality
```

### Project Structure

```text
src/owi/metadatabase/
├── __init__.py          # Main package entry point
├── geometry/            # Geometry data processing
│   ├── io.py           # GeometryAPI
│   ├── processing.py   # OWT, OWTs classes
│   └── structures.py   # Data structures
├── locations/           # Location data handling
│   └── io.py           # LocationsAPI
└── _utils/             # Internal utilities
    ├── exceptions.py   # Custom exceptions
    └── utils.py        # Helper functions
```

## Extensibility

This package uses PEP 420 namespace packages, allowing modular extensions. Installed packages can extend the `owi.metadatabase` namespace side by side:

- **`owi-metadatabase-soil`**: Soil data processing
- **`owi-metadatabase-results`**: Results querying, typed models, and plotting helpers
- **`owi-metadatabase-shm`**: Structural health monitoring queries, typed records, and upload workflows
- **`owi-metadatabase-fatigue`** (planned): Fatigue analysis tools
- **Your extension**: Create custom extensions using the namespace

All extensions work seamlessly together:

```python
from owi.metadatabase.geometry.io import GeometryAPI
from owi.metadatabase.results import ResultsAPI
from owi.metadatabase.shm import ShmAPI
from owi.metadatabase.soil import SoilAPI
```

## Documentation

- **[Core SDK docs](https://owi-lab.github.io/owi-metadatabase-sdk/)**: Geometry, locations, and shared architecture
- **[How-to guides](https://owi-lab.github.io/owi-metadatabase-sdk/how-to/)**: Installation, authentication, and query recipes
- **[Results extension docs](https://owi-lab.github.io/owi-metadatabase-results-sdk/)**: Results APIs, models, services, and notebooks
- **[SHM extension docs](https://owi-lab.github.io/owi-metadatabase-shm-sdk/)**: Sensor and signal retrieval, typed services, and upload workflows
- **[Soil extension docs](https://owi-lab.github.io/owi-metadatabase-soil-sdk/)**: Soil APIs, processing, and visualization

## Contributing

We welcome contributions! Please see our [Contributing Guide](https://owi-lab.github.io/owi-metadatabase-sdk/development/contributing/) for details.

### Quick Contribution Workflow

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make your changes with tests and documentation
4. Run quality checks: `uv run invoke quality.all`
5. Run tests: `uv run invoke test.all`
6. Commit your changes: `git commit -m 'feat: add amazing feature'`
7. Push to the branch: `git push origin feature/amazing-feature`
8. Open a Pull Request

## License

This package is licensed under the [GNU General Public License v3.0](https://www.gnu.org/licenses/gpl-3.0.en.html).

## 👥 Authors

`owi-metadatabase` is developed and maintained by the team at [OWI-Lab](https://www.owi-lab.be/).

**Core Contributors:**

- Pietro D'Antuono ([@pietrodantuono](https://github.com/pietrodantuono))
- Arsen Melnikov ([@arsmlnkv](https://github.com/arsmlnkv))

## Acknowledgements

This package was developed as part of:

- **ETF Smartlife (FOD165)** project
- **WILLOW (EUAR157)** project

## Project Status

| Aspect        | Status                                                                                                                |
|---------------|-----------------------------------------------------------------------------------------------------------------------|
| Version       | ![PyPI Version](https://img.shields.io/pypi/v/owi-metadatabase)                                                       |
| Python        | ![Python Versions](https://img.shields.io/pypi/pyversions/owi-metadatabase)                                           |
| Tests         | ![Test Status](https://img.shields.io/github/actions/workflow/status/owi-lab/owi-metadatabase-sdk/ci.yml?label=tests) |
| Coverage      | ![Coverage](https://img.shields.io/badge/coverage-90%25-brightgreen)                                                  |
| Documentation | ![Docs](https://img.shields.io/badge/docs-zensical-blue)                                                              |
| License       | ![License](https://img.shields.io/github/license/owi-lab/owi-metadatabase-sdk)                                        |

## Related Projects

- **[OWI-Lab Website](https://www.owi-lab.be/)**: Research lab website
- **[OWI-metadatabase](https://owimetadatabase.azurewebsites.net/)**: Online database

## Support

- **Issues**: [GitHub Issues](https://github.com/OWI-Lab/owi-metadatabase-sdk/issues)
- **Discussions**: [GitHub Discussions](https://github.com/OWI-Lab/owi-metadatabase-sdk/discussions)
- **Email**: [pietro.dantuono@vub.be](mailto:pietro.dantuono@vub.be)

---

### Built with ❤️ and 🧠 by OWI-Lab
