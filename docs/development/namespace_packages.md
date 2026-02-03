# Namespace Packages

This project uses a PEP 420 namespace package layout.

## Key Points

- The `owi` namespace is a native namespace package
- There is no `__init__.py` at the `owi/` root
- Extension packages can contribute additional modules

## Import Pattern

```
from owi.metadatabase.geometry.io import GeometryAPI
from owi.metadatabase.locations.io import LocationsAPI
```

## Validation

```
import owi.metadatabase
assert not hasattr(owi.metadatabase, "__file__")
```
