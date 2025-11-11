"""
Mixing Utilities
================

Utility functions for volume fraction normalization and preprocessing.

Author
------
Martin Balcewicz (martin.balcewicz@rockphysics.org)
"""

import numpy as np
import pandas as pd

__all__ = ['get_normalized_f_solid']


def get_normalized_f_solid(porosity, f_solid_components, components=None):
    """
    Calculate normalized solid fractions from absolute volume fractions and porosity.
    
    Converts absolute volume fractions (which include porosity) to normalized
    solid fractions that sum to 1 (excluding porosity).
    
    Relation: f_solid_normalized = f_solid_absolute / (1 - porosity)
    
    Parameters
    ----------
    porosity : float or array-like
        The porosity of the rock (0 <= porosity <= 1).
        Can be scalar for single sample or array for multiple samples.
    f_solid_components : array-like
        Initial absolute volume fractions of solid phases.
        Shape: (n_components,) for single sample
               (n_samples, n_components) for multiple samples
        Must satisfy: sum(f_solid_components) + porosity = 1
    components : list of str, optional
        Names of component phases. Required for DataFrame output.

    Returns
    -------
    pandas.DataFrame
        DataFrame with normalized solid fractions (summing to 1) and porosity.
        Columns: component names + 'Porosity'

    Raises
    ------
    ValueError
        If porosity + solid fractions don't sum to 1, or if dimensions mismatch.

    Examples
    --------
    >>> # Single sample: 20% porosity, 48% quartz, 32% calcite
    >>> result = get_normalized_f_solid(
    ...     porosity=0.2,
    ...     f_solid_components=np.array([0.48, 0.32]),
    ...     components=['Quartz', 'Calcite']
    ... )
    >>> print(result)
       Quartz  Calcite  Porosity
    0     0.6      0.4       0.2
    
    >>> # Multiple samples with varying porosity
    >>> result = get_normalized_f_solid(
    ...     porosity=np.array([0.15, 0.20, 0.25]),
    ...     f_solid_components=np.array([
    ...         [0.51, 0.34],  # 51% Q, 34% C, 15% porosity
    ...         [0.48, 0.32],  # 48% Q, 32% C, 20% porosity
    ...         [0.45, 0.30],  # 45% Q, 30% C, 25% porosity
    ...     ]),
    ...     components=['Quartz', 'Calcite']
    ... )
    >>> print(result)
       Quartz  Calcite  Porosity
    0    0.60     0.40      0.15
    1    0.60     0.40      0.20
    2    0.60     0.40      0.25
    
    Notes
    -----
    This function is useful for rock physics modeling where:
    - Input data provides absolute volume fractions including porosity
    - Models require normalized solid fractions (summing to 1)
    
    For example, if you have:
    - 20% porosity
    - 48% quartz (absolute)
    - 32% calcite (absolute)
    
    The normalized fractions are:
    - Quartz: 48/(1-0.2) = 0.6
    - Calcite: 32/(1-0.2) = 0.4
    """
    porosity = np.asarray(porosity)
    f_solid_components = np.asarray(f_solid_components)
    
    # Determine if single or multiple samples
    is_1d = (f_solid_components.ndim == 1)
    
    if is_1d:
        # Single sample case
        if components is None or len(components) != f_solid_components.shape[0]:
            raise ValueError(
                f'Invalid number of components. Expected {f_solid_components.shape[0]} '
                f'component names, got: {len(components) if components else 0}'
            )
        
        # Check if fractions + porosity sum to 1
        total = np.sum(f_solid_components) + porosity
        if not np.isclose(total, 1.0):
            raise ValueError(
                f'Sum of solid fractions + porosity must equal 1. '
                f'Got: {np.sum(f_solid_components):.6f} + {porosity:.6f} = {total:.6f}'
            )
        
        # Normalize
        normalized_fractions = f_solid_components / (1 - porosity)
        
        # Verify normalized fractions sum to 1
        if not np.isclose(np.sum(normalized_fractions), 1.0):
            raise ValueError(
                f'Normalized fractions do not sum to 1. Got: {np.sum(normalized_fractions):.6f}'
            )
        
        # Create DataFrame
        result_df = pd.DataFrame(
            [normalized_fractions],
            columns=components
        )
        result_df['Porosity'] = porosity
        
    elif f_solid_components.ndim == 2:
        # Multiple samples case
        if components is None or len(components) != f_solid_components.shape[1]:
            raise ValueError(
                f'Invalid number of components. Expected {f_solid_components.shape[1]} '
                f'component names, got: {len(components) if components else 0}'
            )
        
        # Check if porosity length matches number of samples
        if np.isscalar(porosity):
            porosity = np.full(f_solid_components.shape[0], porosity)
        elif len(porosity) != f_solid_components.shape[0]:
            raise ValueError(
                f'Length of porosity ({len(porosity)}) must match number of samples '
                f'({f_solid_components.shape[0]})'
            )
        
        # Check if each row sums to 1 with porosity
        row_sums = np.sum(f_solid_components, axis=1) + porosity
        if not np.allclose(row_sums, 1.0):
            problematic = np.where(~np.isclose(row_sums, 1.0))[0]
            raise ValueError(
                f'Each row of solid fractions + porosity must sum to 1. '
                f'Problematic rows: {problematic.tolist()}'
            )
        
        # Normalize each row
        normalized_fractions = f_solid_components / (1 - porosity)[:, np.newaxis]
        
        # Verify each row sums to 1
        row_sums_norm = np.sum(normalized_fractions, axis=1)
        if not np.allclose(row_sums_norm, 1.0):
            raise ValueError(
                f'Normalized fractions do not sum to 1 for all rows. '
                f'Got: {row_sums_norm}'
            )
        
        # Create DataFrame
        result_df = pd.DataFrame(
            normalized_fractions,
            columns=components
        )
        result_df['Porosity'] = porosity
        
    else:
        raise ValueError(
            f'f_solid_components must be 1D or 2D array. '
            f'Got shape: {f_solid_components.shape}'
        )
    
    return result_df
