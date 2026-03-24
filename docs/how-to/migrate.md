# How to migrate from owimetadatabase-preprocessor v0.10.x

This guide helps you migrate from `owimetadatabase-preprocessor` v0.10.x to
`owi-metadatabase` v0.1.0+.

## Step 1: Uninstall the old package

```bash
pip uninstall owimetadatabase-preprocessor
```

## Step 2: Install the new package

```bash
pip install owi-metadatabase
```

## Step 3: Update import paths

All import paths have changed to use the new namespace package structure:

```python
# Old (owimetadatabase-preprocessor v0.10.x)
from owimetadatabase_preprocessor.geometry import GeometryAPI
from owimetadatabase_preprocessor.locations.io import LocationsAPI
from owimetadatabase_preprocessor.geometry.processing import OWT
from owimetadatabase_preprocessor.utility.exceptions import APIConnectionError

# New (owi-metadatabase v0.1.0+)
from owi.metadatabase.geometry.io import GeometryAPI
from owi.metadatabase.locations.io import LocationsAPI
from owi.metadatabase.geometry.processing import OWT
from owi.metadatabase._utils.exceptions import APIConnectionError
```

### Import mapping table

| Old import path | New import path |
|-----------------|-----------------|
| `owimetadatabase_preprocessor.geometry` | `owi.metadatabase.geometry` |
| `owimetadatabase_preprocessor.locations` | `owi.metadatabase.locations` |
| `owimetadatabase_preprocessor.utility` | `owi.metadatabase._utils` |
| `owimetadatabase_preprocessor.io` | `owi.metadatabase.io` |

## Step 4: Verify the migration

```python
import owi.metadatabase
from owi.metadatabase.geometry.io import GeometryAPI
from owi.metadatabase.locations.io import LocationsAPI

print("Migration successful")
```

## Removed modules

The following modules have been extracted into separate extension packages:

- `fatigue` → `owi-metadatabase-fatigue` (coming soon)
- `soil` → [`owi-metadatabase-soil`](https://pypi.org/project/owi-metadatabase-soil/)
- `results` → [`owi-metadatabase-results`](https://pypi.org/project/owi-metadatabase-results/)

## Automated migration script

Save this as `migrate.py` and run it against your project directory:

```python
#!/usr/bin/env python3
"""Automated migration script for owi-metadatabase v0.1.0."""
from pathlib import Path


def migrate_file(filepath: Path) -> int:
    """Migrate a single Python file. Returns 1 if changed, 0 otherwise."""
    content = filepath.read_text()
    original = content

    replacements = {
        "owimetadatabase_preprocessor.geometry": "owi.metadatabase.geometry",
        "owimetadatabase_preprocessor.locations": "owi.metadatabase.locations",
        "owimetadatabase_preprocessor.utility": "owi.metadatabase._utils",
        "owimetadatabase_preprocessor.io": "owi.metadatabase.io",
        "owimetadatabase_preprocessor": "owi.metadatabase",
    }

    for old, new in replacements.items():
        content = content.replace(old, new)

    if content != original:
        filepath.write_text(content)
        return 1
    return 0


def migrate_project(project_dir: Path) -> None:
    """Migrate all Python files in a project."""
    count = sum(migrate_file(fp) for fp in project_dir.rglob("*.py"))
    print(f"Migrated {count} files")


if __name__ == "__main__":
    import sys

    project_dir = Path(sys.argv[1] if len(sys.argv) > 1 else ".")
    migrate_project(project_dir)
```

```bash
python migrate.py /path/to/your/project
```

## Summary of changes

| Aspect | v0.10.x | v0.1.0+ |
|--------|---------|---------|
| PyPI package | `owimetadatabase-preprocessor` | `owi-metadatabase` |
| Import root | `owimetadatabase_preprocessor` | `owi.metadatabase` |
| Package type | Regular package | PEP 420 namespace package |
| Soil module | Included | Separate (`owi-metadatabase-soil`) |
| Fatigue module | Included | Separate (future) |
| Docstring style | PEP 257 | NumPy |
| Documentation | Sphinx | Zensical |
