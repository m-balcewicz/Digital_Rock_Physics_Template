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
    >>> from drp_template.compute.conversions import GPa2Pa
    >>> import numpy as np
    >>> # Quartz-Calcite mixture
    >>> bulk_modulus_voigt = voigt_bound([0.6, 0.4], GPa2Pa(np.array([37, 76])))
    >>> print(f"bulk_modulus_voigt = {bulk_modulus_voigt/1e9:.2f} GPa")
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
    >>> from drp_template.compute.conversions import GPa2Pa
    >>> import numpy as np
    >>> # Quartz-Calcite mixture
    >>> bulk_modulus_reuss = reuss_bound([0.6, 0.4], GPa2Pa(np.array([37, 76])))
    >>> print(f"bulk_modulus_reuss = {bulk_modulus_reuss/1e9:.2f} GPa")
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
        - 'bulk_modulus_voigt' : Voigt (upper) bound for bulk modulus (Pa)
        - 'bulk_modulus_reuss' : Reuss (lower) bound for bulk modulus (Pa)
        - 'bulk_modulus_hill' : Hill average for bulk modulus (Pa)
        - 'shear_modulus_voigt' : Voigt (upper) bound for shear modulus (Pa)
        - 'shear_modulus_reuss' : Reuss (lower) bound for shear modulus (Pa)
        - 'shear_modulus_hill' : Hill average for shear modulus (Pa)
    
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
    >>> from drp_template.compute.conversions import GPa2Pa
    >>> import numpy as np
    >>> # Quartz-Calcite mixture (60%-40%)
    >>> bounds = voigt_reuss_hill_bounds(
    ...     fractions=[0.6, 0.4],
    ...     bulk_moduli=GPa2Pa(np.array([37, 76])),
    ...     shear_moduli=GPa2Pa(np.array([44, 32]))
    ... )
    >>> print(f"bulk_modulus_hill = {bounds['bulk_modulus_hill']/1e9:.2f} GPa")
    >>> print(f"shear_modulus_hill = {bounds['shear_modulus_hill']/1e9:.2f} GPa")
    bulk_modulus_hill = 51.06 GPa
    shear_modulus_hill = 39.24 GPa
    
    >>> # Three-component mixture
    >>> bounds = voigt_reuss_hill_bounds(
    ...     fractions=[0.5, 0.3, 0.2],
    ...     bulk_moduli=GPa2Pa(np.array([37, 76, 2.2])),  # Quartz, Calcite, Water
    ...     shear_moduli=GPa2Pa(np.array([44, 32, 0]))
    ... )
    >>> print(f"Bounds: K=[{bounds['bulk_modulus_reuss']/1e9:.1f}, {bounds['bulk_modulus_voigt']/1e9:.1f}] GPa")
    
    >>> # Access individual values
    >>> bulk_modulus_upper = bounds['bulk_modulus_voigt']
    >>> bulk_modulus_lower = bounds['bulk_modulus_reuss']
    >>> bulk_modulus_avg = bounds['bulk_modulus_hill']
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
    bulk_modulus_voigt = voigt_bound(fractions, bulk_moduli)
    bulk_modulus_reuss = reuss_bound(fractions, bulk_moduli)
    bulk_modulus_hill = hill_average(bulk_modulus_voigt, bulk_modulus_reuss)
    
    shear_modulus_voigt = voigt_bound(fractions, shear_moduli)
    shear_modulus_reuss = reuss_bound(fractions, shear_moduli)
    shear_modulus_hill = hill_average(shear_modulus_voigt, shear_modulus_reuss)
    
    return {
        'bulk_modulus_voigt': bulk_modulus_voigt,
        'bulk_modulus_reuss': bulk_modulus_reuss,
        'bulk_modulus_hill': bulk_modulus_hill,
        'shear_modulus_voigt': shear_modulus_voigt,
        'shear_modulus_reuss': shear_modulus_reuss,
        'shear_modulus_hill': shear_modulus_hill
    }
