"""
Compute Module
==============

Computational functions for digital rock physics analysis and rock physics theory.

This module provides:
- Core digital image analysis (phase_fractions, porosity)
- Unit conversions (GPa ↔ Pa)
- Wave physics calculations (wavelength, frequency, velocity)
- Rock physics theory submodule (rockphysics)

Structure
---------
- analysis: Core digital analysis functions
- conversions: Unit conversion utilities
- wave: Basic wave equation calculations
- rockphysics/: Rock physics theoretical models (mixing, bounds, elastic, gassmann, wood)

Quick Start
-----------
```python
import drp_template.compute as compute

# Digital analysis
fractions = compute.phase_fractions(data, labels={"0": "Pore", "1": "Quartz"})

# Unit conversions
values_pa = compute.GPa2Pa(37)  # Convert GPa to Pa

# Wave calculations
wavelength = compute.wave.wavelength(velocity=3000, frequency=100)

# Rock physics
from drp_template.compute.rockphysics import hashin_shtrikman_bounds
K_low, K_up, G_up, G_low = hashin_shtrikman_bounds(bulk, shear, fractions)
```
"""

# Core digital analysis
from .analysis import porosity, phase_fractions

# Unit conversions (now public API)
from .conversions import GPa2Pa, Pa2GPa, m2mm, mm2m, m2um, um2m

# Wave physics is accessible as compute.wave
from . import wave

# Rock physics theory is accessible as compute.rockphysics
from . import rockphysics

# CT geometry is accessible as compute.ct_geometry
from .ct import ct_geometry

__all__ = [
    # Core analysis
    'porosity',
    'phase_fractions',
    # Conversions
    'GPa2Pa',
    'Pa2GPa',
    'm2mm',
    'mm2m',
    'm2um',
    'um2m',
    # Submodules
    'wave',
    'rockphysics',
    'ct_geometry',
]