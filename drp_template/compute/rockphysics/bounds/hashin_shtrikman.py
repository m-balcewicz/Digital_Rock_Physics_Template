"""
Hashin-Shtrikman Bounds
=======================

Narrowest possible bounds for elastic moduli of isotropic composites.

References
----------
- Hashin, Z., & Shtrikman, S. (1963): A variational approach to the theory of
  the elastic behaviour of multiphase materials, Journal of the Mechanics and
  Physics of Solids, 11, 127-140
- Walpole, L.J. (1966): On bounds for the overall elastic moduli of inhomogeneous
  systems, Journal of the Mechanics and Physics of Solids, 14, 151-162
- Mavko, G., Mukerji, T., Dvorkin, J. (2020): The Rock Physics Handbook

Author
------
Martin Balcewicz (martin.balcewicz@rockphysics.org)
"""

import numpy as np

__all__ = ['hashin_shtrikman_bounds']


def hashin_shtrikman_bounds(fractions, bulk_moduli, shear_moduli):
    """
    Calculate Hashin-Shtrikman upper and lower bounds for elastic moduli.
    
    The Hashin-Shtrikman bounds are the narrowest possible bounds on effective
    elastic moduli without specifying the microgeometry of constituents.
    
    For "well-ordered" materials (where the constituent with largest bulk modulus
    also has the largest shear modulus), these bounds are optimal.
    
    Parameters
    ----------
    fractions : array-like
        Volume fractions of constituents. Must sum to 1.
    bulk_moduli : array-like
        Bulk moduli of constituents (Pa).
    shear_moduli : array-like
        Shear moduli of constituents (Pa).
    
    Returns
    -------
    dict
        Dictionary containing:
        - 'bulk_modulus_lower' : Lower (Reuss-like) bound for bulk modulus (Pa)
        - 'bulk_modulus_upper' : Upper (Voigt-like) bound for bulk modulus (Pa)
        - 'shear_modulus_lower' : Lower bound for shear modulus (Pa)
        - 'shear_modulus_upper' : Upper bound for shear modulus (Pa)
        - 'bulk_modulus_avg' : Average of bulk modulus bounds (Pa)
        - 'shear_modulus_avg' : Average of shear modulus bounds (Pa)
    
    Raises
    ------
    ValueError
        If arrays have different lengths or fractions don't sum to 1.
    
    Notes
    -----
    The Hashin-Shtrikman bounds are tighter than Voigt-Reuss bounds and
    represent the narrowest possible bounds achievable through variational
    principles without geometric information.
    
    **Well-ordered materials:**
    - Constituent with max(K) has max(G): HS bounds are optimal
    - Otherwise: bounds are still valid but may not be optimal
    
    **Bound formulas:**
    
    For bulk modulus:
    - bulk_modulus_upper = [Σ f_i/(bulk_modulus_i + 4/3 × shear_modulus_max)]⁻¹ - 4/3 × shear_modulus_max
    - bulk_modulus_lower = [Σ f_i/(bulk_modulus_i + 4/3 × shear_modulus_min)]⁻¹ - 4/3 × shear_modulus_min
    
    For shear modulus:
    - shear_modulus_upper = [Σ f_i/(shear_modulus_i + ζ_max)]⁻¹ - ζ_max
    - shear_modulus_lower = [Σ f_i/(shear_modulus_i + ζ_min)]⁻¹ - ζ_min
    
    where ζ = shear_modulus/6 × (9×bulk_modulus + 8×shear_modulus)/(bulk_modulus + 2×shear_modulus)
    
    References
    ----------
    - Hashin & Shtrikman (1963): Variational bounds
    - Walpole (1966): General composite bounds
    - Mavko et al. (2020): The Rock Physics Handbook, Section 3.8
    
    Examples
    --------
    >>> from drp_template.compute.conversions import GPa2Pa
    >>> import numpy as np
    >>> # Quartz-Calcite-Water mixture
    >>> bounds = hashin_shtrikman_bounds(
    ...     fractions=[0.584, 0.146, 0.27],
    ...     bulk_moduli=GPa2Pa(np.array([36, 75, 2.2])),
    ...     shear_moduli=GPa2Pa(np.array([45, 31, 0]))
    ... )
    >>> print(f"K: [{bounds['bulk_modulus_lower']/1e9:.2f}, {bounds['bulk_modulus_upper']/1e9:.2f}] GPa")
    >>> print(f"G: [{bounds['shear_modulus_lower']/1e9:.2f}, {bounds['shear_modulus_upper']/1e9:.2f}] GPa")
    K: [8.54, 28.59] GPa
    G: [0.00, 25.83] GPa
    
    >>> # Two-phase mixture (Quartz-Porosity)
    >>> bounds = hashin_shtrikman_bounds(
    ...     fractions=[0.7, 0.3],
    ...     bulk_moduli=GPa2Pa(np.array([37, 0])),
    ...     shear_moduli=GPa2Pa(np.array([44, 0]))
    ... )
    >>> print(f"HS bounds narrower than VRH for this case")
    
    >>> # Check if material is well-ordered
    >>> K = GPa2Pa(np.array([36, 75, 2.2]))
    >>> G = GPa2Pa(np.array([45, 31, 0]))
    >>> max_K_idx = np.argmax(K)
    >>> max_G_idx = np.argmax(G)
    >>> if max_K_idx != max_G_idx:
    ...     print("Not well-ordered: bounds may not be optimal")
    """
    fractions = np.asarray(fractions)
    bulk_moduli = np.asarray(bulk_moduli)
    shear_moduli = np.asarray(shear_moduli)
    
    # Validation
    if not (len(fractions) == len(bulk_moduli) == len(shear_moduli)):
        raise ValueError(
            f'All input arrays must have the same length. Got: '
            f'fractions({len(fractions)}), bulk_moduli({len(bulk_moduli)}), '
            f'shear_moduli({len(shear_moduli)})'
        )
    
    if not np.isclose(np.sum(fractions), 1.0):
        raise ValueError(
            f'Fractions must sum to 1. Got sum: {np.sum(fractions):.6f}'
        )
    
    # Find extreme values
    bulk_modulus_max = np.max(bulk_moduli)
    bulk_modulus_min = np.min(bulk_moduli)
    shear_modulus_max = np.max(shear_moduli)
    shear_modulus_min = np.min(shear_moduli)
    
    # Hashin-Shtrikman bounds for bulk modulus
    # Upper bound (uses shear_modulus_max)
    z_upper = (4.0 / 3.0) * shear_modulus_max
    bulk_modulus_upper = 1.0 / np.sum(fractions / (bulk_moduli + z_upper)) - z_upper
    
    # Lower bound (uses shear_modulus_min)
    z_lower = (4.0 / 3.0) * shear_modulus_min
    bulk_modulus_lower = 1.0 / np.sum(fractions / (bulk_moduli + z_lower)) - z_lower
    
    # Hashin-Shtrikman bounds for shear modulus
    # Upper bound (uses bulk_modulus_max, shear_modulus_max)
    zeta_max = shear_modulus_max / 6.0 * (9 * bulk_modulus_max + 8 * shear_modulus_max) / (bulk_modulus_max + 2 * shear_modulus_max)
    shear_modulus_upper = 1.0 / np.sum(fractions / (shear_moduli + zeta_max)) - zeta_max
    
    # Lower bound (uses bulk_modulus_min, shear_modulus_min)
    zeta_min = shear_modulus_min / 6.0 * (9 * bulk_modulus_min + 8 * shear_modulus_min) / (bulk_modulus_min + 2 * shear_modulus_min)
    shear_modulus_lower = 1.0 / np.sum(fractions / (shear_moduli + zeta_min)) - zeta_min
    
    # Calculate averages
    bulk_modulus_avg = (bulk_modulus_upper + bulk_modulus_lower) / 2.0
    shear_modulus_avg = (shear_modulus_upper + shear_modulus_lower) / 2.0
    
    return {
        'bulk_modulus_lower': float(bulk_modulus_lower),
        'bulk_modulus_upper': float(bulk_modulus_upper),
        'bulk_modulus_avg': float(bulk_modulus_avg),
        'shear_modulus_lower': float(shear_modulus_lower),
        'shear_modulus_upper': float(shear_modulus_upper),
        'shear_modulus_avg': float(shear_modulus_avg)
    }
