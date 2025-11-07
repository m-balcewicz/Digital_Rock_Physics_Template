"""
Wood's Formula
==============

Wood's (1955) relation for sound velocity in fluid suspensions and mixtures.

This module provides Wood's formula for calculating the acoustic velocity in
fluid mixtures where heterogeneities are small compared to the wavelength.

References
----------
- Wood, A.B. (1955): A Textbook of Sound
- Mavko, G., Mukerji, T., Dvorkin, J. (2020): The Rock Physics Handbook

Author
------
Martin Balcewicz (martin.balcewicz@rockphysics.org)

Notes
-----
Wood's formula applies when:
- Heterogeneity scale << wavelength
- Fluid suspension or mixture
- Reuss (isostress) average applies

Functions
---------
- wood: Calculate P-wave velocity using Wood's formula
"""

import numpy as np
import pandas as pd
import math

__all__ = [
    'wood',
]


def wood(porosity, phase, fraction, bulk_modulus_mineral, density):
    """
    Calculate P-wave velocity in fluid suspension using Wood's formula.
    
    In a fluid suspension or fluid mixture, where the heterogeneities are small
    compared with a wavelength, the sound velocity is given exactly by Wood's (1955)
    relation. This uses the Reuss (isostress) average for the effective bulk modulus.
    
    Parameters:
    -----------
    porosity : float
        Porosity (0-1). Not directly used in current implementation but
        kept for interface consistency.
    phase : list of str
        Names of the phases (e.g., ['Quartz', 'Water'])
    fraction : array-like
        Volume fractions of each phase. Must sum to 1.
    bulk_modulus_mineral : array-like
        Bulk moduli of each phase (Pa)
    density : array-like
        Densities of each phase (kg/m³)
    
    Returns:
    --------
    tuple
        (rho_average, Wood_VP_wet, Reuss_K)
        - rho_average: Average density of the mixture (kg/m³)
        - Wood_VP_wet: P-wave velocity (m/s)
        - Reuss_K: Reuss average bulk modulus (Pa)
    
    Notes:
    ------
    Wood's formula:
    - K_Reuss = 1 / Σ(f_i / K_i)  (Reuss average for bulk modulus)
    - ρ_avg = Σ(f_i × ρ_i)        (Arithmetic average for density)
    - v_P = √(K_Reuss / ρ_avg)    (P-wave velocity)
    
    References:
    -----------
    Wood's Formula according to Hashin-Shtrikman-Walpole Bounds by
    Mavko, G., Mukerji, T., Dvorkin, J.: The Rock Physics Handbook.
    Cambridge University Press (2020)
    
    Examples:
    ---------
    ```python
    # Example 1: Quartz-water mixture
    phase = ['Quartz', 'Water']
    bulk_modulus = [36e9, 2.2e9]  # Pa
    fraction = [0.6, 0.4]
    density = [2650, 1000]  # kg/m³
    porosity = 0.4
    
    rho_avg, vP, K_Reuss = wood(porosity, phase, fraction, bulk_modulus, density)
    print(f"Wood's P-wave velocity: {vP:.0f} m/s")
    
    # Example 2: Quartz-water-air mixture
    phase = ['Quartz', 'Water', 'Air']
    bulk_modulus = [36e9, 2.2e9, 0.000131e9]  # Pa
    porosity = 0.4
    fraction = [1-porosity, 0.5*porosity, 0.5*porosity]
    density = [2650, 1000, 0.00119/1e-3]  # kg/m³
    
    rho_avg, vP, K_Reuss = wood(porosity, phase, fraction, bulk_modulus, density)
    ```
    """
    properties = pd.DataFrame({
        "Phase": phase,
        "Fraction": fraction,
        "Density": density,
        "K": bulk_modulus_mineral
    })

    # Reuss (isostress) average for bulk modulus
    var = np.zeros((len(properties), 1))
    for m in range(len(properties)):
        var[m] = properties.loc[m, "Fraction"] / properties.loc[m, "K"]

    Reuss_K = float(1 / sum(var))

    # Arithmetic average for density
    var = np.zeros((len(properties), 1))
    for m in range(len(properties)):
        var[m] = properties.loc[m, "Fraction"] * properties.loc[m, "Density"]

    rho_average = float(sum(var))

    # P-wave velocity using Wood's formula
    Wood_VP_wet = math.sqrt(Reuss_K / rho_average) / 1e-9

    return rho_average, Wood_VP_wet, Reuss_K
