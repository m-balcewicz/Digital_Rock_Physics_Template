# Digital Rock Physics Template Documentation

Welcome to the **Digital Rock Physics Template** documentation!

This package provides tools for analyzing and visualizing 3D digital rock CT/microCT data, with a focus on:
- Multi-format data import (RAW, TIFF, MATLAB)
- Image processing and visualization
- Phase analysis and segmentation
- Elastic property calculations
- Seismic modeling

```{note}
This is **beta software** (v0.1.0b1). The API is stabilizing but may still change; see `RELEASE_NOTES.md` for migration guidance.
```

## Quick Start

### Installation

```bash
pip install -e .
```

### Basic Usage

```python
import drp_template.io as io
import drp_template.image as image
import drp_template.tools as tools
from drp_template.model import binary_2d, binary_3d
from drp_template.compute.rockphysics.effective_medium import backus_average, thomsen_params

# Import a raw file
data = io.import_model(
    file_path='data.raw',
    dtype='uint8',
    **dimensions**={'nz': 400, 'ny': 400, 'nx': 400}
)

# Visualize a slice
fig, ax, pcm = image.ortho_slice(
    data=data,
    paramsfile='data.json',
    plane='xy'
)

# Get model properties
props = tools.get_model_properties(
    filepath='data.raw',
    dimensions={'nz': 400, 'ny': 400, 'nx': 400},
    verbose=True
)

# Create a quick synthetic 2D binary microstructure (periodic)
synthetic2d = binary_2d(200, 200, num_inclusions=12, periodic=True, random_orientation=True)

# Rock physics: Backus averaging + Thomsen parameters for two layers
backus = backus_average(
    Vp_layers=[5200, 2900], Vs_layers=[2700, 1400], rho_layers=[2450, 2340], d_layers=[0.75, 0.50]
)
thomsen = thomsen_params(A=backus['A'], C=backus['C'], F=backus['F'], D=backus['D'], M=backus['M'])
print(f"epsilon={thomsen['epsilon']:.4f}, gamma={thomsen['gamma']:.4f}, delta={thomsen['delta']:.4f}")
```

## New in 0.1.0b1 (Highlights)

| Area | Change | Why It Matters |
|------|--------|----------------|
| Rock Physics Layout | Modular subpackages: `mixing/`, `bounds/`, `effective_medium/` | Clear separation of concepts, easier extension |
| Backus Averaging | `backus_average()` + `thomsen_params()` | Production-ready VTI anisotropy workflow |
| Naming Consistency | Descriptive keys (`bulk_modulus_hill`, `shear_modulus_lower`, etc.) | Explicit, self-documenting results |
| Dict Returns | Bounds, mixing, substitution functions return dictionaries | Safer than positional tuples; future-proof |
| Synthetic Models | `binary_2d`, `binary_3d`, periodic generation | Easier RVE creation & testing |
| Optional Extras | Install visualization or VTK support via extras | Lean core; opt-in heavy deps |

### Updated Rock Physics Imports

```python
from drp_template.compute.rockphysics.mixing import brie_fluid_mixing, density_solid_mix
from drp_template.compute.rockphysics.bounds import voigt_reuss_hill_bounds, hashin_shtrikman_bounds
from drp_template.compute.rockphysics.effective_medium import backus_average, gassmann
```

### Optional Dependency Extras

```bash
pip install drp_template[viz]         # Visualization stack
pip install drp_template[vtk]         # VTK export support
pip install drp_template[viz,vtk]     # Both
```

## Contents

```{toctree}
---
maxdepth: 2
caption: User Guide
---
installation
quickstart
tutorials/index
```

```{toctree}
---
maxdepth: 2
caption: API Reference
---
api/io
api/image
api/tools
api/model
api/compute
api/default_params
```

```{toctree}
---
maxdepth: 1
caption: Developer Guide
---
contributing
schema_versioning
changelog
```

## Indices and tables

* {ref}`genindex`
* {ref}`modindex`
* {ref}`search`
