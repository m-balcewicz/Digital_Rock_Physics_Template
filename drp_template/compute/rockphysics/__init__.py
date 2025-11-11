"""
Rock Physics Theory Module
===========================

Classical rock physics models and theoretical frameworks.

This module contains implementations of fundamental rock physics theories
including effective medium models, elastic bounds, fluid substitution, and
mixing laws.

Submodules
----------
effective_medium/ : Backus averaging, Gassmann fluid substitution, VTI anisotropy
mixing/           : Density mixing, fluid mixing (Brie, Wood), volume fraction utilities
bounds/           : Voigt-Reuss-Hill and Hashin-Shtrikman elastic bounds
isotropic         : Elastic moduli conversions and seismic velocities (isotropic media)

Quick Reference
---------------
```python
import drp_template.compute.rockphysics as rp

# Effective medium models
from drp_template.compute.rockphysics.effective_medium import (
    backus_average,           # VTI anisotropy from layering
    thomsen_params,           # Thomsen anisotropy parameters
    vti_velocity_vs_angle,    # Phase velocities vs angle
    gassmann_fluid_substitution  # Gassmann fluid substitution
)

# Mixing utilities
from drp_template.compute.rockphysics.mixing import (
    density_solid_mix,      # Solid density mixing
    density_fluid_mix,      # Fluid density mixing
    brie_fluid_mixing,      # Brie's empirical fluid law
    wood_fluid_mixing,      # Wood's equation for fluid suspensions
    get_normalized_f_solid  # Normalize solid fractions
)

# Elastic bounds
from drp_template.compute.rockphysics.bounds import (
    voigt_reuss_hill_bounds,  # VRH bounds and average
    hashin_shtrikman_bounds,  # Narrowest possible bounds
    voigt_bound,              # Upper bound
    reuss_bound,              # Lower bound
    hill_average              # VRH average
)

# Elastic properties (isotropic media)
from drp_template.compute.rockphysics.isotropic import (
    elastic_moduli,
    seismic_velocity
)

# Elastic conversions (simple parameter-to-parameter)
from drp_template.compute.rockphysics.isotropic import (
    poisson,       # K, G → ν
    youngs,        # K, G → E
    lame_lambda,   # K, G → λ
    bulk,          # E, ν → K
    shear          # E, ν → G
)

# Example usage:
# >>> from drp_template.compute import GPa2Pa
# >>> K = GPa2Pa(37)  # Convert 37 GPa to Pa
# >>> G = GPa2Pa(44)  # Convert 44 GPa to Pa
# >>> nu = poisson(K, G)
# >>> E = youngs(K, G)
# >>> K_back = bulk(E, nu)
# >>> G_back = shear(E, nu)

# Fluid substitution
from drp_template.compute.rockphysics.effective_medium import gassmann_fluid_substitution
from drp_template.compute.rockphysics.mixing import wood_fluid_mixing
```

References
----------
- Mavko, G., Mukerji, T., Dvorkin, J. (2020): The Rock Physics Handbook
- Backus, G. E. (1962): Long-wave elastic anisotropy produced by horizontal layering
- Thomsen, L. (1986): Weak elastic anisotropy
- Hashin & Shtrikman (1963): Variational bounds for elastic behavior
- Brie et al. (1995): Fluid mixing law for patchy mixtures

Author
------
Martin Balcewicz (martin.balcewicz@rockphysics.org)
"""

# Import from submodules
from .effective_medium import (
    backus_average,
    thomsen_params,
    vti_velocity_vs_angle,
    gassmann_fluid_substitution,
)

from .mixing import (
    density_solid_mix,
    density_fluid_mix,
    brie_fluid_mixing,
    wood_fluid_mixing,
    get_normalized_f_solid,
)

from .bounds import (
    voigt_reuss_hill_bounds,
    hashin_shtrikman_bounds,
    voigt_bound,
    reuss_bound,
    hill_average,
)

from .isotropic import (
    elastic_moduli,
    seismic_velocity,
    poisson,
    youngs,
    lame_lambda,
    bulk,
    shear,
)

__all__ = [
    # Effective medium models
    'backus_average',
    'thomsen_params',
    'vti_velocity_vs_angle',
    'gassmann_fluid_substitution',
    # Mixing utilities
    'density_solid_mix',
    'density_fluid_mix',
    'brie_fluid_mixing',
    'wood_fluid_mixing',
    'get_normalized_f_solid',
    # Elastic bounds
    'voigt_reuss_hill_bounds',
    'hashin_shtrikman_bounds',
    'voigt_bound',
    'reuss_bound',
    'hill_average',
    # Elastic properties and conversions
    'elastic_moduli',
    'seismic_velocity',
    'poisson',
    'youngs',
    'lame_lambda',
    'bulk',
    'shear',
]
