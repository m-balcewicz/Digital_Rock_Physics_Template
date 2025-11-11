"""
Isotropic Elastic Properties
=============================

Elastic moduli conversions and seismic velocities for isotropic media.

This module provides functions for calculating and converting between various
representations of elastic properties for isotropic, linear, elastic media.

The module handles conversions between:
- Bulk modulus (K) and shear modulus (G)
- Young's modulus (E) and Poisson's ratio (ν)
- Lamé parameters (λ, μ)
- Stiffness coefficients (c11, c44)
- Seismic wave velocities (Vp, Vs, Ve)

References
----------
- Hooke's Law (isotropic form)
- Mavko, G., Mukerji, T., Dvorkin, J. (2020): The Rock Physics Handbook, 
  3rd edition, Cambridge University Press

Author
------
Martin Balcewicz (martin.balcewicz@rockphysics.org)
"""

import math
import numpy as np

__all__ = [
    'elastic_moduli',
    'seismic_velocity',
]


def elastic_moduli(**kwargs):
    """
    Calculate elastic moduli and stiffness coefficients for isotropic media.
    
    This versatile function handles multiple input combinations and performs
    conversions between different representations of elastic properties.
    
    Parameters:
    -----------
    **kwargs : keyword arguments
        Various combinations supported:
        
        - c_11, c_44: Stiffness coefficients (Pa)
        - c_11, c_44, density: Returns wave velocities (m/s)
        - bulk_modulus_mineral, shear_modulus_mineral: Returns c_11, c_44 (Pa)
        - bulk_modulus_rock, shear_modulus_rock: Returns Young's modulus (Pa)
        - density, p_wave_velocity, shear_wave_velocity: Returns c_11, c_44 (Pa)
        - youngs_modulus_mineral, poisson_mineral: Returns c_11, c_44 (Pa)
    
    Returns:
    --------
    tuple
        Depending on inputs:
        - (bulk_modulus, shear_modulus) in Pa
        - (c_11, c_44) in Pa
        - (p_wave_velocity, shear_wave_velocity) in m/s
        - youngs_modulus in Pa
    
    Notes:
    ------
    For isotropic media:
    - c_11 = K + (4/3)G
    - c_44 = G
    - E = 9KG / (3K + G)  (Young's modulus)
    
    References:
    -----------
    Mavko, G., Mukerji, T., Dvorkin, J.: The Rock Physics Handbook.
    Cambridge University Press (2020)
    
    Examples:
    ---------
    ```python
    # Calculate K and G from stiffness coefficients
    K, G = elastic_moduli(c_11=86.6e9, c_44=57.8e9)
    
    # Calculate wave velocities
    vp, vs = elastic_moduli(density=2650, c_11=68e9, c_44=33.5e9)
    
    # Calculate stiffness from K and G
    c11, c44 = elastic_moduli(bulk_modulus_mineral=37.0e9, 
                              shear_modulus_mineral=44.0e9)
    ```
    """
    if 'c_11' in kwargs and 'c_44' in kwargs:
        if 'density' in kwargs:
            density = kwargs.get('density')
            c_11 = kwargs.get('c_11')
            c_44 = kwargs.get('c_44')
            p_wave_velocity = math.sqrt(c_11 / density)
            shear_wave_velocity = math.sqrt(c_44 / density)

            return p_wave_velocity, shear_wave_velocity

        else:
            c_11 = kwargs.get('c_11')
            c_44 = kwargs.get('c_44')
            bulk_modulus = c_11 - 4 / 3 * c_44
            shear_modulus = c_44

            return bulk_modulus, shear_modulus

    elif 'bulk_modulus_mineral' in kwargs and 'shear_modulus_mineral' in kwargs:
        bulk_modulus_mineral = kwargs.get('bulk_modulus_mineral')
        shear_modulus_mineral = kwargs.get('shear_modulus_mineral')
        c_44 = shear_modulus_mineral
        c_11 = bulk_modulus_mineral + 4 / 3 * shear_modulus_mineral

        return c_11, c_44

    elif 'bulk_modulus_rock' in kwargs and 'shear_modulus_rock' in kwargs:
        bulk_modulus_rock = kwargs.get('bulk_modulus_rock')
        shear_modulus_rock = kwargs.get('shear_modulus_rock')

        youngs_modulus_rock = (9 * bulk_modulus_rock * shear_modulus_rock) / (
            3 * bulk_modulus_rock + shear_modulus_rock
        )

        return youngs_modulus_rock

    elif 'density' in kwargs and 'p_wave_velocity' in kwargs and 'shear_wave_velocity' in kwargs:
        density = kwargs.get('density')
        p_wave_velocity = kwargs.get('p_wave_velocity')
        shear_wave_velocity = kwargs.get('shear_wave_velocity')
        c_11 = p_wave_velocity * p_wave_velocity * density
        c_44 = shear_wave_velocity * shear_wave_velocity * density

        return c_11, c_44

    elif 'youngs_modulus_mineral' in kwargs and 'poisson_mineral' in kwargs:
        youngs_modulus_mineral = kwargs.get('youngs_modulus_mineral')
        poisson_mineral = kwargs.get('poisson_mineral')
        c_11 = (youngs_modulus_mineral * (1 - poisson_mineral)) / (
            (1 + poisson_mineral) * (1 - 2 * poisson_mineral)
        )
        c_44 = youngs_modulus_mineral / (2 + 2 * poisson_mineral)

        return c_11, c_44

    else:
        raise ValueError(
            "Not enough information provided to calculate elastic moduli. "
            "Supported input combinations: "
            "(c_11, c_44), (c_11, c_44, density), "
            "(bulk_modulus_mineral, shear_modulus_mineral), "
            "(bulk_modulus_rock, shear_modulus_rock), "
            "(density, p_wave_velocity, shear_wave_velocity), "
            "(youngs_modulus_mineral, poisson_mineral)"
        )


def seismic_velocity(rho_rock, **kwargs):
    """
    Calculate seismic wave velocities for isotropic, linear, elastic media.
    
    This function calculates P-wave (vP), S-wave (vS), extensional wave (vE)
    velocities, and Poisson's ratio from various elastic property inputs.
    
    Parameters:
    -----------
    rho_rock : float
        Rock density (kg/m³)
    **kwargs : keyword arguments
        Various combinations supported:
        
        - bulk_modulus_rock, shear_modulus_rock: K and G in GPa
        - lame_coef, shear_modulus_rock: Lamé coefficients in GPa
        - youngs_modulus_rock: Young's modulus in GPa
    
    Returns:
    --------
    tuple
        (p_wave_velocity, shear_wave_velocity, extensional_wave_velocity, poisson)
        Velocities in m/s, Poisson's ratio dimensionless.
    
    Notes:
    ------
    Seismic velocities for isotropic media:
    - vP = √[(K + 4G/3) / ρ]  (P-wave)
    - vS = √[G / ρ]           (S-wave)
    - vE = √[E / ρ]           (Extensional wave)
    - ν = (vP² - 2vS²) / (2vP² - 2vS²)  (Poisson's ratio)
    
    References:
    -----------
    Mavko, G., Mukerji, T., Dvorkin, J.: The Rock Physics Handbook.
    Cambridge University Press (2020)
    
    Examples:
    ---------
    ```python
    # Calculate velocities from K and G
    vP, vS, vE, nu = seismic_velocity(
        rho_rock=2650,  # kg/m³
        bulk_modulus_rock=37,   # GPa
        shear_modulus_rock=44   # GPa
    )
    
    print(f"P-wave velocity: {vP:.0f} m/s")
    print(f"S-wave velocity: {vS:.0f} m/s")
    print(f"Poisson's ratio: {nu:.3f}")
    ```
    """
    # P-wave velocity
    if 'bulk_modulus_rock' in kwargs and 'shear_modulus_rock' in kwargs:
        K_rock = kwargs.get('bulk_modulus_rock')
        G_rock = kwargs.get('shear_modulus_rock')
        p_wave_velocity = math.sqrt(
            ((K_rock * 1e9) + 4 / 3 * (G_rock * 1e9)) / (rho_rock / 1000)
        ) * 1000

    elif 'lame_coef' in kwargs and 'shear_modulus_rock' in kwargs:
        lame_coef = kwargs.get('lame_coef')
        G_rock = kwargs.get('shear_modulus_rock')
        p_wave_velocity = math.sqrt((lame_coef + 2 * G_rock * 1e9) / rho_rock / 1000)

    else:
        p_wave_velocity = np.nan

    # S-wave velocity
    if 'shear_modulus_rock' in kwargs:
        G_rock = kwargs.get('shear_modulus_rock')
        shear_wave_velocity = math.sqrt((G_rock * 1e9) / (rho_rock / 1000)) * 1000
    else:
        shear_wave_velocity = np.nan

    # Extensional wave velocity
    if 'youngs_modulus_rock' in kwargs:
        E_rock = kwargs.get('youngs_modulus_rock')
        extensional_wave_velocity = math.sqrt(E_rock / rho_rock) * 1000
    elif 'bulk_modulus_rock' in kwargs and 'shear_modulus_rock' in kwargs:
        K_rock = kwargs.get('bulk_modulus_rock')
        G_rock = kwargs.get('shear_modulus_rock')
        E_rock_cal = (9 * K_rock * 1e9 * G_rock * 1e9) / (3 * K_rock * 1e9 + G_rock * 1e9)
        extensional_wave_velocity = math.sqrt(E_rock_cal / rho_rock) * 1000
    else:
        extensional_wave_velocity = np.nan

    # Poisson's ratio
    if not np.isnan(p_wave_velocity) and not np.isnan(shear_wave_velocity):
        poisson = (p_wave_velocity ** 2 - 2 * shear_wave_velocity ** 2) / (
            2 * p_wave_velocity ** 2 - shear_wave_velocity ** 2
        )
    elif not np.isnan(extensional_wave_velocity) and not np.isnan(shear_wave_velocity):
        poisson = (extensional_wave_velocity ** 2 - 2 * shear_wave_velocity ** 2) / (
            2 * shear_wave_velocity ** 2
        )
    else:
        poisson = np.nan

    return p_wave_velocity, shear_wave_velocity, extensional_wave_velocity, poisson
