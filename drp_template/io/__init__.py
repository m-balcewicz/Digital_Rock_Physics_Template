"""
I/O Module
==========

Input/output functions for digital rock physics data.

This module provides a clean, organized interface for reading and writing
digital rock models in various file formats. All functions automatically
handle metadata, parameter files, and data validation.

Structure
---------
- readers: Import functions for various file formats
- writers: Export functions for data and headers
- utils: Internal helper functions
 - vtk: VTK export (.vti) and ParaView utilities

Supported Formats
-----------------
**Import:**
- Raw binary files (.raw, .bin, etc.)
- MATLAB .mat files
- TIFF image sequences
- Single 3D TIFF files

**Export:**
- Raw binary files with JSON metadata
- SEPlib header files

Quick Start
-----------
```python
import drp_template.io as io

# Import a raw binary file
data = io.import_model(
    'sample.raw',
    dtype='uint8',
    voxel_size=5.0,
    dimensions={'nx': 400, 'ny': 400, 'nz': 400}
)

# Import TIFF sequence
volume = io.import_tiff_sequence(
    'path/to/tiff_folder',
    dtype='uint8',
    voxel_size=2.5
)

# Export with labels
io.export_model(
    filename='binary_sample',
    data=data,
    voxel_size=5.0,
    labels={0: 'Pore', 1: 'Solid'}
)
```

Functions
---------
**Readers:**
- import_model: Import raw binary files
- loadmat: Load MATLAB .mat files
- import_tiff_sequence: Import TIFF image sequences
- import_tif_model: Import single 3D TIFF files

**Writers:**
- export_model: Export to raw binary with JSON metadata
- export_header: Export SEPlib header

Notes
-----
All import functions:
- Automatically create parameter JSON files with metadata
- Validate binary data (check for binary/labeled data)
- Reorient volumes to package standard: (nx, ny, nz)

All export functions:
- Create validated parameter JSON files
- Include comprehensive metadata
- Calculate and store file sizes
"""

# Import all public functions
from .readers import (
    import_model,
    loadmat,
    import_tiff_sequence,
    import_tif_model,
)

from .writers import (
    export_model,
    export_header,
)

from .utils import (
    open_in_paraview,
)

__all__ = [
    # Readers
    'import_model',
    'loadmat',
    'import_tiff_sequence',
    'import_tif_model',
    # Writers
    'export_model',
    'export_header',
    # VTK / ParaView
    'open_in_paraview',
]
