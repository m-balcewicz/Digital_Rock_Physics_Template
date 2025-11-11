"""
Effective Medium Models
=======================

Physics-based models for computing effective properties of composite media.

This submodule contains implementations of effective medium theories that
calculate bulk properties from constituent components and microstructure.

Available Models
----------------
- Backus averaging: Effective properties of finely layered VTI media
- Gassmann fluid substitution: Predicting fluid effects on seismic velocities
- [Future] Self-consistent approximation
- [Future] Differential effective medium (DEM)
- [Future] Kuster-Toksöz inclusions
- [Future] Hudson crack models

Quick Reference
---------------
```python
from drp_template.compute.rockphysics.effective_medium import (
    backus_average,
    thomsen_params,
    vti_velocity_vs_angle
)

# Two-layer Backus averaging (Calcite + Shale)
Vp = [5200, 2900]
Vs = [2700, 1400]
rho = [2450, 2340]
d = [0.75, 0.5]

results = backus_average(Vp, Vs, rho, d, angle_deg=0, verbose=True)

# Calculate Thomsen anisotropy parameters
thomsen = thomsen_params(
    A=results['A'], C=results['C'], F=results['F'],
    D=results['D'], M=results['M']
)

# Calculate velocities vs propagation angle
angles, Vp_angles, Vsv, Vsh = vti_velocity_vs_angle(
    A=results['A'], C=results['C'], D=results['D'],
    F=results['F'], M=results['M'], rho_eq=results['rho_eq']
)

# Multi-layer example (5 alternating layers)
Vp_5 = [4500, 2900, 4500, 2900, 4500]
Vs_5 = [2800, 1400, 2800, 1400, 2800]
rho_5 = [2500, 2340, 2500, 2340, 2500]
d_5 = [0.8, 0.4, 0.8, 0.4, 0.8]

results_5 = backus_average(Vp_5, Vs_5, rho_5, d_5)
```
    D=results['D'], M=results['M']
)
```

References
----------
- Backus, G. E. (1962): Long-wave elastic anisotropy produced by horizontal layering
- Thomsen, L. (1986): Weak elastic anisotropy
- Mavko, G., Mukerji, T., Dvorkin, J. (2020): The Rock Physics Handbook
"""

from .backus import backus_average, thomsen_params, vti_velocity_vs_angle
from .gassmann import gassmann_fluid_substitution

__all__ = [
    'backus_average',
    'thomsen_params',
    'vti_velocity_vs_angle',
    'gassmann_fluid_substitution',
]
