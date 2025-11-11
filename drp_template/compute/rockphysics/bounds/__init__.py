"""
Elastic Bounds for Rock Physics
================================

Theoretical upper and lower bounds for effective elastic moduli.

This submodule provides functions for calculating bounds on the effective
elastic properties of composite materials without specifying exact geometry.

Submodules
----------
voigt_reuss : Voigt (upper) and Reuss (lower) bounds, Hill average
hashin_shtrikman : Hashin-Shtrikman bounds (narrowest possible)

Functions
---------
From voigt_reuss module:
    - voigt_bound : Upper (Voigt) bound - arithmetic average
    - reuss_bound : Lower (Reuss) bound - harmonic average
    - hill_average : Voigt-Reuss-Hill average
    - voigt_reuss_hill_bounds : Complete VRH bounds and average

From hashin_shtrikman module:
    - hashin_shtrikman_bounds : Narrowest possible bounds

Examples
--------
>>> from drp_template.compute.rockphysics.bounds import voigt_reuss_hill_bounds
>>> bounds = voigt_reuss_hill_bounds(
...     fractions=[0.6, 0.4],
...     bulk_moduli=[37e9, 76e9],
...     shear_moduli=[44e9, 32e9]
... )
>>> print(f"K_hill = {bounds['K_hill']/1e9:.2f} GPa")
>>> print(f"G_hill = {bounds['G_hill']/1e9:.2f} GPa")

>>> from drp_template.compute.rockphysics.bounds import hashin_shtrikman_bounds
>>> hs_bounds = hashin_shtrikman_bounds(
...     fractions=[0.584, 0.146, 0.27],
...     bulk_moduli=[36e9, 75e9, 2.2e9],
...     shear_moduli=[45e9, 31e9, 0]
... )
>>> print(f"K: [{hs_bounds['K_lower']/1e9:.1f}, {hs_bounds['K_upper']/1e9:.1f}] GPa")

Notes
-----
**Bound hierarchy (from widest to narrowest):**

1. **Voigt-Reuss bounds** (widest)
   - No geometric assumptions
   - Simple to calculate
   - Use for quick estimates

2. **Hashin-Shtrikman bounds** (narrowest)
   - Optimal for isotropic composites
   - Requires "well-ordered" materials for optimality
   - Best theoretical bounds without geometry

**When to use which:**

- Use **VRH** for:
  * Quick estimates
  * Educational purposes
  * When HS bounds are not well-defined

- Use **Hashin-Shtrikman** for:
  * Tighter constraints
  * Theoretical analysis
  * Comparison with measurements

References
----------
- Voigt (1889) & Reuss (1929): Upper and lower bounds
- Hill (1952): Averaging procedure
- Hashin & Shtrikman (1963): Variational bounds
- Mavko, G., Mukerji, T., Dvorkin, J. (2020): The Rock Physics Handbook

Author
------
Martin Balcewicz (martin.balcewicz@rockphysics.org)
"""

from .voigt_reuss import (
    voigt_bound,
    reuss_bound,
    hill_average,
    voigt_reuss_hill_bounds
)
from .hashin_shtrikman import hashin_shtrikman_bounds

__all__ = [
    # Voigt-Reuss-Hill
    'voigt_bound',
    'reuss_bound',
    'hill_average',
    'voigt_reuss_hill_bounds',
    # Hashin-Shtrikman
    'hashin_shtrikman_bounds',
]
