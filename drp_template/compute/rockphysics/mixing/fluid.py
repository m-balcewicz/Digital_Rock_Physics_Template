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


def brie_fluid_mixing(saturation_water, saturation_oil, saturation_gas, 
                      bulk_modulus_water, bulk_modulus_oil, bulk_modulus_gas, exponent=3):
    """
    Calculate effective fluid bulk modulus using Brie's empirical equation.
    
    Brie's equation provides an empirical mixing law for patchy fluid mixtures,
    intermediate between homogeneous (Reuss) and patchy (Voigt) saturation patterns.
    
    The formula is: K_eff = [1/(S_w/K_w + S_o/K_o) - K_g] × (1 - S_g)^e + K_g
    
    Parameters
    ----------
    saturation_water : float
        Water saturation (0-1).
    saturation_oil : float
        Oil saturation (0-1).
    saturation_gas : float
        Gas saturation (0-1). Must satisfy: saturation_water + saturation_oil + saturation_gas = 1.
    bulk_modulus_water : float
        Bulk modulus of water (Pa).
    bulk_modulus_oil : float
        Bulk modulus of oil (Pa).
    bulk_modulus_gas : float
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
    >>> from drp_template.compute.conversions import GPa2Pa
    >>> # Water-gas mixture (50% water, 50% gas)
    >>> bulk_modulus_brie = brie_fluid_mixing(
    ...     saturation_water=0.5, saturation_oil=0.0, saturation_gas=0.5,
    ...     bulk_modulus_water=GPa2Pa(2.2), bulk_modulus_oil=0, bulk_modulus_gas=GPa2Pa(0.01),
    ...     exponent=3
    ... )
    >>> print(f"Effective bulk_modulus_fluid: {bulk_modulus_brie/1e9:.3f} GPa")
    
    >>> # Water-oil-gas mixture
    >>> bulk_modulus_brie = brie_fluid_mixing(
    ...     saturation_water=0.4, saturation_oil=0.3, saturation_gas=0.3,
    ...     bulk_modulus_water=GPa2Pa(2.2), bulk_modulus_oil=GPa2Pa(0.8), bulk_modulus_gas=GPa2Pa(0.01),
    ...     exponent=3
    ... )
    
    >>> # Effect of exponent on mixing
    >>> for e in [1, 2, 3, 5, 10]:
    ...     k = brie_fluid_mixing(0.5, 0, 0.5, GPa2Pa(2.2), 0, GPa2Pa(0.01), exponent=e)
    ...     print(f"e={e}: bulk_modulus_fluid = {k/1e9:.3f} GPa")
    """
    # Validate saturations sum to 1
    total_saturation = saturation_water + saturation_oil + saturation_gas
    if not np.isclose(total_saturation, 1.0):
        raise ValueError(
            f'Saturations must sum to 1. Got: '
            f'saturation_water={saturation_water}, saturation_oil={saturation_oil}, saturation_gas={saturation_gas}, '
            f'sum={total_saturation:.6f}'
        )
    
    # Handle zero bulk moduli (replace with small value to avoid division by zero)
    bulk_modulus_water = bulk_modulus_water if bulk_modulus_water > 0 else 1e-10
    bulk_modulus_oil = bulk_modulus_oil if bulk_modulus_oil > 0 else 1e-10
    bulk_modulus_gas = bulk_modulus_gas if bulk_modulus_gas > 0 else 1e-10
    
    # Brie's equation
    if saturation_oil > 0:
        # Water + oil mixture (no gas case handled first)
        bulk_modulus_liquid = 1.0 / (saturation_water / bulk_modulus_water + saturation_oil / bulk_modulus_oil)
    else:
        # Water only (no oil)
        bulk_modulus_liquid = bulk_modulus_water
    
    # Add gas contribution with Brie exponent
    bulk_modulus_brie = (bulk_modulus_liquid - bulk_modulus_gas) * (1 - saturation_gas)**exponent + bulk_modulus_gas
    
    return float(bulk_modulus_brie)


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
        - 'bulk_modulus_reuss' : Reuss average bulk modulus (Pa)
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
    - bulk_modulus_reuss = 1 / Σ(f_i / bulk_modulus_i)  (Harmonic average)
    - ρ_avg = Σ(f_i × ρ_i)                              (Arithmetic average)
    - V_P = √(bulk_modulus_reuss / ρ_avg)               (P-wave velocity)
    
    Wood's equation is exact for fluid mixtures in the long wavelength limit,
    unlike empirical formulas like Brie's law.
    
    References
    ----------
    - Wood, A.B. (1955): A Textbook of Sound, 3rd edition
    - Mavko, G., Mukerji, T., Dvorkin, J. (2020): The Rock Physics Handbook,
      3rd edition, Section on Hashin-Shtrikman-Walpole Bounds
    
    Examples
    --------
    >>> from drp_template.compute.conversions import GPa2Pa
    >>> import numpy as np
    >>> # Example 1: Water-gas mixture
    >>> results = wood_fluid_mixing(
    ...     fractions=[0.6, 0.4],
    ...     bulk_moduli=GPa2Pa(np.array([2.2, 0.01])),  # Water, Gas
    ...     densities=[1000, 1.2]                       # kg/m³
    ... )
    >>> print(f"Effective bulk_modulus_fluid: {results['bulk_modulus_reuss']/1e9:.3f} GPa")
    >>> print(f"P-wave velocity: {results['Vp']:.0f} m/s")
    
    >>> # Example 2: Quartz-water-air suspension
    >>> results = wood_fluid_mixing(
    ...     fractions=[0.6, 0.3, 0.1],
    ...     bulk_moduli=GPa2Pa(np.array([37, 2.2, 0.0001313])),  # Quartz, Water, Air
    ...     densities=[2650, 1000, 1.19]                          # kg/m³
    ... )
    >>> print(f"Suspension Vp: {results['Vp']:.0f} m/s")
    
    >>> # Example 3: Brine-oil mixture
    >>> results = wood_fluid_mixing(
    ...     fractions=[0.7, 0.3],
    ...     bulk_moduli=GPa2Pa(np.array([2.4, 0.8])),  # Brine, Oil
    ...     densities=[1050, 850]                       # kg/m³
    ... )
    >>> bulk_modulus_eff = results['bulk_modulus_reuss']
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
    bulk_modulus_reuss = 1.0 / np.sum(fractions / bulk_moduli)
    
    # Arithmetic (Voigt) average for density
    rho_avg = np.sum(fractions * densities)
    
    # P-wave velocity using Wood's formula
    Vp = np.sqrt(bulk_modulus_reuss / rho_avg)
    
    return {
        'bulk_modulus_reuss': float(bulk_modulus_reuss),
        'rho_avg': float(rho_avg),
        'Vp': float(Vp)
    }
