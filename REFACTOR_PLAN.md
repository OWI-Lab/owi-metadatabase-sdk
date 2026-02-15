# Migration Plan: OWI-Metadatabase Namespace Package (Updated)

## 📋 Executive Summary

Transform `owi-metadatabase-sdk` into a namespace package (`owi-metadatabase`) containing only the core `geometry` and `locations` modules, with future extensibility for separate `fatigue` and `soil` packages.

## 🎯 Goals

1. Create a PEP 420 namespace package structure for `owi.metadatabase`
2. Extract and retain only `geometry` and `locations` modules as base functionality
3. Modernize project infrastructure using Astral `uv`
4. Implement comprehensive testing (pytest + **extensive** doctest)
5. Create professional documentation with **MkDocs + Material theme** (all markdown)
6. Prepare for future extension packages via **Copier templates**
7. Use **invoke** for all task automation
8. Use **ty** for type checking

## 📦 Target Package Structure

### Repository Name

- **Current**: `owi-metadatabase-sdk`
- **New**: `owi-metadatabase` (base package)

### Package Namespace Structure

```text
src/
└── owi/
    └── metadatabase/
        ├── __init__.py          # Main namespace package init
        ├── py.typed             # PEP 561 marker for type hints
        ├── _version.py          # Version management
        ├── geometry/
        │   ├── __init__.py
        │   ├── io.py
        │   ├── processing.py
        │   └── structures.py
        ├── locations/
        │   ├── __init__.py
        │   └── io.py
        └── _utils/              # Internal utilities (if needed)
            ├── __init__.py
            ├── exceptions.py
            └── utils.py
```

### Import Structure Confirmation

✅ **Confirmed**: Imports will be structured as:

```python
from owi.metadatabase.locations.io import LocationsAPI
from owi.metadatabase.geometry.io import GeometryAPI
from owi.metadatabase.geometry.processing import OWT, OWTs
from owi.metadatabase.geometry.structures import Material, SubAssembly
```

The base namespace is `owi`, so all imports start with `from owi.metadatabase...`

### Future Extension Packages

```text
owi-metadatabase-fatigue/
└── src/owi/metadatabase/fatigue/...

owi-metadatabase-soil/
└── src/owi/metadatabase/soil/...
```

## 🔧 Phase 1: Project Restructuring

### 1.1 Namespace Package Setup

- [x] Create PEP 420 namespace structure (`src/owi/metadatabase/`)
- [x] Remove traditional `__init__.py` from `owi/` directory (namespace root)
- [x] Add proper `__init__.py` to `owi/metadatabase/` with:
  - Version info
  - Public API exports
  - Namespace declaration
- [x] Add `py.typed` marker for type checking support

### 1.2 Module Migration

- [x] Move `geometry/` module to `src/owi/metadatabase/geometry/`
- [x] Move `locations/` module to `src/owi/metadatabase/locations/`
- [x] Extract shared utilities from `utility/` to `_utils/` (prefix indicates internal)
- [x] Update all import statements package-wide:

  ```python
  # Old: from owimetadatabase_preprocessor.geometry import X
  # New: from owi.metadatabase.geometry import X
  ```

### 1.3 Remove Legacy Modules

- [x] Archive `fatigue/` and `soil/` modules for future separate repositories
- [x] Remove `results/` module (or relocate if needed)
- [x] Clean up unused io.py at root level

## 📝 Phase 2: Build System Migration to UV

### 2.1 Update pyproject.toml

```toml
[project]
name = "owi-metadatabase"
version = "0.1.0"  # Major restructuring bump
description = "Core SDK for OWI-Lab metadatabase: geometry and location data"
authors = [
    { name = "arsmlnkv", email = "arsen.melnikov@vub.be" },
    { name = "Pietro D'Antuono", email = "pietro.dantuono@vub.be" }
]
readme = "README.md"
license = { file = "LICENSE" }
keywords = ["owimetadatabase", "offshore wind", "geometry", "locations"]
requires-python = ">=3.9,<3.14"
classifiers = [...]

dependencies = [
    # Core dependencies only (remove fatigue/soil-specific deps)
    "numpy>=1.26.0,<2.0.0; python_version<'3.11'",
    "numpy>=2.0.0; python_version>='3.11'",
    "pandas>=2.0.0",
    "requests>=2.32.0",
    "pyproj>=3.6.0",
    "tqdm>=4.66.0",
]

[dependency-groups]
dev = [
    {include-group = "test"},
    {include-group = "lint"},
    {include-group = "typing"},
    {include-group = "docs"},
    {include-group = "dev-tools"},
]
test = [
    "pytest>=8.4.0",
    "pytest-cov>=7.0.0",
    "pytest-xdist>=3.7.0",
    "pytest-mock>=3.15.0",
    "pytest-clarity>=1.0.0",
]
lint = [
    "ruff>=0.12.9"
]
typing = [
    "ty>=0.2.0",  # NEW: Astral ty instead of mypy
    "pandas-stubs>=2.0.0",
    "types-requests>=2.32.0",
]
docs = [
    "mkdocs>=1.6.0",  # NEW: MkDocs
    "mkdocs-material>=9.5.0",  # Material theme
    "mkdocstrings[python]>=0.27.0",  # Python autodoc
    "mkdocs-jupyter>=0.25.0",  # Jupyter notebook support
    "mkdocs-git-revision-date-localized-plugin>=1.3.0",
    "mkdocs-minify-plugin>=0.8.0",
    "markdown-include>=0.8.0",
]
dev-tools = [
    "invoke>=2.2.0",  # Task runner
    "pre-commit>=3.0.0"
]

# NEW: Extension dependency groups for future use
fatigue = [
    "owi-metadatabase-fatigue>=0.1.0",  # Future package
]
soil = [
    "owi-metadatabase-soil>=0.1.0",  # Future package
]

[build-system]
requires = ["hatchling>=1.25.0"]
build-backend = "hatchling.build"

[tool.hatch.build.targets.wheel]
packages = ["src/owi"]

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
addopts = [
    "-v",
    "--strict-markers",
    "--tb=short",
    "--cov=src/owi/metadatabase",
    "--cov-report=html",
    "--cov-report=term-missing:skip-covered",
    "--doctest-modules",  # Enable doctest
    "--doctest-continue-on-failure",
]
doctest_optionflags = ["NORMALIZE_WHITESPACE", "ELLIPSIS", "NUMBER"]

[tool.ruff]
line-length = 120
target-version = "py39"

[tool.ruff.lint]
select = ["E", "W", "F", "I", "D", "UP", "B", "C4", "SIM", "TCH", "RUF"]
ignore = []

[tool.ruff.lint.pydocstyle]
convention = "numpy"

[tool.ruff.lint.isort]
known-first-party = ["owi.metadatabase"]
```

### 2.2 UV Configuration

- [x] Create `.python-version` file: `3.9`
- [x] Generate uv.lock to repository
- [x] Update CI/CD to use `uv` commands:

  ```bash
  uv sync --dev
  uv run invoke test
  uv build
  ```

### 2.3 Dependency Cleanup

- [x] Audit dependencies - remove:
  - `groundhog` (soil-specific)
  - `scipy` (if only used in soil/fatigue)
  - `matplotlib`, `plotly` (if only for fatigue/soil viz)
- [x] Run `uv tree` to verify dependency graph

## 🧪 Phase 3: Testing Infrastructure

### 3.1 Test Directory Restructuring (Mirror Source)

```text
tests/
├── __init__.py
├── conftest.py              # Global fixtures
├── test_version.py          # Package metadata tests
├── geometry/
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_io.py           # Mirrors src/owi/metadatabase/geometry/io.py
│   ├── test_processing.py   # Mirrors src/owi/metadatabase/geometry/processing.py
│   ├── test_structures.py   # Mirrors src/owi/metadatabase/geometry/structures.py
│   └── data/                # Test fixtures
└── locations/
    ├── __init__.py
    ├── conftest.py
    ├── test_io.py           # Mirrors src/owi/metadatabase/locations/io.py
    └── data/
```

**Key**: Test structure **exactly mirrors** source structure. `test_*.py` files correspond 1:1 with source module files.

### 3.2 Extensive Doctest Requirements

- [x] **Every public function** must have doctest examples
- [x] **At least 2-3 examples** per function showing:
  - Basic usage
  - Edge cases
  - Error handling (where applicable)
- [x] Use doctest fixtures in `conftest.py` for complex objects
- [x] Configure pytest to discover and run all doctests
- [ ] Example comprehensive docstring:

  ```python
  def transform_coordinates(
      x: float,
      y: float,
      from_crs: str = "EPSG:4326",
      to_crs: str = "EPSG:3857"
  ) -> tuple[float, float]:
      """
      Transform coordinates from one CRS to another.

      Parameters
      ----------
      x : float
          X coordinate in source CRS
      y : float
          Y coordinate in source CRS
      from_crs : str, optional
          Source coordinate reference system, by default "EPSG:4326"
      to_crs : str, optional
          Target coordinate reference system, by default "EPSG:3857"

      Returns
      -------
      tuple[float, float]
          Transformed (x, y) coordinates in target CRS

      Raises
      ------
      ValueError
          If coordinates are outside valid range for CRS

      See Also
      --------
      LocationsAPI.get_coordinates : Retrieve coordinates from API

      Examples
      --------
      Basic transformation from WGS84 to Web Mercator:

      >>> transform_coordinates(100.0, 50.0)
      (11131949.079327356, 6446275.841017159)

      Transform with explicit CRS specification:

      >>> transform_coordinates(
      ...     100.0, 50.0,
      ...     from_crs="EPSG:4326",
      ...     to_crs="EPSG:28992"
      ... )  # doctest: +ELLIPSIS
      (8734...., 5234....)

      Edge case - coordinates at origin:

      >>> transform_coordinates(0.0, 0.0)
      (0.0, 0.0)

      Invalid coordinates raise ValueError:

      >>> transform_coordinates(200.0, 100.0)  # doctest: +SKIP
      Traceback (most recent call last):
          ...
      ValueError: Coordinates outside valid range
      """
  ```

### 3.3 Testing Best Practices

- [x] Achieve ≥90% code coverage for core modules
- [x] Mock external API calls (requests-mock)
- [x] Parametrize tests for multiple Python versions
- [x] Add property-based tests with Hypothesis

## 📚 Phase 4: MkDocs Documentation

### 4.1 MkDocs + Material Theme Setup

```yaml
# mkdocs.yml
site_name: OWI-metadatabase SDK
site_description: Core SDK for OWI-Lab metadatabase geometry and location data
site_author: OWI-Lab
site_url: https://owi-lab.github.io/owi-metadatabase/
repo_url: https://github.com/OWI-Lab/owi-metadatabase
repo_name: OWI-Lab/owi-metadatabase
edit_uri: edit/main/docs/

theme:
  name: material
  custom_dir: docs/overrides
  logo: assets/LogoOWI.png
  favicon: assets/favicon.png
  palette:
    # Light mode
    - media: "(prefers-color-scheme: light)"
      scheme: default
      primary: blue
      accent: indigo
      toggle:
        icon: material/brightness-7
        name: Switch to dark mode
    # Dark mode
    - media: "(prefers-color-scheme: dark)"
      scheme: slate
      primary: blue
      accent: indigo
      toggle:
        icon: material/brightness-4
        name: Switch to light mode
  features:
    - navigation.instant
    - navigation.tracking
    - navigation.tabs
    - navigation.tabs.sticky
    - navigation.sections
    - navigation.expand
    - navigation.top
    - navigation.footer
    - toc.follow
    - toc.integrate
    - search.suggest
    - search.highlight
    - search.share
    - content.code.copy
    - content.code.annotate

plugins:
  - search:
      lang: en
  - mkdocstrings:
      handlers:
        python:
          options:
            docstring_style: numpy
            show_source: true
            show_root_heading: true
            show_root_full_path: false
            show_object_full_path: false
            show_category_heading: true
            show_if_no_docstring: false
            inherited_members: true
            members_order: source
            separate_signature: true
            unwrap_annotated: true
            merge_init_into_class: true
            docstring_section_style: table
            signature_crossrefs: true
  - git-revision-date-localized:
      enable_creation_date: true
      type: timeago
  - minify:
      minify_html: true
  - mkdocs-jupyter:
      include_source: true
      execute: false

markdown_extensions:
  - admonition
  - pymdownx.details
  - pymdownx.superfences:
      custom_fences:
        - name: mermaid
          class: mermaid
          format: !!python/name:pymdownx.superfences.fence_code_format
  - pymdownx.highlight:
      anchor_linenums: true
      line_spans: __span
      pygments_lang_class: true
  - pymdownx.inlinehilite
  - pymdownx.snippets
  - pymdownx.tabbed:
      alternate_style: true
  - pymdownx.arithmatex:
      generic: true
  - attr_list
  - md_in_html
  - tables
  - footnotes
  - toc:
      permalink: true

extra:
  version:
    provider: mike
  social:
    - icon: fontawesome/brands/github
      link: https://github.com/OWI-Lab
    - icon: fontawesome/brands/python
      link: https://pypi.org/project/owi-metadatabase/

nav:
  - Home: index.md
  - Getting Started:
      - Installation: getting-started/installation.md
      - Quick Start: getting-started/quickstart.md
      - Basic Examples: getting-started/examples.md
  - User Guide:
      - Overview: user-guide/index.md
      - Geometry Module: user-guide/geometry.md
      - Locations Module: user-guide/locations.md
      - API Authentication: user-guide/authentication.md
  - API Reference:
      - Overview: api/index.md
      - Geometry:
          - I/O: api/geometry/io.md
          - Processing: api/geometry/processing.md
          - Structures: api/geometry/structures.md
      - Locations:
          - I/O: api/locations/io.md
  - Examples:
      - Notebooks: examples/index.md
      - Geometry Examples: examples/geometry_examples.ipynb
      - Locations Examples: examples/locations_examples.ipynb
  - Development:
      - Contributing: development/contributing.md
      - Testing: development/testing.md
      - Documentation: development/documentation.md
      - Namespace Packages: development/namespace_packages.md
      - Release Process: development/release.md
  - About:
      - License: about/license.md
      - Changelog: about/changelog.md
      - Authors: about/authors.md
```

### 4.2 Documentation Structure

```text
docs/
├── index.md                     # Home page
├── getting-started/
│   ├── installation.md
│   ├── quickstart.md
│   └── examples.md
├── user-guide/
│   ├── index.md
│   ├── geometry.md
│   ├── locations.md
│   └── authentication.md
├── api/
│   ├── index.md
│   ├── geometry/
│   │   ├── io.md
│   │   ├── processing.md
│   │   └── structures.md
│   └── locations/
│       └── io.md
├── examples/
│   ├── index.md
│   ├── geometry_examples.ipynb
│   └── locations_examples.ipynb
├── development/
│   ├── contributing.md
│   ├── testing.md
│   ├── documentation.md
│   ├── namespace_packages.md
│   └── release.md
├── about/
│   ├── license.md
│   ├── changelog.md
│   └── authors.md
├── assets/
│   ├── LogoOWI.png
│   └── favicon.png
└── overrides/                   # Theme customization
```

### 4.3 NumPy Docstring Standards

All docstrings follow NumPy convention with **comprehensive doctest examples**. See section 3.2 for detailed requirements.

### 4.4 Documentation Build & Deployment (Invoke)

- [x] Update docs.py for MkDocs:

  ```python
  @task
  def build(c):
      """Build MkDocs documentation."""
      c.run("mkdocs build --strict", pty=PTY)

  @task
  def serve(c):
      """Serve MkDocs documentation with hot reload."""
      c.run("mkdocs serve", pty=PTY)

  @task
  def deploy(c):
      """Deploy documentation to GitHub Pages."""
      c.run("mkdocs gh-deploy --force", pty=PTY)

  @task(default=True)
  def all(c):
      """Build and serve documentation."""
      build(c)
      serve(c)
  ```

- [x] Configure GitHub Pages deployment via invoke
- [x] Add versioning with `mike` for multi-version docs

## 🔍 Phase 5: Code Quality & Type Safety

### 5.1 Type Hints with Ty

- [x] Add comprehensive type hints to all functions
- [x] Use modern typing features:

  ```python
  from typing import TYPE_CHECKING
  from collections.abc import Sequence

  if TYPE_CHECKING:
      from pathlib import Path
      import pandas as pd
  ```

- [x] Add `py.typed` marker
- [x] Configure ty (replace mypy in quality.py):

  ```python
  @task
  def ty_check(c):
      """Run static type checking: ty."""
      tmp_str = colorize("Running ty...\n", color=Color.HEADER, bold=True)
      print(f"{tmp_str}")
      c.run("ty check src/owi/metadatabase tests", warn=True, pty=PTY)
  ```

### 5.2 Ruff Configuration (Updated)

- [x] Ruff configuration verified in pyproject.toml

```toml
[tool.ruff]
line-length = 120
target-version = "py39"

[tool.ruff.lint]
select = ["E", "W", "F", "I", "D", "UP", "B", "C4", "SIM", "TCH", "RUF"]
ignore = []

[tool.ruff.lint.pydocstyle]
convention = "numpy"

[tool.ruff.lint.isort]
known-first-party = ["owi.metadatabase"]
```

### 5.3 Invoke Tasks Integration

Update quality.py to replace black/flake8/pylint/mypy with ruff/ty:

```python
@task
def format(c):
    """Run code formatter: ruff."""
    c.run("ruff format src tests", pty=PTY)

@task
def lint(c):
    """Run linter: ruff."""
    c.run("ruff check src tests", pty=PTY)

@task
def ty_check(c):
    """Run type checker: ty."""
    c.run("ty check src tests", warn=True, pty=PTY)

@task(post=[format, lint, ty_check], default=True)
def all(c):
    """Run all quality checks."""
```

- [x] Update invoke quality tasks for ruff/ty
- [x] Validate invoke QA with ruff/ty

### 5.4 Pre-commit Hooks

- [x] Pre-commit hooks updated for ruff and ty

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.12.9
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format

  - repo: local
    hooks:
      - id: ty
        name: ty type checker
        entry: uv run ty check
        language: system
        types: [python]
        pass_filenames: false
```

## 🚀 Phase 6: CI/CD & Release

### 6.1 GitHub Actions Workflows (Using Invoke)

- [x] Update CI workflow to use uv + invoke for test/quality/docs

```yaml
# .github/workflows/ci.yml
name: CI

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.9", "3.10", "3.11", "3.12", "3.13"]

    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}

      - name: Install uv
        uses: astral-sh/setup-uv@v4

      - name: Install dependencies
        run: uv sync --dev

      - name: Run tests via invoke
        run: uv run invoke test.run

      - name: Upload coverage
        uses: codecov/codecov-action@v4
        if: matrix.python-version == '3.11'

  quality:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Install uv
        uses: astral-sh/setup-uv@v4

      - name: Install dependencies
        run: uv sync --dev

      - name: Run quality checks via invoke
        run: uv run invoke qa.all

  docs:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Install uv
        uses: astral-sh/setup-uv@v4

      - name: Install dependencies
        run: uv sync --dev

      - name: Build docs via invoke
        run: uv run invoke docs.build

      - name: Upload docs artifact
        uses: actions/upload-artifact@v4
        with:
          name: docs
          path: site/
```

### 6.2 CI Workflow Hardening

- [x] Add concurrency group to cancel in-progress runs on new commits
- [x] Enable pip/uv cache for dependency install speed
- [x] Pin action versions and enforce minimum permissions
- [x] Upload coverage report artifact for post-run inspection

### 6.3 Documentation Deployment Workflow

- [x] Add docs workflow to build and publish versioned site with `mike` to GitHub Pages
- [x] Deploy only on tagged releases and main branch updates
- [x] Keep docs build strict (`mkdocs build --strict`) in CI
- [x] Store docs preview as artifact for pull requests

### 6.4 PyPI Publishing

```yaml
# .github/workflows/release.yml
name: Publish to PyPI

on:
  release:
    types: [published]

jobs:
  pypi-publish:
    runs-on: ubuntu-latest
    permissions:
      id-token: write
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v4
      - run: uv build
      - uses: pypa/gh-action-pypi-publish@release/v1
```

### 6.5 Version Management

- [ ] Use `uv version` for version bumps
- [ ] Dynamic version from `_version.py`
- [ ] Automated changelog generation

## 📦 Phase 7: Namespace Package Extensibility & Copier Template

### 7.1 Create Copier Template

Create a Copier template repository for generating extension packages:

**Template Repository**: `owi-metadatabase-extension-template`

```yaml
# copier.yml
_subdirectory: template

_templates_suffix: .jinja
_answers_file: .copier-answers.yml

project_name:
  type: str
  help: What is the extension name? (e.g., 'fatigue', 'soil', 'results')
  validator: >-
    {% if not project_name %}
    Extension name is required
    {% endif %}

project_slug:
  type: str
  default: "{{ project_name | lower | replace(' ', '-') }}"
  help: Project slug for package name

project_description:
  type: str
  help: Short description of the extension
  default: "{{ project_name }} extension for OWI Metadatabase SDK"

author_name:
  type: str
  help: Author name
  default: "OWI-Lab"

author_email:
  type: str
  help: Author email
  default: "info@owi-lab.be"

python_version:
  type: str
  help: Minimum Python version
  default: "3.9"
  choices:
    - "3.9"
    - "3.10"
    - "3.11"
    - "3.12"

base_package_version:
  type: str
  help: Minimum owi-metadatabase version required
  default: "0.1.0"

include_visualization:
  type: bool
  help: Include visualization dependencies (plotly, matplotlib)?
  default: false

include_numerical:
  type: bool
  help: Include numerical dependencies (scipy, scikit-learn)?
  default: false
```

**Template Structure**:

```text
owi-metadatabase-ext-sdk-tpl/
├── copier.yml
├── README.md
└── template/
    ├── .github/
    │   └── workflows/
    │       ├── ci.yml.jinja
    │       └── release.yml.jinja
    ├── .gitignore
    ├── .pre-commit-config.yaml.jinja
    ├── .python-version
    ├── LICENSE
    ├── README.md.jinja
    ├── pyproject.toml.jinja
    ├── mkdocs.yml.jinja
    ├── invoke.yaml.jinja
    ├── docs/
    │   ├── index.md.jinja
    │   ├── getting-started/
    │   ├── api/
    │   └── examples/
    ├── src/
    │   └── owi/
    │       └── metadatabase/
    │           └── {{ project_slug }}/
    │               ├── __init__.py.jinja
    │               └── io.py.jinja
    ├── tests/
    │   ├── __init__.py
    │   ├── conftest.py.jinja
    │   └── {{ project_slug }}/
    │       ├── __init__.py
    │       └── test_io.py.jinja
    └── tasks/
        ├── __init__.py
        ├── test.py
        ├── quality.py
        └── docs.py
```

**Key Template Files**:

`template/pyproject.toml.jinja`:

```toml
[project]
name = "owi-metadatabase-{{ project_slug }}"
version = "0.1.0"
description = "{{ project_description }}"
authors = [
    { name = "{{ author_name }}", email = "{{ author_email }}" }
]
readme = "README.md"
license = { file = "LICENSE" }
requires-python = ">={{ python_version }},<3.14"

dependencies = [
    "owi-metadatabase>={{ base_package_version }}",
    {% if include_numerical %}
    "scipy>=1.14.0",
    "scikit-learn>=1.3.0",
    {% endif %}
    {% if include_visualization %}
    "plotly>=5.19.0",
    "matplotlib>=3.9.0",
    {% endif %}
]

[dependency-groups]
dev = [
    {include-group = "test"},
    {include-group = "lint"},
    {include-group = "typing"},
    {include-group = "docs"},
    {include-group = "dev-tools"},
]
test = [
    "pytest>=8.4.0",
    "pytest-cov>=7.0.0",
    "pytest-mock>=3.15.0",
]
lint = ["ruff>=0.12.9"]
typing = ["ty>=0.2.0", "types-requests>=2.32.0"]
docs = [
    "mkdocs>=1.6.0",
    "mkdocs-material>=9.5.0",
    "mkdocstrings[python]>=0.27.0",
]
dev-tools = ["invoke>=2.2.0", "pre-commit>=3.0.0"]

[build-system]
requires = ["hatchling>=1.25.0"]
build-backend = "hatchling.build"

[tool.hatch.build.targets.wheel]
packages = ["src/owi"]

[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = [
    "-v",
    "--cov=src/owi/metadatabase/{{ project_slug }}",
    "--doctest-modules",
]

[tool.ruff]
line-length = 120
target-version = "py{{ python_version | replace('.', '') }}"

[tool.ruff.lint]
select = ["E", "W", "F", "I", "D", "UP", "B", "C4", "SIM"]

[tool.ruff.lint.pydocstyle]
convention = "numpy"

[tool.ruff.lint.isort]
known-first-party = ["owi.metadatabase.{{ project_slug }}"]
```

`template/src/owi/metadatabase/{{ project_slug }}/__init__.py.jinja`:

```python
"""{{ project_description }}."""

__version__ = "0.1.0"

# Import public API
from .io import {{ project_name }}API

__all__ = ["{{ project_name }}API"]
```

### 7.2 Usage of Copier Template

**Creating a new extension package**:

```bash
# Install copier
uv tool install copier

# Generate new extension package
copier copy gh:OWI-Lab/owi-metadatabase-extension-template owi-metadatabase-fatigue

# Answer prompts:
# project_name: fatigue
# project_description: Fatigue analysis for OWI Metadatabase
# include_numerical: Yes
# include_visualization: Yes

# Initialize the new package
cd owi-metadatabase-fatigue
uv sync --dev
uv run invoke test.run
uv run invoke docs.build
```

### 7.3 Documentation for Extensions

Create `docs/development/namespace_packages.md`:

```markdown
# Creating Extension Packages

## Using the Copier Template

The OWI Metadatabase SDK uses a namespace package structure that allows
for modular extensions. To create a new extension:

1. Install copier: `uv tool install copier`
2. Generate your extension:
   `copier copy gh:OWI-Lab/owi-metadatabase-ext-sdk-tpl owi-metadatabase-<name>-sdk`
3. Follow the prompts to customize your package

## Import Patterns

After installing both base and extension packages:

```python
# Base package
from owi.metadatabase.geometry import load_geometry
from owi.metadatabase.locations import LocationsAPI

# Extension package (fatigue)
from owi.metadatabase.fatigue import FatigueAPI

# Extension package (soil)
from owi.metadatabase.soil import SoilAPI
```

## PEP 420 Namespace Structure

The namespace merging works because:

- No `__init__.py` in `src/owi/` directory
- Each package contributes to `owi.metadatabase` namespace
- Python automatically merges the namespaces

## Testing Namespace Imports

Verify namespace package structure:

```python
import owi.metadatabase
# Should not have __file__ attribute (namespace package)
assert not hasattr(owi.metadatabase, '__file__')
```

### 7.4 Validation Tests

```python
# tests/test_namespace.py
def test_namespace_package_structure():
    """Verify owi.metadatabase is a proper namespace package."""
    import owi.metadatabase
    # Namespace packages don't have __file__
    assert not hasattr(owi.metadatabase, '__file__')

def test_base_modules_importable():
    """Verify base modules are accessible."""
    from owi.metadatabase import geometry, locations
    assert geometry is not None
    assert locations is not None
```

## 🎯 Phase 8: Migration Execution & Validation

### 8.1 Pre-Migration Checklist

- [ ] Tag current version as `v0.10.6-legacy`
- [ ] Create migration branch: `feature/namespace-package`
- [ ] Backup test data
- [ ] Document breaking changes

### 8.2 Migration Execution Order

1. [ ] Phase 1: Restructure code
2. [ ] Phase 2: Update build system (pyproject.toml, uv)
3. [ ] Phase 3: Update tests (mirror structure + extensive doctest)
4. [ ] Phase 4: Rebuild docs with MkDocs
5. [ ] Phase 5: Code quality (ty, ruff)
6. [ ] Phase 6: CI/CD updates (invoke-based)
7. [ ] Phase 7: Create Copier template

### 8.3 Validation Checklist

- [ ] All tests pass on Python 3.9-3.13
- [ ] Documentation builds without warnings: `invoke docs.build`
- [ ] Package installs correctly: `uv pip install -e .`
- [ ] Namespace imports work: `from owi.metadatabase.geometry.io import GeometryAPI`
- [x] Type checking passes: `invoke qa.ty`
- [ ] Coverage ≥90%
- [ ] All public functions have extensive doctest examples
- [ ] Test package build: `uv build`
- [ ] Invoke tasks work: `invoke test.all`, `invoke qa.all`, `invoke docs.all`

## Import Changes

### Old Imports (v0.10.x)

```python
from owimetadatabase_preprocessor.geometry import load_geometry
from owimetadatabase_preprocessor.locations.io import LocationsAPI
```

### New Imports (v0.11.0+)

```python
from owi.metadatabase.geometry.io import GeometryAPI
from owi.metadatabase.locations.io import LocationsAPI
```

## Removed Modules

- `fatigue` → Separate package `owi-metadatabase-fatigue` (TBD)
- `soil` → Separate package `owi-metadatabase-soil` (TBD)
- `results` → Removed (functionality consolidated elsewhere)

## New Features

- ✨ Namespace package architecture
- ✨ Extensive doctest coverage
- ✨ MkDocs documentation with Material theme
- ✨ Invoke task automation
- ✨ Ty type checking

## ⚠️ Risk Assessment

| Risk | Impact | Mitigation |
| - | - | - |
| Breaking changes for existing users | **High** | Clear migration guide, detailed changelog |
| Namespace import issues | **Medium** | Comprehensive testing, PEP 420 compliance |
| Dependency conflicts | **Medium** | UV lock files, matrix testing |
| Doctest maintenance overhead | **Medium** | Clear contributor guidelines, CI enforcement |
| MkDocs learning curve | **Low** | Simple markdown, excellent docs |

## 🎁 Nice-to-Have Features

- [ ] **Auto-generated changelog** using `git-cliff`
- [ ] **Codecov integration** for coverage visualization
- [ ] **Dependabot** for automated dependency updates
- [ ] **Security scanning** with `bandit`
- [ ] **Performance benchmarks** using `pytest-benchmark`
- [ ] **API versioning** strategy (semantic versioning)
- [ ] **Contributor guide** with development setup
- [ ] **Issue/PR templates** for GitHub
- [ ] **Release notes automation** via GitHub releases
- [ ] **Docker images** for reproducible environments
- [ ] **Binder integration** for interactive docs
- [ ] **Renovate bot** for dependency updates
- [ ] **Social preview cards** for docs pages

## ✅ Acceptance Criteria

- [x] Package installable as `owi-metadatabase`
- [x] Imports work: `from owi.metadatabase.geometry.io import GeometryAPI`
- [x] Future extensibility: Copier template functional
- [x] Tests: ≥90% coverage, pytest + **extensive** doctest
- [x] Docs: MkDocs Material theme, auto-generated API
- [x] CI/CD: Invoke-based workflows, automated releases
- [x] Type-safe: Full type hints, ty compliance
- [x] Modern tooling: UV + invoke for all workflows
- [x] Test structure mirrors source structure exactly

## 📞 Next Steps

1. **Review & Approve** - Confirm this updated plan meets requirements
2. **Create GitHub Project** - Track progress with issues/milestones
3. **Begin Implementation** - Start with Phase 1 restructuring

Ready to proceed with implementation?
