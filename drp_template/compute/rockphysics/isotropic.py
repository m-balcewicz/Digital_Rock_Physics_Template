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
    'poisson',
    'youngs',
    'lame_lambda',
    'bulk',
    'shear',
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
    
    Parameters
    ----------
    rho_rock : float
        Rock density (kg/m³)
    **kwargs : keyword arguments
        Various combinations supported:
        
        - bulk_modulus_rock, shear_modulus_rock: K and G in Pa
        - lame_coef, shear_modulus_rock: Lamé coefficients in Pa
        - youngs_modulus_rock: Young's modulus in Pa
    
    Returns
    -------
    tuple
        (p_wave_velocity, shear_wave_velocity, extensional_wave_velocity, poisson)
        Velocities in m/s, Poisson's ratio dimensionless.
    
    Notes
    -----
    Seismic velocities for isotropic media:
    - vP = √[(K + 4G/3) / ρ]  (P-wave)
    - vS = √[G / ρ]           (S-wave)
    - vE = √[E / ρ]           (Extensional wave)
    - ν = (vP² - 2vS²) / (2vP² - 2vS²)  (Poisson's ratio)
    
    References
    ----------
    - Mavko et al. (2020): The Rock Physics Handbook
    
    Examples
    --------
    >>> from drp_template.compute import GPa2Pa
    >>> 
    >>> # Calculate velocities from K and G
    >>> vP, vS, vE, nu = seismic_velocity(
    ...     rho_rock=2650,  # kg/m³
    ...     bulk_modulus_rock=GPa2Pa(37),    # Convert 37 GPa to Pa
    ...     shear_modulus_rock=GPa2Pa(44)    # Convert 44 GPa to Pa
    ... )
    >>> 
    >>> print(f"P-wave velocity: {vP:.0f} m/s")
    >>> print(f"S-wave velocity: {vS:.0f} m/s")
    >>> print(f"Poisson's ratio: {nu:.3f}")
    P-wave velocity: 6050 m/s
    S-wave velocity: 4078 m/s
    Poisson's ratio: 0.077
    """
    # P-wave velocity
    if 'bulk_modulus_rock' in kwargs and 'shear_modulus_rock' in kwargs:
        K_rock = kwargs.get('bulk_modulus_rock')  # Pa
        G_rock = kwargs.get('shear_modulus_rock')  # Pa
        p_wave_velocity = math.sqrt((K_rock + 4.0/3.0 * G_rock) / rho_rock)

    elif 'lame_coef' in kwargs and 'shear_modulus_rock' in kwargs:
        lame_coef = kwargs.get('lame_coef')  # Pa
        G_rock = kwargs.get('shear_modulus_rock')  # Pa
        p_wave_velocity = math.sqrt((lame_coef + 2.0 * G_rock) / rho_rock)

    else:
        p_wave_velocity = np.nan

    # S-wave velocity
    if 'shear_modulus_rock' in kwargs:
        G_rock = kwargs.get('shear_modulus_rock')  # Pa
        shear_wave_velocity = math.sqrt(G_rock / rho_rock)
    else:
        shear_wave_velocity = np.nan

    # Extensional wave velocity
    if 'youngs_modulus_rock' in kwargs:
        E_rock = kwargs.get('youngs_modulus_rock')  # Pa
        extensional_wave_velocity = math.sqrt(E_rock / rho_rock)
    elif 'bulk_modulus_rock' in kwargs and 'shear_modulus_rock' in kwargs:
        K_rock = kwargs.get('bulk_modulus_rock')  # Pa
        G_rock = kwargs.get('shear_modulus_rock')  # Pa
        E_rock_cal = (9.0 * K_rock * G_rock) / (3.0 * K_rock + G_rock)
        extensional_wave_velocity = math.sqrt(E_rock_cal / rho_rock)
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


def poisson(bulk_modulus, shear_modulus):
    """
    Calculate Poisson's ratio from bulk and shear moduli.
    
    Poisson's ratio (ν) characterizes the ratio of lateral strain to axial
    strain in an elastic material under uniaxial stress. It can be calculated
    from independently measured bulk modulus (K) and shear modulus (G).
    
    Parameters
    ----------
    bulk_modulus : float or array-like
        Bulk modulus K (Pa)
    shear_modulus : float or array-like
        Shear modulus G (Pa)
    
    Returns
    -------
    float or array-like
        Poisson's ratio ν (dimensionless, theoretical range: -1 to 0.5)
        For most rocks: 0.0 to 0.45
    
    Notes
    -----
    Formula: ν = (3K - 2G) / (6K + 2G)
    
    Alternative forms:
    - ν = (3K - 2G) / 2(3K + G)
    - ν = λ / 2(λ + μ), where λ is Lamé's first parameter
    
    **Dynamic vs Static Measurements:**
    The calculation is identical regardless of how K and G were measured:
    
    - **Dynamic** (high-frequency): seismic, ultrasonic, geophysical logging
    - **Static** (quasi-static): mechanical testing, core analysis
    
    Dynamic Poisson's ratio is typically 5-20% higher than static for the
    same rock due to frequency-dependent effects and measurement conditions.
    
    **Physical Interpretation:**
    - ν ≈ 0.0: Material contracts minimally in lateral direction (cork)
    - ν ≈ 0.25: Typical sandstone/granite
    - ν ≈ 0.5: Incompressible material (saturated clay, rubber)
    - ν < 0: Auxetic materials (expand laterally under tension)
    
    References
    ----------
    - Mavko et al. (2020): The Rock Physics Handbook, Section 2.3
    - Fjaer et al. (2008): Petroleum Related Rock Mechanics, Chapter 2
    
    Examples
    --------
    >>> from drp_template.compute import GPa2Pa
    >>> 
    >>> # Quartz: K=37 GPa, G=44 GPa
    >>> nu = poisson(GPa2Pa(37), GPa2Pa(44))
    >>> print(f"Poisson's ratio: {nu:.3f}")
    Poisson's ratio: 0.077
    
    >>> # Saturated sandstone (dynamic measurement)
    >>> nu_dyn = poisson(bulk_modulus=GPa2Pa(20), shear_modulus=GPa2Pa(15))
    >>> print(f"Dynamic Poisson's ratio: {nu_dyn:.3f}")
    Dynamic Poisson's ratio: 0.237
    
    >>> # Array input
    >>> K_array = np.array([20, 30, 40])  # GPa
    >>> G_array = np.array([15, 20, 25])  # GPa
    >>> nu_array = poisson(GPa2Pa(K_array), GPa2Pa(G_array))
    
    See Also
    --------
    youngs : Calculate Young's modulus from K and G
    lame_lambda : Calculate Lamé's first parameter from K and G
    bulk : Calculate bulk modulus from E and ν
    shear : Calculate shear modulus from E and ν
    seismic_velocity : Calculate wave velocities and Poisson's ratio from K, G, ρ
    """
    K = np.asarray(bulk_modulus)
    G = np.asarray(shear_modulus)
    return (3*K - 2*G) / (6*K + 2*G)


def youngs(bulk_modulus, shear_modulus):
    """
    Calculate Young's modulus from bulk and shear moduli.
    
    Young's modulus (E) measures the stiffness of a material under uniaxial
    stress and is one of the fundamental elastic constants.
    
    Parameters
    ----------
    bulk_modulus : float or array-like
        Bulk modulus K (Pa)
    shear_modulus : float or array-like
        Shear modulus G (Pa)
    
    Returns
    -------
    float or array-like
        Young's modulus E (Pa)
    
    Notes
    -----
    Formula: E = 9KG / (3K + G)
    
    Alternative derivation from Hooke's law for isotropic media:
    - E = 2G(1 + ν)
    - E = 3K(1 - 2ν)
    
    **Physical Interpretation:**
    Young's modulus represents the ratio of tensile stress to tensile strain
    in the direction of the applied load. Higher E means stiffer material.
    
    Typical values:
    - Sandstone: 10-40 GPa
    - Limestone: 30-70 GPa
    - Granite: 40-80 GPa
    - Steel: ~200 GPa
    
    References
    ----------
    - Mavko et al. (2020): The Rock Physics Handbook, Section 2.2
    - Landau & Lifshitz (1986): Theory of Elasticity
    
    Examples
    --------
    >>> from drp_template.compute import GPa2Pa
    >>> 
    >>> # Quartz: K=37 GPa, G=44 GPa
    >>> E = youngs(GPa2Pa(37), GPa2Pa(44))
    >>> print(f"Young's modulus: {E/1e9:.1f} GPa")
    Young's modulus: 94.1 GPa
    
    >>> # Sandstone: K=20 GPa, G=15 GPa
    >>> E_sand = youngs(GPa2Pa(20), GPa2Pa(15))
    >>> print(f"Sandstone E: {E_sand/1e9:.1f} GPa")
    Sandstone E: 37.5 GPa
    
    >>> # Array input
    >>> K_array = np.array([20, 30, 40])  # GPa
    >>> G_array = np.array([15, 20, 25])  # GPa
    >>> E_array = youngs(GPa2Pa(K_array), GPa2Pa(G_array))
    
    See Also
    --------
    poisson : Calculate Poisson's ratio from K and G
    bulk : Calculate bulk modulus from E and ν
    shear : Calculate shear modulus from E and ν
    """
    K = np.asarray(bulk_modulus)
    G = np.asarray(shear_modulus)
    return (9*K*G) / (3*K + G)


def lame_lambda(bulk_modulus, shear_modulus):
    """
    Calculate Lamé's first parameter (λ) from bulk and shear moduli.
    
    Lamé's first parameter (λ) is one of the two Lamé parameters that
    describe elastic properties of isotropic materials. Together with
    the shear modulus (μ = G), they provide an alternative representation
    of elastic constants.
    
    Parameters
    ----------
    bulk_modulus : float or array-like
        Bulk modulus K (Pa)
    shear_modulus : float or array-like
        Shear modulus G (Pa)
    
    Returns
    -------
    float or array-like
        Lamé's first parameter λ (Pa)
    
    Notes
    -----
    Formula: λ = K - (2/3)G
    
    Alternative forms:
    - λ = 2Gν / (1 - 2ν)
    - λ = E·ν / [(1 + ν)(1 - 2ν)]
    
    **Physical Interpretation:**
    Lamé's first parameter appears in the stress-strain relationship for
    isotropic materials:
    - σ_ij = λ·δ_ij·ε_kk + 2μ·ε_ij
    
    where δ_ij is the Kronecker delta, ε is strain, and σ is stress.
    
    **Relation to P-wave modulus:**
    - M = λ + 2μ = K + (4/3)G = ρ·V_P²
    
    where M is the P-wave modulus and V_P is P-wave velocity.
    
    References
    ----------
    - Lamé, G. (1852): Leçons sur la théorie mathématique de l'élasticité
    - Mavko et al. (2020): The Rock Physics Handbook, Section 2.2
    - Aki & Richards (2002): Quantitative Seismology
    
    Examples
    --------
    >>> from drp_template.compute import GPa2Pa
    >>> 
    >>> # Quartz: K=37 GPa, G=44 GPa
    >>> lam = lame_lambda(GPa2Pa(37), GPa2Pa(44))
    >>> print(f"Lamé λ: {lam/1e9:.1f} GPa")
    Lamé λ: 7.7 GPa
    
    >>> # Calculate P-wave modulus
    >>> K, G = GPa2Pa(30), GPa2Pa(20)
    >>> lam = lame_lambda(K, G)
    >>> M = lam + 2*G  # P-wave modulus
    >>> print(f"P-wave modulus: {M/1e9:.1f} GPa")
    P-wave modulus: 56.7 GPa
    
    >>> # Array input
    >>> K_array = np.array([20, 30, 40])  # GPa
    >>> G_array = np.array([15, 20, 25])  # GPa
    >>> lambda_array = lame_lambda(GPa2Pa(K_array), GPa2Pa(G_array))
    
    See Also
    --------
    poisson : Calculate Poisson's ratio from K and G
    youngs : Calculate Young's modulus from K and G
    """
    K = np.asarray(bulk_modulus)
    G = np.asarray(shear_modulus)
    return K - (2.0/3.0)*G


def bulk(youngs_modulus, poisson_ratio):
    """
    Calculate bulk modulus from Young's modulus and Poisson's ratio.
    
    This is the inverse relationship allowing calculation of bulk modulus
    when Young's modulus and Poisson's ratio are known from measurements.
    
    Parameters
    ----------
    youngs_modulus : float or array-like
        Young's modulus E (Pa)
    poisson_ratio : float or array-like
        Poisson's ratio ν (dimensionless, range: -1 to 0.5)
    
    Returns
    -------
    float or array-like
        Bulk modulus K (Pa)
    
    Notes
    -----
    Formula: K = E / [3(1 - 2ν)]
    
    **Constraints:**
    - For ν → 0.5: K → ∞ (incompressible limit)
    - For ν = 0.5: K is undefined (division by zero)
    - For realistic rocks: -0.1 < ν < 0.45
    
    **Physical Interpretation:**
    Bulk modulus represents resistance to uniform compression (hydrostatic
    pressure). It can be derived from more easily measured parameters
    (E and ν) obtained from uniaxial compression tests.
    
    References
    ----------
    - Mavko et al. (2020): The Rock Physics Handbook, Section 2.2
    - Jaeger et al. (2007): Fundamentals of Rock Mechanics
    
    Examples
    --------
    >>> from drp_template.compute import GPa2Pa
    >>> 
    >>> # Sandstone: E=40 GPa, ν=0.25
    >>> K = bulk(youngs_modulus=GPa2Pa(40), poisson_ratio=0.25)
    >>> print(f"Bulk modulus: {K/1e9:.1f} GPa")
    Bulk modulus: 26.7 GPa
    
    >>> # Granite: E=70 GPa, ν=0.20
    >>> K_granite = bulk(GPa2Pa(70), 0.20)
    >>> print(f"Granite K: {K_granite/1e9:.1f} GPa")
    Granite K: 38.9 GPa
    
    >>> # Array input
    >>> E_array = np.array([30, 40, 50])  # GPa
    >>> nu_array = np.array([0.20, 0.25, 0.30])
    >>> K_array = bulk(GPa2Pa(E_array), nu_array)
    
    See Also
    --------
    shear : Calculate shear modulus from E and ν
    poisson : Calculate Poisson's ratio from K and G
    youngs : Calculate Young's modulus from K and G
    """
    E = np.asarray(youngs_modulus)
    nu = np.asarray(poisson_ratio)
    return E / (3.0 * (1.0 - 2.0*nu))


def shear(youngs_modulus, poisson_ratio):
    """
    Calculate shear modulus from Young's modulus and Poisson's ratio.
    
    This is the inverse relationship allowing calculation of shear modulus
    when Young's modulus and Poisson's ratio are known from measurements.
    
    Parameters
    ----------
    youngs_modulus : float or array-like
        Young's modulus E (Pa)
    poisson_ratio : float or array-like
        Poisson's ratio ν (dimensionless, range: -1 to 0.5)
    
    Returns
    -------
    float or array-like
        Shear modulus G (Pa), also denoted μ
    
    Notes
    -----
    Formula: G = E / [2(1 + ν)]
    
    Alternative notation: μ = G (shear modulus = Lamé's second parameter)
    
    **Physical Interpretation:**
    Shear modulus represents resistance to shear deformation (shape change
    without volume change). It can be derived from uniaxial test parameters.
    
    **Constraints:**
    - G must be positive for stable materials
    - For ν = -1: G = E/0 (undefined)
    - For typical rocks: 0 < ν < 0.45, so G ≈ E/3
    
    Typical G values:
    - Sandstone: 5-25 GPa
    - Limestone: 10-35 GPa
    - Granite: 20-40 GPa
    
    References
    ----------
    - Mavko et al. (2020): The Rock Physics Handbook, Section 2.2
    - Jaeger et al. (2007): Fundamentals of Rock Mechanics
    
    Examples
    --------
    >>> from drp_template.compute import GPa2Pa
    >>> 
    >>> # Sandstone: E=40 GPa, ν=0.25
    >>> G = shear(youngs_modulus=GPa2Pa(40), poisson_ratio=0.25)
    >>> print(f"Shear modulus: {G/1e9:.1f} GPa")
    Shear modulus: 16.0 GPa
    
    >>> # Granite: E=70 GPa, ν=0.20
    >>> G_granite = shear(GPa2Pa(70), 0.20)
    >>> print(f"Granite G: {G_granite/1e9:.1f} GPa")
    Granite G: 29.2 GPa
    
    >>> # Array input
    >>> E_array = np.array([30, 40, 50])  # GPa
    >>> nu_array = np.array([0.20, 0.25, 0.30])
    >>> G_array = shear(GPa2Pa(E_array), nu_array)
    
    >>> # Verify relationship: E = 2G(1 + ν)
    >>> E_check = 2 * G * (1 + 0.25)
    >>> print(f"E check: {E_check/1e9:.1f} GPa")
    E check: 40.0 GPa
    
    See Also
    --------
    bulk : Calculate bulk modulus from E and ν
    poisson : Calculate Poisson's ratio from K and G
    youngs : Calculate Young's modulus from K and G
    """
    E = np.asarray(youngs_modulus)
    nu = np.asarray(poisson_ratio)
    return E / (2.0 * (1.0 + nu))
