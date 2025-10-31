# Digital Rock Physics Template Documentation

Welcome to the **Digital Rock Physics Template** documentation!

This package provides tools for analyzing and visualizing 3D digital rock CT/microCT data, with a focus on:
- Multi-format data import (RAW, TIFF, MATLAB)
- Image processing and visualization
- Phase analysis and segmentation
- Elastic property calculations
- Seismic modeling

```{note}
This is **alpha software** (v0.1.0-alpha). The API may change in future releases.
```

## Quick Start

### Installation

```bash
pip install -e .
```

### Basic Usage

```python
import drp_template.input_output as io
import drp_template.image as image
import drp_template.tools as tools

# Import a raw file
data = io.import_model(
    file_path='data.raw',
    dtype='uint8',
    dimensions={'nz': 400, 'ny': 400, 'nx': 400}
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
api/input_output
api/image
api/tools
api/math
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
