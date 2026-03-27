# Extension overview

The core SDK focuses on geometry and location access. Domain-specific
packages are distributed as namespace extensions so you can install only the
capabilities you need and still work under the shared `owi.metadatabase`
import root.

## Why the extensions exist

The OWI Metadatabase spans several data domains with different dependency and
workflow requirements. Keeping those domains in separate packages avoids
forcing every user to install plotting, modeling, or upload dependencies they
do not need.

The currently deployed extras are:

- `soil` for soil data access, processing, and visualization
- `results` for typed result queries, services, and plotting workflows
- `shm` for structural health monitoring queries, typed services, and upload
  orchestration

## Comparison

| Extension | Install through core | Main entry points | Best fit |
| --------- | -------------------- | ----------------- | -------- |
| Soil | `pip install "owi-metadatabase[soil]"` | `SoilAPI`, `SoilDataProcessor`, `SoilPlot` | Geotechnical and soil campaign workflows |
| Results | `pip install "owi-metadatabase[results]"` | `ResultsAPI`, `ResultsService`, `ResultQuery` | Analysis results retrieval, typed result models, and visualization |
| SHM | `pip install "owi-metadatabase[shm]"` | `ShmAPI`, `SensorService`, `SignalService` | Structural health monitoring queries, typed records, and upload pipelines |

## How they fit with the core package

The core package remains the shared base layer. It provides:

- the authentication and request pipeline in `owi.metadatabase.io`
- geometry and locations APIs
- shared exception types and utilities
- the namespace package structure that lets installed extensions coexist

Each extension then builds on that base with its own models, service layer,
and domain workflows.

## Choosing the right package

Use only the core package when you need:

- geometry queries
- location queries
- the shared base API behavior

Add an extra when you also need:

- `soil`: CPTs, boreholes, soil profiles, or soil plotting
- `results`: typed analysis/result retrieval and plotting helpers
- `shm`: sensor and signal retrieval, typed SHM records, or SHM uploads

You can combine extras in one installation:

```bash
pip install "owi-metadatabase[soil,results,shm]"
```

## Documentation map

- [Soil extension docs](https://owi-lab.github.io/owi-metadatabase-soil-sdk/)
- [Results extension docs](https://owi-lab.github.io/owi-metadatabase-results-sdk/)
- [SHM extension docs](https://owi-lab.github.io/owi-metadatabase-shm-sdk/)
- [Namespace packages](namespace-packages.md)
