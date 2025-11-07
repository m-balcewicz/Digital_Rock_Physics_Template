"""
Rock Physics Theory Module
===========================

Classical rock physics models and theoretical frameworks.

This submodule contains implementations of fundamental rock physics theories
including effective medium models, elastic bounds, and fluid substitution.

Submodules
----------
- mixing: Effective medium and mixing laws (Brie, density mixing, elastic bounds)
- bounds: Voigt-Reuss-Hill and Hashin-Shtrikman bounds
- elastic: Elastic moduli conversions and seismic velocities
- gassmann: Gassmann fluid substitution
- wood: Wood's formula for fluid suspensions

Quick Reference
---------------
```python
import drp_template.compute.rockphysics as rp

# Mixing laws
from drp_template.compute.rockphysics.mixing import (
    density_solid_mix,
    density_fluid_mix,
    Brie_law,
    elastic_bounds
)

# Elastic bounds
from drp_template.compute.rockphysics.bounds import (
    hashin_shtrikman_bounds,
    voigt_reuss_hill_bounds
)

# Elastic properties
from drp_template.compute.rockphysics.elastic import (
    elastic_moduli,
    seismic_velocity
)

# Fluid substitution
from drp_template.compute.rockphysics.gassmann import gassmann
from drp_template.compute.rockphysics.wood import wood
```

References
----------
- Mavko, G., Mukerji, T., Dvorkin, J. (2020): The Rock Physics Handbook
- Berryman, J.G. (1993): Mixture theories for rock properties
"""

# Import all functions from submodules
from .mixing import (
    density_solid_mix,
    density_fluid_mix,
    Brie_law,
    get_normalized_f_solid,
    elastic_bounds,
)

from .bounds import (
    hashin_shtrikman_bounds,
    voigt_reuss_hill_bounds,
)

from .elastic import (
    elastic_moduli,
    seismic_velocity,
)

from .gassmann import gassmann

from .wood import wood

__all__ = [
    # Mixing laws
    'density_solid_mix',
    'density_fluid_mix',
    'Brie_law',
    'get_normalized_f_solid',
    'elastic_bounds',
    # Bounds
    'hashin_shtrikman_bounds',
    'voigt_reuss_hill_bounds',
    # Elastic properties
    'elastic_moduli',
    'seismic_velocity',
    # Fluid substitution
    'gassmann',
    'wood',
]
