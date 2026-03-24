# How to install the SDK

## From PyPI

```bash
pip install owi-metadatabase
```

With [uv](https://github.com/astral-sh/uv):

```bash
uv pip install owi-metadatabase
```

## From source (development)

```bash
git clone https://github.com/OWI-Lab/owi-metadatabase-sdk.git
cd owi-metadatabase-sdk
uv sync --dev
```

## Verify the installation

```python
from owi.metadatabase.geometry.io import GeometryAPI
from owi.metadatabase.locations.io import LocationsAPI

print("Installation successful")
```

## Optional extras

### Soil extension

```bash
pip install "owi-metadatabase[soil]"
```

### Documentation tooling

```bash
uv sync --group docs
```

### Full development environment

```bash
uv sync --dev
```

## Troubleshooting

### Import errors after upgrade

Make sure the old package is fully removed before installing the new one:

```bash
pip uninstall owimetadatabase-preprocessor
pip install owi-metadatabase
```

### Namespace package conflicts

If imports fail with `ModuleNotFoundError`, remove stale installations:

```bash
pip uninstall owi-metadatabase-sdk owimetadatabase-preprocessor
pip install owi-metadatabase
```

!!! note
    If you use `zsh`, wrap extras in quotes because `[` and `]` are glob
    characters: `pip install "owi-metadatabase[soil]"`.
