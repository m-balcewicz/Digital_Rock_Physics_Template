"""
Mixing Laws for Rock Physics
=============================

Density mixing, fluid substitution, and volume fraction utilities.

This submodule provides functions for calculating effective properties
of multi-phase mixtures in rock physics applications.

Submodules
----------
density : Density mixing for solids and fluids
fluid : Empirical fluid mixing laws (Brie, Wood, etc.)
utils : Volume fraction normalization utilities

Functions
---------
From density module:
    - density_solid_mix : Effective density of solid mixtures
    - density_fluid_mix : Effective density of fluid mixtures

From fluid module:
    - brie_fluid_mixing : Brie's empirical fluid mixing law
    - wood_fluid_mixing : Wood's equation for fluid suspensions

From utils module:
    - get_normalized_f_solid : Normalize solid fractions based on porosity

Examples
--------
>>> from drp_template.compute.rockphysics.mixing import density_solid_mix
>>> rho_solid = density_solid_mix([0.6, 0.4], [2650, 2710])
>>> print(f"Solid density: {rho_solid:.1f} kg/m³")

>>> from drp_template.compute.rockphysics.mixing import brie_fluid_mixing
>>> k_fluid = brie_fluid_mixing(0.5, 0, 0.5, 2.2e9, 0, 0.01e9)
>>> print(f"Fluid bulk modulus: {k_fluid/1e9:.3f} GPa")

>>> from drp_template.compute.rockphysics.mixing import wood_fluid_mixing
>>> results = wood_fluid_mixing([0.6, 0.4], [2.2e9, 0.01e9], [1000, 1.2])
>>> print(f"Mixture Vp: {results['Vp']:.0f} m/s")

References
----------
- Brie et al. (1995): Shear velocity prediction in porous rocks
- Mavko, G., Mukerji, T., Dvorkin, J. (2020): The Rock Physics Handbook

Author
------
Martin Balcewicz (martin.balcewicz@rockphysics.org)
"""

from .density import density_solid_mix, density_fluid_mix
from .fluid import brie_fluid_mixing, wood_fluid_mixing
from .utils import get_normalized_f_solid

__all__ = [
    # Density mixing
    'density_solid_mix',
    'density_fluid_mix',
    # Fluid mixing laws
    'brie_fluid_mixing',
    'wood_fluid_mixing',
    # Utilities
    'get_normalized_f_solid',
]
