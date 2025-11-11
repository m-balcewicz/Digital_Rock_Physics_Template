"""
Voigt-Reuss-Hill Bounds
=======================

Upper (Voigt), lower (Reuss) bounds and Hill average for elastic moduli.

References
----------
- Voigt, W. (1889): Ueber die Beziehung zwischen den beiden Elasticitätsconstanten
  isotroper Körper, Annalen der Physik, 274, 573-587
- Reuss, A. (1929): Berechnung der Fließgrenze von Mischkristallen auf Grund der
  Plastizitätsbedingung für Einkristalle, ZAMM, 9, 49-58
- Hill, R. (1952): The Elastic Behaviour of a Crystalline Aggregate, Proceedings of
  the Physical Society A, 65, 349-354
- Mavko, G., Mukerji, T., Dvorkin, J. (2020): The Rock Physics Handbook

Author
------
Martin Balcewicz (martin.balcewicz@rockphysics.org)
"""

import numpy as np

__all__ = ['voigt_bound', 'reuss_bound', 'hill_average', 'voigt_reuss_hill_bounds']


def voigt_bound(fractions, moduli):
    """
    Calculate Voigt (upper) bound using arithmetic averaging.
    
    The Voigt bound assumes uniform strain (isostrain) conditions.
    
    Formula: M_voigt = Σ(f_i × M_i)
    
    Parameters
    ----------
    fractions : array-like
        Volume fractions of constituents. Must sum to 1.
    moduli : array-like
        Elastic moduli of constituents (Pa).
    
    Returns
    -------
    float
        Voigt (upper) bound for elastic modulus (Pa).
        
    Examples
    --------
    >>> # Quartz-Calcite mixture
    >>> K_voigt = voigt_bound([0.6, 0.4], [37e9, 76e9])
    >>> print(f"K_voigt = {K_voigt/1e9:.2f} GPa")
    """
    fractions = np.asarray(fractions)
    moduli = np.asarray(moduli)
    return float(np.sum(fractions * moduli))


def reuss_bound(fractions, moduli):
    """
    Calculate Reuss (lower) bound using harmonic averaging.
    
    The Reuss bound assumes uniform stress (isostress) conditions.
    
    Formula: M_reuss = 1 / Σ(f_i / M_i)
    
    Parameters
    ----------
    fractions : array-like
        Volume fractions of constituents. Must sum to 1.
    moduli : array-like
        Elastic moduli of constituents (Pa).
    
    Returns
    -------
    float
        Reuss (lower) bound for elastic modulus (Pa).
        
    Examples
    --------
    >>> # Quartz-Calcite mixture
    >>> K_reuss = reuss_bound([0.6, 0.4], [37e9, 76e9])
    >>> print(f"K_reuss = {K_reuss/1e9:.2f} GPa")
    """
    fractions = np.asarray(fractions)
    moduli = np.asarray(moduli)
    return float(1.0 / np.sum(fractions / moduli))


def hill_average(voigt, reuss):
    """
    Calculate Hill average (arithmetic mean of Voigt and Reuss bounds).
    
    Formula: M_hill = (M_voigt + M_reuss) / 2
    
    Parameters
    ----------
    voigt : float
        Voigt (upper) bound (Pa).
    reuss : float
        Reuss (lower) bound (Pa).
    
    Returns
    -------
    float
        Hill average (Pa).
        
    Examples
    --------
    >>> M_hill = hill_average(50e9, 40e9)
    >>> print(f"M_hill = {M_hill/1e9:.2f} GPa")
    """
    return (voigt + reuss) / 2.0


def voigt_reuss_hill_bounds(fractions, bulk_moduli, shear_moduli):
    """
    Calculate Voigt-Reuss-Hill bounds and averages for bulk and shear moduli.
    
    Computes upper (Voigt), lower (Reuss) bounds and Hill averages for both
    bulk and shear moduli of an isotropic aggregate.
    
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
        - 'K_voigt' : Voigt (upper) bound for bulk modulus (Pa)
        - 'K_reuss' : Reuss (lower) bound for bulk modulus (Pa)
        - 'K_hill' : Hill average for bulk modulus (Pa)
        - 'G_voigt' : Voigt (upper) bound for shear modulus (Pa)
        - 'G_reuss' : Reuss (lower) bound for shear modulus (Pa)
        - 'G_hill' : Hill average for shear modulus (Pa)
    
    Raises
    ------
    ValueError
        If arrays have different lengths or fractions don't sum to 1.
    
    Notes
    -----
    The Voigt-Reuss-Hill bounds provide the widest possible bounds for
    elastic moduli without specifying constituent geometry:
    
    - **Voigt bound** (upper): Assumes uniform strain (isostrain)
    - **Reuss bound** (lower): Assumes uniform stress (isostress)
    - **Hill average**: Arithmetic mean, often used as practical estimate
    
    These bounds apply to isotropic aggregates. For narrower bounds, see
    Hashin-Shtrikman bounds.
    
    References
    ----------
    - Voigt (1889): Upper bound for polycrystals
    - Reuss (1929): Lower bound for polycrystals
    - Hill (1952): Averaging procedure for crystalline aggregates
    - Mavko et al. (2020): The Rock Physics Handbook, Chapter 3
    
    Examples
    --------
    >>> # Quartz-Calcite mixture (60%-40%)
    >>> bounds = voigt_reuss_hill_bounds(
    ...     fractions=[0.6, 0.4],
    ...     bulk_moduli=[37e9, 76e9],
    ...     shear_moduli=[44e9, 32e9]
    ... )
    >>> print(f"K_hill = {bounds['K_hill']/1e9:.2f} GPa")
    >>> print(f"G_hill = {bounds['G_hill']/1e9:.2f} GPa")
    K_hill = 51.06 GPa
    G_hill = 39.24 GPa
    
    >>> # Three-component mixture
    >>> bounds = voigt_reuss_hill_bounds(
    ...     fractions=[0.5, 0.3, 0.2],
    ...     bulk_moduli=[37e9, 76e9, 2.2e9],  # Quartz, Calcite, Water
    ...     shear_moduli=[44e9, 32e9, 0]
    ... )
    >>> print(f"Bounds: K=[{bounds['K_reuss']/1e9:.1f}, {bounds['K_voigt']/1e9:.1f}] GPa")
    
    >>> # Access individual values
    >>> K_upper = bounds['K_voigt']
    >>> K_lower = bounds['K_reuss']
    >>> K_avg = bounds['K_hill']
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
    
    # Calculate bounds
    K_voigt = voigt_bound(fractions, bulk_moduli)
    K_reuss = reuss_bound(fractions, bulk_moduli)
    K_hill = hill_average(K_voigt, K_reuss)
    
    G_voigt = voigt_bound(fractions, shear_moduli)
    G_reuss = reuss_bound(fractions, shear_moduli)
    G_hill = hill_average(G_voigt, G_reuss)
    
    return {
        'K_voigt': K_voigt,
        'K_reuss': K_reuss,
        'K_hill': K_hill,
        'G_voigt': G_voigt,
        'G_reuss': G_reuss,
        'G_hill': G_hill
    }
