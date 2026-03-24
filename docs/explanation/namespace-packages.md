# Namespace packages

The OWI Metadatabase SDK uses **PEP 420 implicit namespace packages**.
This page explains what that means and why the design was chosen.

## What is a namespace package?

A regular Python package has an `__init__.py` file at every level of its
directory tree. A namespace package omits the `__init__.py` at certain
levels, allowing multiple separately-installed distributions to contribute
sub-packages under the same top-level name.

In this project the `owi/` directory has **no** `__init__.py`. The
`owi.metadatabase` level uses `pkgutil.extend_path` so that extension
packages can add modules alongside the core package:

```txt
site-packages/
├── owi/                          # No __init__.py — namespace root
│   └── metadatabase/             # No __init__.py — namespace package
│       ├── io.py                 # Core SDK
│       ├── geometry/             # Core SDK
│       ├── locations/            # Core SDK
│       ├── soil/                 # From owi-metadatabase-soil
│       └── results/              # From owi-metadatabase-results
```

## Why namespace packages?

The OWI Metadatabase covers several data domains — geometry, locations,
soil, fatigue, structural results. Bundling everything in a single PyPI
distribution would force users to install dependencies they do not need.

Namespace packages solve this by allowing each domain to ship as an
independent PyPI package while sharing the `owi.metadatabase` import
prefix:

```python
# Core SDK (pip install owi-metadatabase)
from owi.metadatabase.geometry.io import GeometryAPI
from owi.metadatabase.locations.io import LocationsAPI

# Soil extension (pip install owi-metadatabase-soil)
from owi.metadatabase.soil.io import SoilAPI

# Results extension (pip install owi-metadatabase-results)
from owi.metadatabase.results.io import ResultsAPI
```

## Practical implications

### Installing extensions

Extensions are installed alongside the core package:

```bash
pip install owi-metadatabase
pip install owi-metadatabase-soil
```

Or as optional extras:

```bash
pip install "owi-metadatabase[soil]"
```

### No `__init__.py` at the `owi/` root and `owi.metadatabase` level

If you create an `__init__.py` in `owi/` or `owi/metadatabase/`, it will shadow
the namespace and break imports from other `owi.metadatabase.*` distributions.
Do not add `__init__.py` files at these levels.

### Validation

You can confirm the namespace is working:

```python
import owi.metadatabase
print(owi.metadatabase.__path__)
# Should list multiple directories if extensions are installed
```

## Creating a new extension

New extension packages can be scaffolded from the
[`owi-metadatabase-ext-sdk-tpl`](https://github.com/OWI-Lab/owi-metadatabase-ext-sdk-tpl)
Copier template. The template generates the correct namespace layout,
`pyproject.toml`, and CI workflows automatically.
