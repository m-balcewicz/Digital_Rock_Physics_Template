"""
Density Mixing Calculations
============================

Calculate effective densities for solid and fluid mixtures.

References
----------
- Mavko, G., Mukerji, T., Dvorkin, J. (2020): The Rock Physics Handbook

Author
------
Martin Balcewicz (martin.balcewicz@rockphysics.org)
"""

import numpy as np

__all__ = ['density_solid_mix', 'density_fluid_mix']


def density_solid_mix(fractions, densities):
    """
    Calculate the effective density of a solid mixture using arithmetic (Voigt) averaging.
    
    Uses volume-weighted arithmetic average: ρ_mix = Σ(f_i × ρ_i)
    
    Parameters
    ----------
    fractions : array-like
        Volume fractions of the solid components. Must sum to 1.
    densities : array-like
        Densities of the solid components (kg/m³).
        
    Returns
    -------
    float
        Mixed solid density (kg/m³).
        
    Raises
    ------
    ValueError
        If input arrays have different lengths or fractions don't sum to 1.
        
    Notes
    -----
    The effective density follows: f_total = f_porosity + f_solid
    
    This is an exact relation (not a bound) for density mixing.
    
    Examples
    --------
    >>> # Quartz-Calcite mixture (60% Quartz, 40% Calcite)
    >>> rho_mix = density_solid_mix(
    ...     fractions=[0.6, 0.4],
    ...     densities=[2650, 2710]
    ... )
    >>> print(f"Effective density: {rho_mix:.1f} kg/m³")
    Effective density: 2674.0 kg/m³
    
    >>> # Three-component mixture
    >>> rho_mix = density_solid_mix(
    ...     fractions=[0.5, 0.3, 0.2],
    ...     densities=[2650, 2710, 2850]
    ... )
    """
    fractions = np.asarray(fractions)
    densities = np.asarray(densities)
    
    if len(fractions) != len(densities):
        raise ValueError(
            f'Input fractions and densities must have the same length. '
            f'Got: fractions({len(fractions)}), densities({len(densities)})'
        )
    
    if not np.isclose(np.sum(fractions), 1.0):
        raise ValueError(
            f'Volume fractions must sum to 1. Got sum: {np.sum(fractions):.6f}'
        )
    
    rho_mix = np.sum(fractions * densities)
    
    return float(rho_mix)


def density_fluid_mix(saturations, densities):
    """
    Calculate the effective density of a fluid mixture using arithmetic (Voigt) averaging.
    
    Uses saturation-weighted arithmetic average: ρ_fluid = Σ(S_i × ρ_i)
    
    Parameters
    ----------
    saturations : array-like
        Saturation of the fluid phases. Must sum to 1.
    densities : array-like
        Densities of the fluid components (kg/m³).
        
    Returns
    -------
    float
        Mixed fluid density (kg/m³).
        
    Raises
    ------
    ValueError
        If input arrays have different lengths or saturations don't sum to 1.
        
    Notes
    -----
    This is an exact relation for fluid density mixing in porous media.
    Saturations represent volume fractions within the pore space.
    
    Examples
    --------
    >>> # Water-oil mixture (70% water, 30% oil)
    >>> rho_fluid = density_fluid_mix(
    ...     saturations=[0.7, 0.3],
    ...     densities=[1000, 850]
    ... )
    >>> print(f"Effective fluid density: {rho_fluid:.1f} kg/m³")
    Effective fluid density: 955.0 kg/m³
    
    >>> # Water-oil-gas mixture
    >>> rho_fluid = density_fluid_mix(
    ...     saturations=[0.5, 0.3, 0.2],
    ...     densities=[1000, 850, 200]
    ... )
    """
    saturations = np.asarray(saturations)
    densities = np.asarray(densities)
    
    if len(saturations) != len(densities):
        raise ValueError(
            f'Input saturations and densities must have the same length. '
            f'Got: saturations({len(saturations)}), densities({len(densities)})'
        )
    
    if not np.isclose(np.sum(saturations), 1.0):
        raise ValueError(
            f'Saturations must sum to 1. Got sum: {np.sum(saturations):.6f}'
        )
    
    rho_fluid_mix = np.sum(saturations * densities)
    
    return float(rho_fluid_mix)
