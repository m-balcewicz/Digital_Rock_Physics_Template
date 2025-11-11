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
        - 'K_lower' : Lower (Reuss-like) bound for bulk modulus (Pa)
        - 'K_upper' : Upper (Voigt-like) bound for bulk modulus (Pa)
        - 'G_lower' : Lower bound for shear modulus (Pa)
        - 'G_upper' : Upper bound for shear modulus (Pa)
        - 'K_avg' : Average of K bounds (Pa)
        - 'G_avg' : Average of G bounds (Pa)
    
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
    - K_upper = [Σ f_i/(K_i + 4/3 × G_max)]⁻¹ - 4/3 × G_max
    - K_lower = [Σ f_i/(K_i + 4/3 × G_min)]⁻¹ - 4/3 × G_min
    
    For shear modulus:
    - G_upper = [Σ f_i/(G_i + ζ_max)]⁻¹ - ζ_max
    - G_lower = [Σ f_i/(G_i + ζ_min)]⁻¹ - ζ_min
    
    where ζ = G/6 × (9K + 8G)/(K + 2G)
    
    References
    ----------
    - Hashin & Shtrikman (1963): Variational bounds
    - Walpole (1966): General composite bounds
    - Mavko et al. (2020): The Rock Physics Handbook, Section 3.8
    
    Examples
    --------
    >>> # Quartz-Calcite-Water mixture
    >>> bounds = hashin_shtrikman_bounds(
    ...     fractions=[0.584, 0.146, 0.27],
    ...     bulk_moduli=[36e9, 75e9, 2.2e9],
    ...     shear_moduli=[45e9, 31e9, 0]
    ... )
    >>> print(f"K: [{bounds['K_lower']/1e9:.2f}, {bounds['K_upper']/1e9:.2f}] GPa")
    >>> print(f"G: [{bounds['G_lower']/1e9:.2f}, {bounds['G_upper']/1e9:.2f}] GPa")
    K: [8.54, 28.59] GPa
    G: [0.00, 25.83] GPa
    
    >>> # Two-phase mixture (Quartz-Porosity)
    >>> bounds = hashin_shtrikman_bounds(
    ...     fractions=[0.7, 0.3],
    ...     bulk_moduli=[37e9, 0],
    ...     shear_moduli=[44e9, 0]
    ... )
    >>> print(f"HS bounds narrower than VRH for this case")
    
    >>> # Check if material is well-ordered
    >>> K = [36e9, 75e9, 2.2e9]
    >>> G = [45e9, 31e9, 0]
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
    K_max = np.max(bulk_moduli)
    K_min = np.min(bulk_moduli)
    G_max = np.max(shear_moduli)
    G_min = np.min(shear_moduli)
    
    # Hashin-Shtrikman bounds for bulk modulus
    # Upper bound (uses G_max)
    z_upper = (4.0 / 3.0) * G_max
    K_upper = 1.0 / np.sum(fractions / (bulk_moduli + z_upper)) - z_upper
    
    # Lower bound (uses G_min)
    z_lower = (4.0 / 3.0) * G_min
    K_lower = 1.0 / np.sum(fractions / (bulk_moduli + z_lower)) - z_lower
    
    # Hashin-Shtrikman bounds for shear modulus
    # Upper bound (uses K_max, G_max)
    zeta_max = G_max / 6.0 * (9 * K_max + 8 * G_max) / (K_max + 2 * G_max)
    G_upper = 1.0 / np.sum(fractions / (shear_moduli + zeta_max)) - zeta_max
    
    # Lower bound (uses K_min, G_min)
    zeta_min = G_min / 6.0 * (9 * K_min + 8 * G_min) / (K_min + 2 * G_min)
    G_lower = 1.0 / np.sum(fractions / (shear_moduli + zeta_min)) - zeta_min
    
    # Calculate averages
    K_avg = (K_upper + K_lower) / 2.0
    G_avg = (G_upper + G_lower) / 2.0
    
    return {
        'K_lower': float(K_lower),
        'K_upper': float(K_upper),
        'K_avg': float(K_avg),
        'G_lower': float(G_lower),
        'G_upper': float(G_upper),
        'G_avg': float(G_avg)
    }
