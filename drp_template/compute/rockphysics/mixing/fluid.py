"""
Fluid Mixing Laws
=================

Empirical and theoretical mixing laws for multi-phase fluid systems.

References
----------
- Brie et al. (1995): Shear velocity prediction in porous rocks
- Wood, A.B. (1955): A Textbook of Sound
- Mavko, G., Mukerji, T., Dvorkin, J. (2020): The Rock Physics Handbook

Author
------
Martin Balcewicz (martin.balcewicz@rockphysics.org)
"""

import numpy as np

__all__ = ['brie_fluid_mixing', 'wood_fluid_mixing']


def brie_fluid_mixing(s_water, s_oil, s_gas, k_water, k_oil, k_gas, exponent=3):
    """
    Calculate effective fluid bulk modulus using Brie's empirical equation.
    
    Brie's equation provides an empirical mixing law for patchy fluid mixtures,
    intermediate between homogeneous (Reuss) and patchy (Voigt) saturation patterns.
    
    The formula is: K_eff = [1/(S_w/K_w + S_o/K_o) - K_g] × (1 - S_g)^e + K_g
    
    Parameters
    ----------
    s_water : float
        Water saturation (0-1).
    s_oil : float
        Oil saturation (0-1).
    s_gas : float
        Gas saturation (0-1). Must satisfy: s_water + s_oil + s_gas = 1.
    k_water : float
        Bulk modulus of water (Pa).
    k_oil : float
        Bulk modulus of oil (Pa).
    k_gas : float
        Bulk modulus of gas (Pa).
    exponent : float, optional
        Empirical constant (default=3 from original experiments).
        Controls the degree of fluid mixing:
        - e = 1: Approaches uniform saturation (Reuss bound)
        - e = 3: Original Brie calibration
        - e → ∞: Approaches patchy saturation (Voigt bound)
        
    Returns
    -------
    float
        Effective fluid bulk modulus using Brie's law (Pa).
        
    Notes
    -----
    Brie's equation is an empirical relation calibrated to experimental data.
    It provides better estimates than simple Voigt or Reuss averages for
    partially saturated rocks where fluid distribution is complex.
    
    The exponent 'e' should be calibrated to specific rock types when possible.
    
    References
    ----------
    Brie, A., Pampuri, F., Marsala, A.F., and Meazza, O. (1995): Shear sonic
    interpretation in gas-bearing sands, SPE Annual Technical Conference,
    Paper SPE 30595, 701-710.
        
    Examples
    --------
    >>> # Water-gas mixture (50% water, 50% gas)
    >>> k_brie = brie_fluid_mixing(
    ...     s_water=0.5, s_oil=0.0, s_gas=0.5,
    ...     k_water=2.2e9, k_oil=0, k_gas=0.01e9,
    ...     exponent=3
    ... )
    >>> print(f"Effective K_fluid: {k_brie/1e9:.3f} GPa")
    
    >>> # Water-oil-gas mixture
    >>> k_brie = brie_fluid_mixing(
    ...     s_water=0.4, s_oil=0.3, s_gas=0.3,
    ...     k_water=2.2e9, k_oil=0.8e9, k_gas=0.01e9,
    ...     exponent=3
    ... )
    
    >>> # Effect of exponent on mixing
    >>> for e in [1, 2, 3, 5, 10]:
    ...     k = brie_fluid_mixing(0.5, 0, 0.5, 2.2e9, 0, 0.01e9, exponent=e)
    ...     print(f"e={e}: K_fluid = {k/1e9:.3f} GPa")
    """
    # Validate saturations sum to 1
    total_saturation = s_water + s_oil + s_gas
    if not np.isclose(total_saturation, 1.0):
        raise ValueError(
            f'Saturations must sum to 1. Got: '
            f's_water={s_water}, s_oil={s_oil}, s_gas={s_gas}, '
            f'sum={total_saturation:.6f}'
        )
    
    # Handle zero bulk moduli (replace with small value to avoid division by zero)
    k_water = k_water if k_water > 0 else 1e-10
    k_oil = k_oil if k_oil > 0 else 1e-10
    k_gas = k_gas if k_gas > 0 else 1e-10
    
    # Brie's equation
    if s_oil > 0:
        # Water + oil mixture (no gas case handled first)
        k_liquid = 1.0 / (s_water / k_water + s_oil / k_oil)
    else:
        # Water only (no oil)
        k_liquid = k_water
    
    # Add gas contribution with Brie exponent
    k_brie = (k_liquid - k_gas) * (1 - s_gas)**exponent + k_gas
    
    return float(k_brie)


def wood_fluid_mixing(fractions, bulk_moduli, densities):
    """
    Calculate effective fluid properties using Wood's equation.
    
    Wood's (1955) formula gives the exact P-wave velocity in fluid suspensions
    or mixtures where heterogeneities are small compared to wavelength. Uses
    Reuss (isostress) averaging for bulk modulus and arithmetic averaging for density.
    
    Parameters
    ----------
    fractions : array-like
        Volume fractions of each fluid phase. Must sum to 1.
    bulk_moduli : array-like
        Bulk moduli of each fluid phase (Pa).
    densities : array-like
        Densities of each fluid phase (kg/m³).
    
    Returns
    -------
    dict
        Dictionary containing:
        - 'K_reuss' : Reuss average bulk modulus (Pa)
        - 'rho_avg' : Arithmetic average density (kg/m³)
        - 'Vp' : P-wave velocity in fluid mixture (m/s)
    
    Raises
    ------
    ValueError
        If arrays have different lengths or fractions don't sum to 1.
    
    Notes
    -----
    Wood's formula applies when:
    - Heterogeneity scale << wavelength
    - Fluid suspension or mixture
    - Long wavelength limit (quasi-static)
    
    The formulas are:
    - K_Reuss = 1 / Σ(f_i / K_i)  (Harmonic average)
    - ρ_avg = Σ(f_i × ρ_i)        (Arithmetic average)
    - V_P = √(K_Reuss / ρ_avg)    (P-wave velocity)
    
    Wood's equation is exact for fluid mixtures in the long wavelength limit,
    unlike empirical formulas like Brie's law.
    
    References
    ----------
    - Wood, A.B. (1955): A Textbook of Sound, 3rd edition
    - Mavko, G., Mukerji, T., Dvorkin, J. (2020): The Rock Physics Handbook,
      3rd edition, Section on Hashin-Shtrikman-Walpole Bounds
    
    Examples
    --------
    >>> # Example 1: Water-gas mixture
    >>> results = wood_fluid_mixing(
    ...     fractions=[0.6, 0.4],
    ...     bulk_moduli=[2.2e9, 0.01e9],  # Water, Gas
    ...     densities=[1000, 1.2]          # kg/m³
    ... )
    >>> print(f"Effective K_fluid: {results['K_reuss']/1e9:.3f} GPa")
    >>> print(f"P-wave velocity: {results['Vp']:.0f} m/s")
    
    >>> # Example 2: Quartz-water-air suspension
    >>> results = wood_fluid_mixing(
    ...     fractions=[0.6, 0.3, 0.1],
    ...     bulk_moduli=[37e9, 2.2e9, 1.31e5],  # Quartz, Water, Air
    ...     densities=[2650, 1000, 1.19]         # kg/m³
    ... )
    >>> print(f"Suspension Vp: {results['Vp']:.0f} m/s")
    
    >>> # Example 3: Brine-oil mixture
    >>> results = wood_fluid_mixing(
    ...     fractions=[0.7, 0.3],
    ...     bulk_moduli=[2.4e9, 0.8e9],  # Brine, Oil
    ...     densities=[1050, 850]         # kg/m³
    ... )
    >>> K_eff = results['K_reuss']
    >>> rho_eff = results['rho_avg']
    >>> Vp = results['Vp']
    """
    fractions = np.asarray(fractions, dtype=float)
    bulk_moduli = np.asarray(bulk_moduli, dtype=float)
    densities = np.asarray(densities, dtype=float)
    
    # Validation
    if not (len(fractions) == len(bulk_moduli) == len(densities)):
        raise ValueError(
            f'All input arrays must have the same length. Got: '
            f'fractions({len(fractions)}), bulk_moduli({len(bulk_moduli)}), '
            f'densities({len(densities)})'
        )
    
    if not np.isclose(np.sum(fractions), 1.0):
        raise ValueError(
            f'Fractions must sum to 1. Got sum: {np.sum(fractions):.6f}'
        )
    
    # Reuss (harmonic) average for bulk modulus
    K_reuss = 1.0 / np.sum(fractions / bulk_moduli)
    
    # Arithmetic (Voigt) average for density
    rho_avg = np.sum(fractions * densities)
    
    # P-wave velocity using Wood's formula
    Vp = np.sqrt(K_reuss / rho_avg)
    
    return {
        'K_reuss': float(K_reuss),
        'rho_avg': float(rho_avg),
        'Vp': float(Vp)
    }
