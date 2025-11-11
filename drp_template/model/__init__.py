"""
Digital Rock Physics Template - Model Generation Package

This package provides functions for generating synthetic binary models with
ellipsoidal/elliptical inclusions. Use these to create digital rock physics
models for testing, validation, and research.

Available Functions
-------------------
Model Generation:
- binary_2d: Generate 2D models with elliptical inclusions
- binary_3d: Generate 3D models with ellipsoidal inclusions

Model Utilities:
- get_dim: Extract and validate model dimensions
- reshape: Reorder model axes to (nx, ny, nz)
- subvolume: Extract and save centered subvolumes

Examples
--------
>>> from drp_template.model import binary_2d, binary_3d
>>> 
>>> # Create a 2D model
>>> data_2d = binary_2d(nx=200, ny=200, num_inclusions=10, seed=42)
>>> 
>>> # Create a 3D model
>>> data_3d = binary_3d(nx=100, ny=100, nz=100, num_inclusions=15, seed=42)
>>> 
>>> # Extract a subvolume
>>> from drp_template.model import subvolume
>>> subvol = subvolume(data_3d, set_subvolume=50, 
...                    name_subvolume='test', voxel_size=5.0)
"""

from drp_template.model.generators import (
    binary_2d,
    binary_3d,
    binary_vti,
)

from drp_template.model.utils import (
    get_dim,
    reshape,
    subvolume,
)

__all__ = [
    'binary_2d',
    'binary_3d',
    'binary_vti',
    'get_dim',
    'reshape',
    'subvolume',
]
