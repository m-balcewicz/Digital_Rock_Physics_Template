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


def gassmann_fluid_substitution(bulk_modulus_mineral, bulk_modulus_dry, 
                                 bulk_modulus_fluid1, bulk_modulus_fluid2, porosity, 
                                 shear_modulus_dry=None, bulk_modulus_sat1=None, return_moduli_only=False):
    """
    Perform Gassmann fluid substitution to predict saturated rock properties.
    
    Calculates the bulk modulus (and optionally velocities) of a porous rock
    saturated with a new fluid (fluid 2) given properties with original fluid
    (fluid 1) or dry frame properties.
    
    Parameters
    ----------
    bulk_modulus_mineral : float
        Bulk modulus of mineral grains (Pa). For multi-mineral rocks, use
        Voigt-Reuss-Hill or Hashin-Shtrikman average.
    bulk_modulus_dry : float
        Bulk modulus of dry rock frame (Pa). If unknown, can be computed from
        bulk_modulus_sat1 using inverse Gassmann.
    bulk_modulus_fluid1 : float
        Bulk modulus of original pore fluid (Pa). Use 0 for dry/gas.
    bulk_modulus_fluid2 : float
        Bulk modulus of new pore fluid (Pa).
    porosity : float
        Porosity (fraction, 0-1).
    shear_modulus_dry : float, optional
        Shear modulus of dry rock frame (Pa). Required if velocities are needed.
        Gassmann assumes shear modulus is fluid-independent: shear_modulus_sat = shear_modulus_dry.
    bulk_modulus_sat1 : float, optional
        Bulk modulus of rock saturated with fluid 1 (Pa). If provided with bulk_modulus_fluid1,
        bulk_modulus_dry will be back-calculated using inverse Gassmann.
    return_moduli_only : bool, optional
        If True, return only moduli dict. If False and shear_modulus_dry is provided,
        also calculate velocities. Default is False.
    
    Returns
    -------
    dict
        Dictionary containing:
        - 'bulk_modulus_sat2' : Bulk modulus with new fluid (Pa)
        - 'shear_modulus_sat2' : Shear modulus with new fluid (Pa) - equals shear_modulus_dry
        - 'bulk_modulus_dry' : Dry frame bulk modulus (Pa)
        - 'Vp_sat2' : P-wave velocity with new fluid (m/s) [if shear_modulus_dry provided]
        - 'Vs_sat2' : S-wave velocity with new fluid (m/s) [if shear_modulus_dry provided]
        - 'rho_sat2' : Bulk density with new fluid (kg/m³) [if densities provided]
    
    Raises
    ------
    ValueError
        If parameters are out of physical bounds or inconsistent.
    
    Notes
    -----
    **Gassmann's Equation (Forward):**
    
    bulk_modulus_sat = bulk_modulus_dry + (1 - bulk_modulus_dry/bulk_modulus_mineral)² / 
                       (φ/bulk_modulus_fluid + (1-φ)/bulk_modulus_mineral - bulk_modulus_dry/bulk_modulus_mineral²)
    
    **Key Assumptions:**
    
    1. Low frequency (quasi-static, < 100 Hz for seismic)
    2. Isotropic, homogeneous mineral modulus
    3. Pores are interconnected (fluid pressure equilibrated)
    4. No chemical interaction between fluid and rock
    5. Monomineralic or isotropic mineral mixture
    6. Shear modulus is fluid-independent: shear_modulus_sat = shear_modulus_dry
    
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
    
    **Inverse Gassmann (Back-calculate bulk_modulus_dry):**
    
    If bulk_modulus_sat1 is known, bulk_modulus_dry can be computed by solving Gassmann's equation
    for bulk_modulus_dry. This is useful when you have saturated measurements but need
    the dry frame modulus.
    
    References
    ----------
    - Gassmann (1951): Original derivation
    - Mavko et al. (2020): The Rock Physics Handbook, Section 5.5
    - Berryman (1999): Origin of Gassmann's equations
    
    Examples
    --------
    >>> from drp_template.compute.conversions import GPa2Pa
    >>> # Forward substitution: Water → Oil
    >>> result = gassmann_fluid_substitution(
    ...     bulk_modulus_mineral=GPa2Pa(37),      # Quartz
    ...     bulk_modulus_dry=GPa2Pa(10),          # Dry sandstone
    ...     bulk_modulus_fluid1=GPa2Pa(2.2),      # Water
    ...     bulk_modulus_fluid2=GPa2Pa(0.8),      # Oil
    ...     porosity=0.20,
    ...     shear_modulus_dry=GPa2Pa(8)
    ... )
    >>> print(f"bulk_modulus_sat(oil) = {result['bulk_modulus_sat2']/1e9:.2f} GPa")
    >>> print(f"Vp(oil) = {result['Vp_sat2']:.0f} m/s")
    
    >>> # Inverse Gassmann: Calculate dry modulus from saturated
    >>> result = gassmann_fluid_substitution(
    ...     bulk_modulus_mineral=GPa2Pa(37),
    ...     bulk_modulus_dry=None,                    # Will be calculated
    ...     bulk_modulus_fluid1=GPa2Pa(2.2),          # Current fluid (water)
    ...     bulk_modulus_fluid2=0,                    # New fluid (air/dry)
    ...     porosity=0.15,
    ...     bulk_modulus_sat1=GPa2Pa(18),             # Measured saturated bulk modulus
    ...     shear_modulus_dry=GPa2Pa(12)
    ... )
    >>> print(f"bulk_modulus_dry = {result['bulk_modulus_dry']/1e9:.2f} GPa")
    
    >>> # Dry → Saturated
    >>> result = gassmann_fluid_substitution(
    ...     bulk_modulus_mineral=GPa2Pa(37),
    ...     bulk_modulus_dry=GPa2Pa(15),
    ...     bulk_modulus_fluid1=0,                    # Dry
    ...     bulk_modulus_fluid2=GPa2Pa(2.2),          # Water
    ...     porosity=0.10,
    ...     shear_modulus_dry=GPa2Pa(18)
    ... )
    >>> print(f"Dry: K={15:.1f} GPa, Vp={result['Vp_sat2']:.0f} m/s")
    
    >>> # Multi-mineral rock (use VRH for bulk_modulus_mineral first)
    >>> from drp_template.compute.rockphysics.bounds import voigt_reuss_hill_bounds
    >>> import numpy as np
    >>> mineral_props = voigt_reuss_hill_bounds(
    ...     fractions=[0.7, 0.3],
    ...     bulk_moduli=GPa2Pa(np.array([37, 76])),      # Quartz, Calcite
    ...     shear_moduli=GPa2Pa(np.array([44, 32]))
    ... )
    >>> result = gassmann_fluid_substitution(
    ...     bulk_modulus_mineral=mineral_props['bulk_modulus_hill'],
    ...     bulk_modulus_dry=GPa2Pa(12),
    ...     bulk_modulus_fluid1=GPa2Pa(2.2),
    ...     bulk_modulus_fluid2=GPa2Pa(0.6),
    ...     porosity=0.18
    ... )
    """
    # Validation
    if porosity < 0 or porosity > 1:
        raise ValueError(f"Porosity must be between 0 and 1. Got: {porosity}")
    
    if bulk_modulus_mineral <= 0:
        raise ValueError(f"bulk_modulus_mineral must be positive. Got: {bulk_modulus_mineral}")
    
    if bulk_modulus_fluid1 < 0 or bulk_modulus_fluid2 < 0:
        raise ValueError(f"Fluid bulk moduli must be non-negative. Got bulk_modulus_fluid1={bulk_modulus_fluid1}, bulk_modulus_fluid2={bulk_modulus_fluid2}")
    
    # If bulk_modulus_sat1 is provided, back-calculate bulk_modulus_dry using inverse Gassmann
    if bulk_modulus_sat1 is not None and bulk_modulus_dry is None:
        # Inverse Gassmann to find bulk_modulus_dry from bulk_modulus_sat1
        # Rearranging Gassmann's equation (numerical solution)
        # bulk_modulus_dry = bulk_modulus_sat1 * (φ*bulk_modulus_mineral/bulk_modulus_fluid1 + 1 - φ - bulk_modulus_sat1/bulk_modulus_mineral) / 
        #                    (φ*bulk_modulus_mineral/bulk_modulus_fluid1 + 1 - bulk_modulus_sat1/bulk_modulus_mineral)
        
        if bulk_modulus_fluid1 == 0:  # If original fluid was gas/dry, bulk_modulus_sat1 IS bulk_modulus_dry
            bulk_modulus_dry = bulk_modulus_sat1
        else:
            # General inverse Gassmann formula
            numerator = bulk_modulus_sat1 * (porosity * bulk_modulus_mineral / bulk_modulus_fluid1 + 1 - porosity - bulk_modulus_sat1 / bulk_modulus_mineral)
            denominator = porosity * bulk_modulus_mineral / bulk_modulus_fluid1 + 1 - bulk_modulus_sat1 / bulk_modulus_mineral
            bulk_modulus_dry = numerator / denominator
            
        if bulk_modulus_dry < 0:
            raise ValueError(
                f"Back-calculated bulk_modulus_dry is negative ({bulk_modulus_dry/1e9:.2f} GPa). "
                f"Check input parameters for physical consistency."
            )
    
    elif bulk_modulus_dry is None:
        raise ValueError("Either bulk_modulus_dry or bulk_modulus_sat1 must be provided.")
    
    # Validate bulk_modulus_dry is physically reasonable
    if bulk_modulus_dry < 0:
        raise ValueError(f"bulk_modulus_dry must be non-negative. Got: {bulk_modulus_dry}")
    
    if bulk_modulus_dry > bulk_modulus_mineral:
        raise ValueError(
            f"bulk_modulus_dry ({bulk_modulus_dry/1e9:.2f} GPa) cannot exceed bulk_modulus_mineral ({bulk_modulus_mineral/1e9:.2f} GPa)"
        )
    
    # Forward Gassmann: Calculate bulk_modulus_sat2 with new fluid
    # bulk_modulus_sat = bulk_modulus_dry + (1 - bulk_modulus_dry/bulk_modulus_mineral)² / 
    #                    (φ/bulk_modulus_fluid + (1-φ)/bulk_modulus_mineral - bulk_modulus_dry/bulk_modulus_mineral²)
    
    alpha = 1 - bulk_modulus_dry / bulk_modulus_mineral  # Biot coefficient
    
    if bulk_modulus_fluid2 == 0:  # New fluid is gas/dry
        bulk_modulus_sat2 = bulk_modulus_dry
    else:
        denominator = porosity / bulk_modulus_fluid2 + (1 - porosity) / bulk_modulus_mineral - bulk_modulus_dry / bulk_modulus_mineral**2
        bulk_modulus_sat2 = bulk_modulus_dry + alpha**2 / denominator
    
    # Shear modulus is fluid-independent in Gassmann theory
    shear_modulus_sat2 = shear_modulus_dry if shear_modulus_dry is not None else None
    
    # Build result dictionary
    result = {
        'bulk_modulus_sat2': float(bulk_modulus_sat2),
        'shear_modulus_sat2': float(shear_modulus_sat2) if shear_modulus_sat2 is not None else None,
        'bulk_modulus_dry': float(bulk_modulus_dry),
    }
    
    # Calculate velocities if shear modulus is provided
    if shear_modulus_dry is not None and not return_moduli_only:
        # Need density - simplified assumption (can be improved)
        # For accurate velocities, user should provide densities
        # Here we use a reasonable estimate
        
        # Typical mineral density (can be refined)
        rho_mineral = 2650  # kg/m³ (approximate for quartz/sandstone)
        rho_fluid2 = 1000   # kg/m³ (approximate for water/oil)
        
        # Bulk density
        rho_sat2 = (1 - porosity) * rho_mineral + porosity * rho_fluid2
        
        # Elastic moduli
        M_sat2 = bulk_modulus_sat2 + 4.0 / 3.0 * shear_modulus_sat2  # P-wave modulus
        
        # Velocities
        Vp_sat2 = np.sqrt(M_sat2 / rho_sat2)
        Vs_sat2 = np.sqrt(shear_modulus_sat2 / rho_sat2)
        
        result['Vp_sat2'] = float(Vp_sat2)
        result['Vs_sat2'] = float(Vs_sat2)
        result['rho_sat2'] = float(rho_sat2)
    
    return result
