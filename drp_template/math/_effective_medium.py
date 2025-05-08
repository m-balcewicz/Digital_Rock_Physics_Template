import numpy as np
import pandas as pd

__all__ = [
    'density_solid_mix',
    'density_fluid_mix',
    'Brie_law',
    'get_normalized_f_solid',
    'elastic_bounds',
    
]

def density_solid_mix(f_solid, rho_solid):
    """_summary_
    f_volume = f_porosity + f_solid
    Args:
        f_solid (_type_): fraction of the solid
        density_components (_type_): density of the solid
    """
    if len(f_solid) != len(rho_solid):
        raise ValueError('Input volume fractions and densities must have the same length')
    
    if not np.isclose(np.sum(f_solid), 1):
        raise ValueError('Volume fractions must sum up to 1')
    
    rho_solid_mix = np.sum(f_solid * rho_solid)
    
    return rho_solid_mix


def density_fluid_mix(s_fluid, rho_fluid):
    """_summary_

    Args:
        s_fluid (_type_): saturation of the fluid
        rho_fluid (_type_): density of the fluid
    """
    if len(s_fluid) != len(rho_fluid):
        raise ValueError('Input volume fractions and densities must have the same length')
    
    if not np.isclose(np.sum(s_fluid), 1):
        raise ValueError('Volume fractions must sum up to 1')
    
    rho_fluid_mix = np.sum(s_fluid * rho_fluid)
    
    return rho_fluid_mix

def Brie_law(s_water, s_oil, s_gas, k_water,k_oil, k_gas, e=3):
    """
    Similar to the solid phase case, the average of Voigt and Reuss bounds (i.e. patchy and
    homogeneous mixtures) can also be adopted to describe intermediate cases. Alternatively,
    Brie et al. (1995) propose a fluid mixing law for patchy mixtures of water and hydrocarbon,
    namely Brie’s equation, where e is an empirical constant, equal to 3 in the original experiments.
    """
    
    # Handle None values for constants
    k_water = k_water or 0
    k_oil = k_oil or 0
    k_gas = k_gas or 0

    # Check for division by zero condition
    if k_oil == 0:
        k_Brie = (1 / (s_water / k_water) - k_gas) * (1 - s_gas)**e + k_gas
    else:
        k_Brie = (1 / (s_water / k_water + s_oil / k_oil) - k_gas) * (1 - s_gas)**e + k_gas
    
    return k_Brie
    
    
def get_normalized_f_solid(porosity, f_solid_components, components=None):
    """
    Calculate normalized solid fractions based on the given porosity. The function utilizes NumPy and pandas for efficient array operations and data manipulation.

    Parameters:
    - porosity (float or numpy.ndarray): The porosity of the rock (0 <= porosity <= 1).
    - f_solid_components (numpy.ndarray): Initial fractions of solid phases.
    - phases (list of str): List of phase names corresponding to the solid components.

    Returns:
    - result_df (pandas.DataFrame): A DataFrame containing the normalized solid fractions, corresponding phase names, and the "Porosity" column.

    Raises:
    - ValueError: If the input values do not meet the specified conditions.

    Example:
    ```python
    porosity = 0.2
    f_solid_components = np.array([0.3, 0.4, 0.3])
    phases = ['Quartz', 'Feldspar', 'Dolomite']

    result_df = get_normalized_f_solid(porosity, f_solid_components, phases=phases)

    ```
    """
    
    # Check if f_solid_components is a 1D array
    if f_solid_components.ndim == 1:
        if components is None or len(components) != f_solid_components.shape[0]:
            raise ValueError('Invalid number of phases. Provide a list of phase names with the correct length.')
        # Check if the sum of each column + porosity is approximately equal to 1
        print(f"porosity: {porosity}")
        print(f"components:\n{f_solid_components}")
        column_sums = np.sum(f_solid_components, axis=0) + porosity
        print(f"column_sums: {column_sums}")
        if not np.allclose(column_sums, 1):
            raise ValueError(f'The sum of each column + porosity must be approximately equal to 1. Problematic columns.')
        
        # Calculate the normalized solid fractions
        normalized_solid_fractions = f_solid_components.T / (1 - porosity)
        
        print(f"normalized_solid_fractions:\n{normalized_solid_fractions}")
        
        # Check if the sum of the normalzed solid fractions is equal to 1
        column_sums = np.sum(normalized_solid_fractions, axis=0)
        if not np.allclose(column_sums, 1):
            raise ValueError('The sum of the normalized solid fractions is not equal to 1')

        
    elif f_solid_components.ndim == 2:
        if components is None or len(components) != f_solid_components.shape[1]:
            raise ValueError('Invalid number of phases. Provide a list of phase names with the correct length.')
        # Check if the length of porosity array is equal to f_solid_components
        if len(porosity) != f_solid_components.shape[0]:
            raise ValueError('Length of porosity must match the number of columns in f_solid_components.')
        # Check if the sum of each column + porosity is approximately equal to 1
        column_sums = np.sum(f_solid_components, axis=1) + porosity
        if not np.allclose(column_sums, 1):
            problematic_columns = np.where(~np.isclose(column_sums, 1))[0]
            raise ValueError(f'The sum of each column + porosity must be approximately equal to 1. Problematic columns: {problematic_columns}.')
        
        # Calculate the normalized solid fractions
        normalized_solid_fractions = f_solid_components.T / (1 - porosity)
        
        # Check if the sum of the normalized solid fractions is equal to 1
        column_sums = np.sum(normalized_solid_fractions, axis=0)
        if not np.allclose(column_sums, 1):
            raise ValueError('The sum of the normalized solid fractions is not equal to 1')

    else:
        raise ValueError('Invalid shape for f_solid_components. It should be a 1D or 2D array.')
    

    # transpose the shape of the array
    normalized_solid_fractions = normalized_solid_fractions.T 
    # Create column names based on the length and strings of components
    column_names = [component for component in components]
    df_normalized_solid_fractions = pd.DataFrame(normalized_solid_fractions, columns=column_names)
    # Add "Porosity" column
    df_normalized_solid_fractions['Porosity'] = porosity

    return df_normalized_solid_fractions


def elastic_bounds(fractions, k_values, u_values, bound_type='voigt-reuss'):
    """
    Calculate elastic bounds (upper and lower) of an aggregate.

    Parameters:
    - fractions (numpy.ndarray): Volume fractions of components. Can be 1D array for a single dataset
      or 2D array for multiple datasets. Each row/array must sum to 1.
    - k_values (numpy.ndarray): Bulk moduli of the components.
    - u_values (numpy.ndarray): Shear moduli of the components (not used for 'fluid' bound_type).
    - bound_type (str): Type of bound calculation:
        - 'voigt-reuss': Simplest bounds
        - 'hashin-shtrikman': Narrowest possible bounds
        - 'fluid': Bulk modulus bounds for fluids only (no shear modulus)

    Returns:
    - For 'voigt-reuss' and 'hashin-shtrikman':
        If fractions is 1D: Tuple of (k_upper, k_lower, u_upper, u_lower, k_avg, u_avg)
        If fractions is 2D: Tuple of arrays (k_upper_array, k_lower_array, u_upper_array, u_lower_array, k_avg_array, u_avg_array)
    
    - For 'fluid':
        If fractions is 1D: Tuple of (k_voigt, k_reuss)
        If fractions is 2D: Tuple of arrays (k_voigt_array, k_reuss_array)

    Raises:
    - ValueError: If inputs have invalid dimensions, if fractions don't sum to 1,
      or if an invalid bound_type is specified.

    Note:
    1. Voigt-Reuss bounds are the simplest.
    2. Hashin-Shtrikman bounds are the narrowest possible.
    3. Assumption: Rock is isotropic.

    Source:
    - Berryman, J.G., 1993, Mixture theories for rock properties.
    - Mavko, G., 1993, Rock physics formulas.
    - https://github.com/StanfordRockPhysics/The-Rock-Physics-Handbook-3rd-Edition
    """
    with np.errstate(divide='ignore', invalid='ignore'):
        # Ensure fractions is a numpy array
        fractions = np.asarray(fractions)
        k_values = np.asarray(k_values)
        u_values = np.asarray(u_values)
        
        # Determine if input is 1D or 2D
        multi_dataset = (fractions.ndim > 1)
        
        # For a single dataset, reshape into 2D for consistent processing
        if not multi_dataset:
            fractions = fractions.reshape(1, -1)
            if not (len(fractions[0]) == len(k_values) == len(u_values)):
                raise ValueError('Input fractions, k_values, and u_values must have the same length')
            
            # Check if fractions sum to 1
            if not np.allclose(np.sum(fractions, axis=1), 1):
                raise ValueError('Fractions must sum up to 1')
        else:
            # For 2D fractions, ensure dimensions match components
            if bound_type != 'fluid' and not (fractions.shape[1] == len(k_values) == len(u_values)):
                raise ValueError('Number of components in fractions must match length of k_values and u_values')
            
            # Check if all rows of fractions sum to 1
            if not np.allclose(np.sum(fractions, axis=1), 1):
                raise ValueError('Each row in fractions must sum up to 1')
        
        c = 4 / 3  # Helper constant for Hashin-Shtrikman bounds
        
        # Initialize result arrays
        num_datasets = fractions.shape[0]
        k_upper = np.zeros(num_datasets)
        k_lower = np.zeros(num_datasets)
        
        if bound_type != 'fluid':
            u_upper = np.zeros(num_datasets)
            u_lower = np.zeros(num_datasets)
            u_avg = np.zeros(num_datasets)
        
        k_avg = np.zeros(num_datasets)
        
        # Process each dataset
        for i in range(num_datasets):
            if bound_type == 'voigt-reuss':
                # Voigt (upper) bound for bulk modulus
                k_upper[i] = np.sum(fractions[i] * k_values)
                # Reuss (lower) bound for bulk modulus
                k_lower[i] = 1 / np.sum(fractions[i] / k_values)
                
                # Voigt (upper) bound for shear modulus
                u_upper[i] = np.sum(fractions[i] * u_values)
                # Reuss (lower) bound for shear modulus
                u_lower[i] = 1 / np.sum(fractions[i] / u_values)
                
                # Hill average for bulk and shear moduli
                k_avg[i] = (k_upper[i] + k_lower[i]) / 2
                u_avg[i] = (u_upper[i] + u_lower[i]) / 2
                
            elif bound_type == 'hashin-shtrikman':
                kmx, kmn = np.max(k_values), np.min(k_values)
                umx, umn = np.max(u_values), np.min(u_values)
                
                # HS upper bound for bulk modulus
                k_upper[i] = 1 / np.sum(fractions[i] / (k_values + c * umx)) - c * umx
                # HS lower bound for bulk modulus
                k_lower[i] = 1 / np.sum(fractions[i] / (k_values + c * umn)) - c * umn
                
                etamx = umx * (9 * kmx + 8 * umx) / (kmx + 2 * umx) / 6
                etamn = umn * (9 * kmn + 8 * umn) / (kmn + 2 * umn) / 6
                
                # HS upper bound for shear modulus
                u_upper[i] = 1 / np.sum(fractions[i] / (u_values + etamx)) - etamx
                # HS lower bound for shear modulus
                u_lower[i] = 1 / np.sum(fractions[i] / (u_values + etamn)) - etamn
                
                # Simple arithmetic average for bulk and shear moduli
                k_avg[i] = (k_upper[i] + k_lower[i]) / 2
                u_avg[i] = (u_upper[i] + u_lower[i]) / 2
                
            elif bound_type == 'fluid':
                # For fluids, there is no shear modulus
                # Voigt (upper) bound for bulk modulus
                k_upper[i] = np.sum(fractions[i] * k_values)
                # Reuss (lower) bound for bulk modulus
                k_lower[i] = 1 / np.sum(fractions[i] / k_values)
                
            else:
                raise ValueError('Invalid bound_type. Use "voigt-reuss", "hashin-shtrikman", or "fluid".')
        
        # Convert back to single values if input was 1D
        if not multi_dataset:
            k_upper = k_upper[0]
            k_lower = k_lower[0]
            k_avg = k_avg[0]
            
            if bound_type != 'fluid':
                u_upper = u_upper[0]
                u_lower = u_lower[0]
                u_avg = u_avg[0]
        
        # Return appropriate results based on the bound type
        if bound_type == 'fluid':
            return k_upper, k_lower
        else:
            return k_upper, k_lower, u_upper, u_lower, k_avg, u_avg
