"""
Elastic Bounds for Rock Physics
=================================

Voigt-Reuss-Hill and Hashin-Shtrikman bounds for effective elastic moduli.

This module provides functions for calculating theoretical bounds on the effective
elastic properties of composite materials. These bounds provide constraints on the
possible range of elastic moduli for aggregates without specifying exact geometry.

References
----------
- Hashin & Shtrikman (1963): Variational approach to elastic behavior of multiphase materials
- Voigt (1889) & Reuss (1929): Upper and lower bounds for polycrystals
- Hill (1952): Elastic properties of crystalline aggregates
- Mavko, G., Mukerji, T., Dvorkin, J. (2020): The Rock Physics Handbook

Author
------
Martin Balcewicz (martin.balcewicz@rockphysics.org)

Functions
---------
- hashin_shtrikman_bounds: Calculate narrowest possible HS bounds
- voigt_reuss_hill_bounds: Calculate VRH bounds and average
"""

import numpy as np
import pandas as pd

__all__ = [
    'hashin_shtrikman_bounds',
    'voigt_reuss_hill_bounds',
]


def hashin_shtrikman_bounds(bulk_modulus_rock, shear_modulus_rock, fractions_rock):
    """
    Calculate Hashin-Shtrikman upper and lower bounds for bulk and shear moduli.
    
    The Hashin-Shtrikman bounds are the narrowest possible bounds on the effective elastic
    moduli without specifying the geometry of the constituents. For well-ordered materials
    (where the constituent with the largest bulk modulus also has the largest shear modulus),
    these bounds are optimum.
    
    Parameters:
    -----------
    bulk_modulus_rock : array-like
        Bulk moduli of the rock constituents (Pa).
    shear_modulus_rock : array-like
        Shear moduli of the rock constituents (Pa).
    fractions_rock : array-like
        Volume fractions of the constituents. Must sum to 1.
    
    Returns:
    --------
    tuple
        (HS_K_low, HS_K_up, HS_G_up, HS_G_low) - Lower and upper bounds for
        bulk modulus (K) and shear modulus (G) in Pa.
        
    Notes:
    ------
    - If the material is not "well-ordered" (max K doesn't correspond to max G),
      the bounds are still valid but may not be optimum.
    - Well-ordered: constituent with largest bulk modulus has largest shear modulus
    
    References:
    -----------
    Hashin-Shtrikman-Walpole Bounds by Mavko, G., Mukerji, T., Dvorkin, J.:
    The Rock Physics Handbook. Cambridge University Press (2020)
    
    Example:
    --------
    ```python
    # Quartz-calcite-water mixture
    phase = ['Quartz', 'Calcite', 'Water']
    bulk = [36e9, 75e9, 2.2e9]  # Pa
    shear = [45e9, 31e9, 0]     # Pa
    fractions = [0.584, 0.146, 0.27]
    
    K_low, K_up, G_up, G_low = hashin_shtrikman_bounds(bulk, shear, fractions)
    ```
    """
    bulk_modulus_rock = np.asarray(bulk_modulus_rock)
    shear_modulus_rock = np.asarray(shear_modulus_rock)
    fractions_rock = np.asarray(fractions_rock)
    
    G_max = np.max(shear_modulus_rock)
    G_min = np.min(shear_modulus_rock)
    K_max = np.max(bulk_modulus_rock)
    K_min = np.min(bulk_modulus_rock)
    
    # Upper Hashin-Shtrikman Bound (Bulk Modulus)
    z = (4 / 3) * G_max  # G_max is required
    var = np.zeros((len(bulk_modulus_rock), 1))
    for m in range(len(bulk_modulus_rock)):
        var[m] = fractions_rock[m] / (bulk_modulus_rock[m] + z)
    
    HS_K_up = float(1 / sum(var) - z)
    
    # Lower Hashin-Shtrikman Bound (Bulk Modulus)
    z = (4 / 3) * G_min  # G_min is required
    var = np.zeros((len(bulk_modulus_rock), 1))
    for m in range(len(bulk_modulus_rock)):
        var[m] = fractions_rock[m] / (bulk_modulus_rock[m] + z)
    
    HS_K_low = float(1 / sum(var) - z)
    
    # Upper Hashin-Shtrikman Bound (Shear Modulus)
    zeta = G_max / 6 * ((9 * K_max + 8 * G_max) / (K_max + 2 * G_max))
    var = np.zeros((len(bulk_modulus_rock), 1))
    for m in range(len(bulk_modulus_rock)):
        var[m] = fractions_rock[m] / (shear_modulus_rock[m] + zeta)
    
    HS_G_up = float(1 / sum(var)) - zeta
    
    # Lower Hashin-Shtrikman Bound (Shear Modulus)
    zeta = G_min / 6 * ((9 * K_min + 8 * G_min) / (K_min + 2 * G_min))
    var = np.zeros((len(bulk_modulus_rock), 1))
    for m in range(len(bulk_modulus_rock)):
        var[m] = fractions_rock[m] / (shear_modulus_rock[m] + zeta)
    
    HS_G_low = float(1 / sum(var)) - zeta
    
    return HS_K_low, HS_K_up, HS_G_up, HS_G_low


def voigt_reuss_hill_bounds(phase, fraction, bulk_modulus_mineral, shear_modulus_mineral):
    """
    Calculate Voigt (upper), Reuss (lower) bounds and Voigt-Reuss-Hill average.
    
    The Voigt bound assumes uniform strain (isostrain), while the Reuss bound assumes
    uniform stress (isostress). The Hill average is the arithmetic mean of these two
    bounds and often provides a reasonable estimate of the effective moduli.
    
    Parameters:
    -----------
    phase : list of str
        Names of the constituent phases.
    fraction : array-like
        Volume fractions of the constituents. Must sum to 1.
    bulk_modulus_mineral : array-like
        Bulk moduli of the constituents (Pa).
    shear_modulus_mineral : array-like
        Shear moduli of the constituents (Pa).
    
    Returns:
    --------
    tuple
        (Voigt_K, Voigt_G, Reuss_K, Reuss_G, VRH_K, VRH_G) - 
        Voigt (upper), Reuss (lower), and Hill average values for
        bulk modulus (K) and shear modulus (G) in Pa.
    
    References:
    -----------
    Voigt upper and Reuss lower bound, and Voigt-Reuss-Hill average by
    Mavko, G., Mukerji, T., Dvorkin, J.: The Rock Physics Handbook.
    Cambridge University Press (2020)
    
    Example:
    --------
    ```python
    phase = ['Quartz', 'Feldspar', 'Dolomite', 'Calcite']
    bulk = np.array([37, 75, 95, 76]) * 1e9  # Convert to Pa
    shear = np.array([44, 25, 45, 32]) * 1e9
    fraction = [0.5, 0.3, 0.1, 0.1]
    
    V_K, V_G, R_K, R_G, VRH_K, VRH_G = voigt_reuss_hill_bounds(
        phase, fraction, bulk, shear
    )
    ```
    """
    fraction = np.asarray(fraction)
    bulk_modulus_mineral = np.asarray(bulk_modulus_mineral)
    shear_modulus_mineral = np.asarray(shear_modulus_mineral)
    
    fraction_control = np.sum(fraction)
    if fraction_control > 1.001 or fraction_control < 0.999:
        raise ValueError('Fractions must sum to 1. Current sum: {:.4f}'.format(fraction_control))
    
    # Create properties dataframe
    properties = pd.DataFrame({
        "Phase": phase,
        "Fraction": fraction,
        "K": bulk_modulus_mineral,
        "G": shear_modulus_mineral
    })
    
    # Upper Voigt Bound (Bulk Modulus)
    var = np.zeros((len(properties), 1))
    for m in range(len(properties)):
        var[m] = properties.loc[m, "Fraction"] * properties.loc[m, "K"]
    Voigt_K = float(sum(var))
    
    # Upper Voigt Bound (Shear Modulus)
    var = np.zeros((len(properties), 1))
    for m in range(len(properties)):
        var[m] = properties.loc[m, "Fraction"] * properties.loc[m, "G"]
    Voigt_G = float(sum(var))
    
    # Lower Reuss Bound (Bulk Modulus)
    var = np.zeros((len(properties), 1))
    for m in range(len(properties)):
        var[m] = properties.loc[m, "Fraction"] / properties.loc[m, "K"]
    Reuss_K = float(1 / sum(var))
    
    # Lower Reuss Bound (Shear Modulus)
    var = np.zeros((len(properties), 1))
    for m in range(len(properties)):
        var[m] = properties.loc[m, "Fraction"] / properties.loc[m, "G"]
    Reuss_G = float(1 / sum(var))
    
    # Voigt-Reuss-Hill Average (Bulk Modulus)
    Voigt_Reuss_Hill_K = (Voigt_K + Reuss_K) / 2
    
    # Voigt-Reuss-Hill Average (Shear Modulus)
    Voigt_Reuss_Hill_G = (Voigt_G + Reuss_G) / 2
    
    return Voigt_K, Voigt_G, Reuss_K, Reuss_G, Voigt_Reuss_Hill_K, Voigt_Reuss_Hill_G
