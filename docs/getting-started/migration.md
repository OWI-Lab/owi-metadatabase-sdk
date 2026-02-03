# Migration Guide: v0.10.x → v0.11.0

This guide helps you migrate from `owi-metadatabase-sdk` v0.10.x to v0.11.0.

## ⚠️ Breaking Changes

### 1. Package Name Change

**PyPI Package Name:**
- Old: `owi-metadatabase-sdk`
- New: `owi-metadatabase`

**Note**: The GitHub repository name remains `owi-metadatabase-sdk`.

### 2. Import Path Changes

All import paths have changed to use the new namespace package structure:

```python
# ❌ Old (v0.10.x)
from owimetadatabase_preprocessor.geometry import GeometryAPI
from owimetadatabase_preprocessor.locations.io import LocationsAPI
from owimetadatabase_preprocessor.geometry.processing import OWT
from owimetadatabase_preprocessor.utility.exceptions import APIConnectionError

# ✅ New (v0.11.0+)
from owi.metadatabase.geometry.io import GeometryAPI
from owi.metadatabase.locations.io import LocationsAPI
from owi.metadatabase.geometry.processing import OWT
from owi.metadatabase._utils.exceptions import APIConnectionError
```

### 3. Removed Modules

The following modules have been removed from the core package and will be released as separate extension packages:

- `fatigue` → `owi-metadatabase-fatigue` (coming soon)
- `soil` → `owi-metadatabase-soil` (coming soon)
- `results` → Functionality consolidated elsewhere

## Migration Steps

### Step 1: Uninstall Old Package

```bash
pip uninstall owi-metadatabase-sdk
```

### Step 2: Install New Package

```bash
pip install owi-metadatabase
```

### Step 3: Update Imports

Use find-and-replace in your codebase:

| Old Import | New Import |
|------------|------------|
| `owimetadatabase_preprocessor.geometry` | `owi.metadatabase.geometry` |
| `owimetadatabase_preprocessor.locations` | `owi.metadatabase.locations` |
| `owimetadatabase_preprocessor.utility` | `owi.metadatabase._utils` |
| `owimetadatabase_preprocessor.io` | `owi.metadatabase.io` |

### Step 4: Update API Imports

```python
# Old
from owimetadatabase_preprocessor.geometry.io import GeometryAPI
from owimetadatabase_preprocessor.locations.io import LocationsAPI

# New
from owi.metadatabase.geometry.io import GeometryAPI
from owi.metadatabase.locations.io import LocationsAPI
```

### Step 5: Update Utility Imports

```python
# Old
from owimetadatabase_preprocessor.utility.exceptions import (
    APIConnectionError,
    DataProcessingError
)
from owimetadatabase_preprocessor.utility.utils import deepcompare

# New
from owi.metadatabase._utils.exceptions import (
    APIConnectionError,
    DataProcessingError
)
from owi.metadatabase._utils.utils import deepcompare
```

## Automated Migration Script

Here's a Python script to help automate the migration:

```python
#!/usr/bin/env python3
"""
Automated migration script for owi-metadatabase v0.11.0
"""
from pathlib import Path
import re

def migrate_file(filepath: Path) -> int:
    """Migrate a single Python file."""
    content = filepath.read_text()
    original = content

    # Replace import paths
    replacements = {
        'owimetadatabase_preprocessor.geometry': 'owi.metadatabase.geometry',
        'owimetadatabase_preprocessor.locations': 'owi.metadatabase.locations',
        'owimetadatabase_preprocessor.utility': 'owi.metadatabase._utils',
        'owimetadatabase_preprocessor.io': 'owi.metadatabase.io',
        'owimetadatabase_preprocessor': 'owi.metadatabase',
    }

    for old, new in replacements.items():
        content = content.replace(old, new)

    if content != original:
        filepath.write_text(content)
        return 1
    return 0

def migrate_project(project_dir: Path) -> None:
    """Migrate all Python files in a project."""
    count = 0
    for filepath in project_dir.rglob('*.py'):
        count += migrate_file(filepath)
    print(f"✓ Migrated {count} files")

if __name__ == '__main__':
    import sys
    project_dir = Path(sys.argv[1] if len(sys.argv) > 1 else '.')
    migrate_project(project_dir)
```

Save this as `migrate.py` and run:

```bash
python migrate.py /path/to/your/project
```

## Testing Your Migration

After migration, run your tests:

```bash
pytest
```

Verify imports work:

```python
import owi.metadatabase
from owi.metadatabase.geometry.io import GeometryAPI
from owi.metadatabase.locations.io import LocationsAPI

print(f"✓ Migration successful! Version: {owi.metadatabase.__version__}")
```

## Key Changes Summary

| Aspect | v0.10.x | v0.11.0 |
|--------|---------|---------|
| PyPI Package | `owi-metadatabase-sdk` | `owi-metadatabase` |
| Import Root | `owimetadatabase_preprocessor` | `owi.metadatabase` |
| Package Type | Regular package | PEP 420 namespace package |
| Fatigue Module | Included | Separate package (future) |
| Soil Module | Included | Separate package (future) |
| Line Length | 127 characters | 120 characters |
| Docstring Style | PEP 257 | NumPy |
| Documentation | Sphinx | MkDocs Material |

## Benefits of v0.11.0

- ✨ **Namespace package architecture** - Modular, extensible design
- 📦 **Cleaner dependencies** - Core package has fewer dependencies
- 📝 **Better documentation** - NumPy-style docstrings with extensive doctests
- 🎨 **Modern tooling** - Built with uv, ruff, and invoke
- 🧪 **Enhanced testing** - Comprehensive doctest coverage
- 📖 **MkDocs documentation** - Beautiful, searchable documentation

## Need Help?

- **[GitHub Issues](https://github.com/OWI-Lab/owi-metadatabase-sdk/issues)** - Report bugs or issues
- **[GitHub Discussions](https://github.com/OWI-Lab/owi-metadatabase-sdk/discussions)** - Ask questions
- **[Documentation](https://owi-lab.github.io/owi-metadatabase-sdk/)** - Full documentation

## Extension Packages (Coming Soon)

Once available, you'll be able to install extension packages:

```bash
# Core package (available now)
pip install owi-metadatabase

# Extension packages (coming soon)
pip install owi-metadatabase-fatigue
pip install owi-metadatabase-soil
```

All packages will work together seamlessly through the namespace package mechanism:

```python
from owi.metadatabase.geometry import GeometryAPI
from owi.metadatabase.fatigue import FatigueAPI  # Future
from owi.metadatabase.soil import SoilAPI        # Future
```
