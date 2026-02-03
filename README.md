# OWI Metadatabase SDK

[![version](https://img.shields.io/pypi/v/owi-metadatabase)](https://pypi.org/project/owi-metadatabase/)
[![python versions](https://img.shields.io/pypi/pyversions/owi-metadatabase)](https://pypi.org/project/owi-metadatabase/)
[![license](https://img.shields.io/github/license/owi-lab/owi-metadatabase-sdk)](https://github.com/OWI-Lab/owi-metadatabase-sdk/blob/main/LICENSE)
[![pytest](https://img.shields.io/github/actions/workflow/status/owi-lab/owi-metadatabase-sdk/ci.yml?label=pytest)](https://github.com/OWI-Lab/owi-metadatabase-sdk/actions/workflows/ci.yml)
[![lint](https://img.shields.io/github/actions/workflow/status/owi-lab/owi-metadatabase-sdk/ci.yml?label=lint)](https://github.com/OWI-Lab/owi-metadatabase-sdk/actions/workflows/ci.yml)
[![issues](https://img.shields.io/github/issues/owi-lab/owi-metadatabase-sdk)](https://github.com/OWI-Lab/owi-metadatabase-sdk/issues)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.17531273.svg)](https://doi.org/10.5281/zenodo.10620568)

**Core SDK for OWI-Lab metadatabase: geometry and location data processing.**

A modern Python namespace package providing tools for working with offshore wind turbine geometry and location data from the OWI Metadatabase. Built with extensibility in mind using PEP 420 namespace packages.

📚 **[Read the Documentation](https://owi-lab.github.io/owi-metadatabase-sdk/)**

## ✨ Features

- 🏗️ **Geometry Module**: Process offshore wind turbine geometries, components, and structures
- 📍 **Locations Module**: Handle geographic location and site data
- 🔌 **API Integration**: Seamless connection to OWI Metadatabase API
- 🧩 **Extensible**: Namespace package architecture supports future extensions
- 🎯 **Type-Safe**: Full type hints for better IDE support
- 📖 **Well-Documented**: Comprehensive documentation with NumPy-style docstrings

## 📦 Installation

### Quick Install

Using pip:
```bash
pip install owi-metadatabase
```

Using uv (recommended for development):
```bash
uv pip install owi-metadatabase
```

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

## 🚀 Quick Start

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

See the [Quick Start Guide](https://owi-lab.github.io/owi-metadatabase-sdk/getting-started/quickstart/) for more examples.

## 🔄 Migration from v0.10.x

If you're upgrading from `owi-metadatabase-sdk` v0.10.x, see our [Migration Guide](https://owi-lab.github.io/owi-metadatabase-sdk/getting-started/migration/).

**Key Changes:**
- Package name: `owi-metadatabase-sdk` → `owi-metadatabase`
- Import path: `owimetadatabase_preprocessor.*` → `owi.metadatabase.*`
- Removed modules: `fatigue`, `soil`, and `results` (available as separate packages in the future)

## 🛠️ Development

This project uses modern Python tooling:

- **[uv](https://github.com/astral-sh/uv)**: Fast Python package manager
- **[invoke](https://www.pyinvoke.org/)**: Task automation
- **[ruff](https://github.com/astral-sh/ruff)**: Linting and formatting
- **[pytest](https://pytest.org/)**: Testing with extensive doctest coverage
- **[MkDocs Material](https://squidfunk.github.io/mkdocs-material/)**: Documentation

### Common Tasks

```bash
# Run tests
uv run invoke test.all

# Build documentation
uv run invoke docs.build

# Serve documentation locally
uv run invoke docs.serve

# Run code quality checks
uv run invoke quality.all

# Format code
uv run invoke quality.format
```

### Project Structure

```
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

## 🧩 Extensibility

This package uses PEP 420 namespace packages, allowing modular extensions. Future packages will extend the `owi.metadatabase` namespace:

- **`owi-metadatabase-fatigue`** (planned): Fatigue analysis tools
- **`owi-metadatabase-soil`** (planned): Soil data processing
- **Your extension**: Create custom extensions using the namespace

All extensions work seamlessly together:
```python
from owi.metadatabase.geometry import GeometryAPI     # Base
from owi.metadatabase.fatigue import FatigueAPI       # Extension
from owi.metadatabase.soil import SoilAPI             # Extension
```

## 📖 Documentation

- **[Getting Started](https://owi-lab.github.io/owi-metadatabase-sdk/getting-started/installation/)**: Installation and quick start
- **[User Guide](https://owi-lab.github.io/owi-metadatabase-sdk/user-guide/overview/)**: Comprehensive usage guide
- **[API Reference](https://owi-lab.github.io/owi-metadatabase-sdk/api/index/)**: Complete API documentation
- **[Examples](https://owi-lab.github.io/owi-metadatabase-sdk/examples/index/)**: Jupyter notebooks and code examples

## 🤝 Contributing

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

## 📄 License

This package is licensed under the [GNU General Public License v3.0](https://www.gnu.org/licenses/gpl-3.0.en.html).

## 👥 Authors

`owi-metadatabase` is developed and maintained by the team at [OWI-Lab](https://www.owi-lab.be/).

**Core Contributors:**
- Arsen Melnikov ([@arsmlnkv](https://github.com/arsmlnkv))
- Pietro D'Antuono ([@petrushy](https://github.com/petrushy))

## 🙏 Acknowledgements

This package was developed as part of:
- **ETF Smartlife (FOD165)** project
- **WILLOW (EUAR157)** project

## 📊 Project Status

| Aspect | Status |
|--------|--------|
| Version | ![PyPI Version](https://img.shields.io/pypi/v/owi-metadatabase) |
| Python | ![Python Versions](https://img.shields.io/pypi/pyversions/owi-metadatabase) |
| Tests | ![Test Status](https://img.shields.io/github/actions/workflow/status/owi-lab/owi-metadatabase-sdk/ci.yml?label=tests) |
| Coverage | 76% |
| Documentation | ![Docs](https://img.shields.io/badge/docs-mkdocs-blue) |
| License | ![License](https://img.shields.io/github/license/owi-lab/owi-metadatabase-sdk) |

## 🔗 Related Projects

- **[OWI-Lab Website](https://www.owi-lab.be/)**: Research lab website
- **[OWI Metadatabase](https://metadatabase.owi-lab.be/)**: Online database

## 💬 Support

- **Issues**: [GitHub Issues](https://github.com/OWI-Lab/owi-metadatabase-sdk/issues)
- **Discussions**: [GitHub Discussions](https://github.com/OWI-Lab/owi-metadatabase-sdk/discussions)
- **Email**: [info@owi-lab.be](mailto:info@owi-lab.be)

---

**Built with ❤️ by OWI-Lab**
