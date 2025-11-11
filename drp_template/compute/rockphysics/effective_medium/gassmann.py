"""
Gassmann Fluid Substitution
============================

Low-frequency fluid substitution in porous rocks using Gassmann's (1951) relations.

This module provides functions for predicting seismic properties of rocks
saturated with different fluids using Gassmann's theory.

References
----------
- Gassmann, F. (1951): Uber die Elastizitat poroser Medien, Vierteljahrsschrift
  der Naturforschenden Gesellschaft in Zurich, 96, 1-23
- Mavko, G., Mukerji, T., Dvorkin, J. (2020): The Rock Physics Handbook,
  3rd edition, Cambridge University Press

Author
------
Martin Balcewicz (martin.balcewicz@rockphysics.org)
"""

import numpy as np

__all__ = ['gassmann_fluid_substitution']


def gassmann_fluid_substitution(K_mineral, K_dry, K_fl1, K_fl2, porosity, 
                                 G_dry=None, K_sat1=None, return_moduli_only=False):
    """
    Perform Gassmann fluid substitution to predict saturated rock properties.
    
    Calculates the bulk modulus (and optionally velocities) of a porous rock
    saturated with a new fluid (fluid 2) given properties with original fluid
    (fluid 1) or dry frame properties.
    
    Parameters
    ----------
    K_mineral : float
        Bulk modulus of mineral grains (Pa). For multi-mineral rocks, use
        Voigt-Reuss-Hill or Hashin-Shtrikman average.
    K_dry : float
        Bulk modulus of dry rock frame (Pa). If unknown, can be computed from
        K_sat1 using inverse Gassmann.
    K_fl1 : float
        Bulk modulus of original pore fluid (Pa). Use 0 for dry/gas.
    K_fl2 : float
        Bulk modulus of new pore fluid (Pa).
    porosity : float
        Porosity (fraction, 0-1).
    G_dry : float, optional
        Shear modulus of dry rock frame (Pa). Required if velocities are needed.
        Gassmann assumes shear modulus is fluid-independent: G_sat = G_dry.
    K_sat1 : float, optional
        Bulk modulus of rock saturated with fluid 1 (Pa). If provided with K_fl1,
        K_dry will be back-calculated using inverse Gassmann.
    return_moduli_only : bool, optional
        If True, return only moduli dict. If False and G_dry is provided,
        also calculate velocities. Default is False.
    
    Returns
    -------
    dict
        Dictionary containing:
        - 'K_sat2' : Bulk modulus with new fluid (Pa)
        - 'G_sat2' : Shear modulus with new fluid (Pa) - equals G_dry
        - 'K_dry' : Dry frame bulk modulus (Pa)
        - 'Vp_sat2' : P-wave velocity with new fluid (m/s) [if G_dry provided]
        - 'Vs_sat2' : S-wave velocity with new fluid (m/s) [if G_dry provided]
        - 'rho_sat2' : Bulk density with new fluid (kg/m³) [if densities provided]
    
    Raises
    ------
    ValueError
        If parameters are out of physical bounds or inconsistent.
    
    Notes
    -----
    **Gassmann's Equation (Forward):**
    
    K_sat = K_dry + (1 - K_dry/K_mineral)² / (φ/K_fluid + (1-φ)/K_mineral - K_dry/K_mineral²)
    
    **Key Assumptions:**
    
    1. Low frequency (quasi-static, < 100 Hz for seismic)
    2. Isotropic, homogeneous mineral modulus
    3. Pores are interconnected (fluid pressure equilibrated)
    4. No chemical interaction between fluid and rock
    5. Monomineralic or isotropic mineral mixture
    6. Shear modulus is fluid-independent: G_sat = G_dry
    
    **When Gassmann Works Well:**
    
    - Low-frequency seismic data (< 100 Hz)
    - Clean sandstones with high permeability
    - Rocks with interconnected porosity
    
    **When Gassmann May Fail:**
    
    - High frequencies (sonic logs ~10 kHz, ultrasonic ~1 MHz)
    - Poorly connected pores (low permeability)
    - Clay-rich rocks (frequency-dependent)
    - Partial saturation (use Brie or patchy models)
    - Strong fluid-rock interaction
    
    **Inverse Gassmann (Back-calculate K_dry):**
    
    If K_sat1 is known, K_dry can be computed by solving Gassmann's equation
    for K_dry. This is useful when you have saturated measurements but need
    the dry frame modulus.
    
    References
    ----------
    - Gassmann (1951): Original derivation
    - Mavko et al. (2020): The Rock Physics Handbook, Section 5.5
    - Berryman (1999): Origin of Gassmann's equations
    
    Examples
    --------
    >>> # Forward substitution: Water → Oil
    >>> result = gassmann_fluid_substitution(
    ...     K_mineral=37e9,      # Quartz
    ...     K_dry=10e9,          # Dry sandstone
    ...     K_fl1=2.2e9,         # Water
    ...     K_fl2=0.8e9,         # Oil
    ...     porosity=0.20,
    ...     G_dry=8e9
    ... )
    >>> print(f"K_sat(oil) = {result['K_sat2']/1e9:.2f} GPa")
    >>> print(f"Vp(oil) = {result['Vp_sat2']:.0f} m/s")
    
    >>> # Inverse Gassmann: Calculate dry modulus from saturated
    >>> result = gassmann_fluid_substitution(
    ...     K_mineral=37e9,
    ...     K_dry=None,          # Will be calculated
    ...     K_fl1=2.2e9,         # Current fluid (water)
    ...     K_fl2=0,             # New fluid (air/dry)
    ...     porosity=0.15,
    ...     K_sat1=18e9,         # Measured saturated bulk modulus
    ...     G_dry=12e9
    ... )
    >>> print(f"K_dry = {result['K_dry']/1e9:.2f} GPa")
    
    >>> # Dry → Saturated
    >>> result = gassmann_fluid_substitution(
    ...     K_mineral=37e9,
    ...     K_dry=15e9,
    ...     K_fl1=0,             # Dry
    ...     K_fl2=2.2e9,         # Water
    ...     porosity=0.10,
    ...     G_dry=18e9
    ... )
    >>> print(f"Dry: K={15e9/1e9:.1f} GPa, Vp={result['Vp_sat2']:.0f} m/s")
    
    >>> # Multi-mineral rock (use VRH for K_mineral first)
    >>> from drp_template.compute.rockphysics.bounds import voigt_reuss_hill_bounds
    >>> mineral_props = voigt_reuss_hill_bounds(
    ...     fractions=[0.7, 0.3],
    ...     bulk_moduli=[37e9, 76e9],    # Quartz, Calcite
    ...     shear_moduli=[44e9, 32e9]
    ... )
    >>> result = gassmann_fluid_substitution(
    ...     K_mineral=mineral_props['K_hill'],
    ...     K_dry=12e9,
    ...     K_fl1=2.2e9,
    ...     K_fl2=0.6e9,
    ...     porosity=0.18
    ... )
    """
    # Validation
    if porosity < 0 or porosity > 1:
        raise ValueError(f"Porosity must be between 0 and 1. Got: {porosity}")
    
    if K_mineral <= 0:
        raise ValueError(f"K_mineral must be positive. Got: {K_mineral}")
    
    if K_fl1 < 0 or K_fl2 < 0:
        raise ValueError(f"Fluid bulk moduli must be non-negative. Got K_fl1={K_fl1}, K_fl2={K_fl2}")
    
    # If K_sat1 is provided, back-calculate K_dry using inverse Gassmann
    if K_sat1 is not None and K_dry is None:
        # Inverse Gassmann to find K_dry from K_sat1
        # Rearranging Gassmann's equation (numerical solution)
        # K_dry = K_sat1 * (φ*K_mineral/K_fl1 + 1 - φ - K_sat1/K_mineral) / 
        #         (φ*K_mineral/K_fl1 + 1 - K_sat1/K_mineral)
        
        if K_fl1 == 0:  # If original fluid was gas/dry, K_sat1 IS K_dry
            K_dry = K_sat1
        else:
            # General inverse Gassmann formula
            numerator = K_sat1 * (porosity * K_mineral / K_fl1 + 1 - porosity - K_sat1 / K_mineral)
            denominator = porosity * K_mineral / K_fl1 + 1 - K_sat1 / K_mineral
            K_dry = numerator / denominator
            
        if K_dry < 0:
            raise ValueError(
                f"Back-calculated K_dry is negative ({K_dry/1e9:.2f} GPa). "
                f"Check input parameters for physical consistency."
            )
    
    elif K_dry is None:
        raise ValueError("Either K_dry or K_sat1 must be provided.")
    
    # Validate K_dry is physically reasonable
    if K_dry < 0:
        raise ValueError(f"K_dry must be non-negative. Got: {K_dry}")
    
    if K_dry > K_mineral:
        raise ValueError(
            f"K_dry ({K_dry/1e9:.2f} GPa) cannot exceed K_mineral ({K_mineral/1e9:.2f} GPa)"
        )
    
    # Forward Gassmann: Calculate K_sat2 with new fluid
    # K_sat = K_dry + (1 - K_dry/K_mineral)² / (φ/K_fl + (1-φ)/K_mineral - K_dry/K_mineral²)
    
    alpha = 1 - K_dry / K_mineral  # Biot coefficient
    
    if K_fl2 == 0:  # New fluid is gas/dry
        K_sat2 = K_dry
    else:
        denominator = porosity / K_fl2 + (1 - porosity) / K_mineral - K_dry / K_mineral**2
        K_sat2 = K_dry + alpha**2 / denominator
    
    # Shear modulus is fluid-independent in Gassmann theory
    G_sat2 = G_dry if G_dry is not None else None
    
    # Build result dictionary
    result = {
        'K_sat2': float(K_sat2),
        'G_sat2': float(G_sat2) if G_sat2 is not None else None,
        'K_dry': float(K_dry),
    }
    
    # Calculate velocities if shear modulus is provided
    if G_dry is not None and not return_moduli_only:
        # Need density - simplified assumption (can be improved)
        # For accurate velocities, user should provide densities
        # Here we use a reasonable estimate
        
        # Typical mineral density (can be refined)
        rho_mineral = 2650  # kg/m³ (approximate for quartz/sandstone)
        rho_fluid2 = 1000   # kg/m³ (approximate for water/oil)
        
        # Bulk density
        rho_sat2 = (1 - porosity) * rho_mineral + porosity * rho_fluid2
        
        # Elastic moduli
        M_sat2 = K_sat2 + 4.0 / 3.0 * G_sat2  # P-wave modulus
        
        # Velocities
        Vp_sat2 = np.sqrt(M_sat2 / rho_sat2)
        Vs_sat2 = np.sqrt(G_sat2 / rho_sat2)
        
        result['Vp_sat2'] = float(Vp_sat2)
        result['Vs_sat2'] = float(Vs_sat2)
        result['rho_sat2'] = float(rho_sat2)
    
    return result
