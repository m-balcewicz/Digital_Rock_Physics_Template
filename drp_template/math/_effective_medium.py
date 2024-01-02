import numpy as np

__all__ = [
    'density_solid_mix',
    'density_fluid_mix',
    'Brie_law',
    'get_normalized_f_solid',
    'bound',
    'bound2',

    
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
    
    
def get_normalized_f_solid(porosity, f_solid_components, type='solid'):
    """
    Calculate normalized solid fractions based on the given porosity.

    Parameters:
    - porosity (float or numpy.ndarray): The porosity of the rock (0 <= porosity <= 1).
    - f_solid_components (numpy.ndarray): Initial fractions of solid phases.
    - type (str): Type of check to perform. Use 'solid' for sum check, 'solid-porosity' for sum + porosity check.

    Returns:
    - normalized_solid_fractions (numpy.ndarray): Normalized solid fractions.
    """

    if type == 'solid':
        # Check if f_solid_components is a 1D array
        if f_solid_components.ndim == 1:
            # Check if the sum of initial fractions is approximately equal to 1
            if not np.allclose(np.sum(f_solid_components), 1):
                raise ValueError('The sum of initial fractions must be approximately equal to 1.')
        elif f_solid_components.ndim == 2:
            # Check if the sum of each column is approximately equal to 1
            column_sums = np.sum(f_solid_components, axis=0)
            if not np.allclose(column_sums, 1):
                problematic_columns = np.where(~np.isclose(column_sums, 1))[0]
                raise ValueError(f'The sum of each column must be approximately equal to 1. Problematic columns: {problematic_columns}.')
        else:
            raise ValueError('Invalid shape for f_solid_components. It should be a 1D or 2D array.')

    elif type == 'solid-porosity':
        # Check if f_solid_components is a 1D array
        if f_solid_components.ndim == 1:
            # Check if the sum of initial fractions + porosity is approximately equal to 1
            if not np.allclose(np.sum(f_solid_components) + porosity, 1):
                raise ValueError('The sum of initial fractions + porosity must be approximately equal to 1.')
        elif f_solid_components.ndim == 2:
            # Check if the sum of each column + porosity is approximately equal to 1
            if len(porosity) != f_solid_components.shape[1]:
                raise ValueError('Length of porosity must match the number of columns in f_solid_components.')
            
            column_sums = np.sum(f_solid_components, axis=0) + porosity
            if not np.allclose(column_sums, 1):
                problematic_columns = np.where(~np.isclose(column_sums, 1))[0]
                raise ValueError(f'The sum of each column + porosity must be approximately equal to 1. Problematic columns: {problematic_columns}.')
        else:
            raise ValueError('Invalid shape for f_solid_components. It should be a 1D or 2D array.')

    else:
        raise ValueError('Invalid value for check_type. Use "solid" or "solid-porosity".')

    # Calculate the normalized solid fractions
    normalized_solid_fractions = (1 - porosity) * f_solid_components / np.sum(f_solid_components, axis=0)

    return normalized_solid_fractions



def bound(f_volume, k_component, u_component, type='voigt-reuss'):
    """
    Calculate elastic bounds (upper and lower) of an aggregate.

    Parameters:
    - type (str): Type of bound. Use 'voigt-reuss' for Voigt-Reuss bounds or 'hashin-shtrikman' for Hashin-Shtrikman bounds.
    - f_solid (numpy.ndarray): Volume fractions (<=1) of the components.
    - k_solid (numpy.ndarray): Bulk moduli of the solid components.
    - u_solid (numpy.ndarray): Shear moduli of the solid components.

    Returns:
    - k_voigt (float): Voigt bound for bulk modulus.
    - k_reuss (float): Reuss bound for bulk modulus.
    - u_voigt (float): Voigt bound for shear modulus.
    - u_reuss (float): Reuss bound for shear modulus.
    - k_avg (float): Arithmetic average of upper and lower bounds for bulk modulus.
    - u_avg (float): Arithmetic average of upper and lower bounds for shear modulus.
        (equals the Hill average for Hashin-Shtrikman bounds)

    Raises:
    - ValueError: If the lengths of fractions, k, and u are not the same, or if the sum of fractions is not approximately 1.

    Note:
    1. Voigt-Reuss bounds are the simplest.
    2. Hashin-Shtrikman bounds are the narrowest possible.
    3. Assumption: Rock is isotropic.

    Source:
    - Berryman, J.G., 1993, Mixture theories for rock properties.
    - Mavko, G., 1993, Rock physics formulas.
    - https://github.com/StanfordRockPhysics/The-Rock-Physics-Handbook-3rd-Edition
    """   
    # mode=strict
    if len(f_volume) != len(k_component) != len(u_component):
        raise ValueError('Input fractions, k, and u must have the same length')
    
    if not np.isclose(np.sum(f_volume), 1):
        raise ValueError('Fractions must sum up to 1')
    
    c = 4 / 3
    
    if type == 'voigt-reuss':  # Voigt-Reuss bounds
        k_voigt = np.sum(f_volume * k_component)  # Voigt (upper) bound
        k_reuss = 1 / np.sum(f_volume / k_component)  # Reuss (lower) bound

        u_voigt = np.sum(f_volume * u_component)  # Voigt (upper) bound
        u_reuss = 1 / np.sum(f_volume / u_component)  # Reuss (lower) bound

        k_hill = (k_voigt + k_reuss) / 2  # Hill average
        u_hill = (u_voigt + u_reuss) / 2
        
        return k_voigt, k_reuss, u_voigt, u_reuss, k_hill, u_hill

    elif type == 'hashin-shtrikman':  # Hashin-Shtrikman bounds
        kmx, kmn = np.max(k_component), np.min(k_component)
        umx, umn = np.max(u_component), np.min(u_component)

        k_hs_upper = 1 / np.sum(f_volume / (k_component + c * umx)) - c * umx  # HS upper bound
        k_hs_lower = 1 / np.sum(f_volume / (k_component + c * umn)) - c * umn  # HS lower bound

        etamx = umx * (9 * kmx + 8 * umx) / (kmx + 2 * umx) / 6
        etamn = umn * (9 * kmn + 8 * umn) / (kmn + 2 * umn) / 6

        u_hs_upper = 1 / np.sum(f_volume / (u_component + etamx)) - etamx  # HS upper bound
        u_hs_lower = 1 / np.sum(f_volume / (u_component + etamn)) - etamn  # HS lower bound

        k_avg = (k_hs_upper + k_hs_lower) / 2  # Simple arithmetic average
        u_avg = (u_hs_upper + u_hs_lower) / 2
        
        return k_hs_upper, k_hs_lower, u_hs_upper, u_hs_lower, k_avg, u_avg
    
    elif type == 'fluid': # Bulk modulus bounds after Voigt, Reuss, and Brie

        k_voigt = np.sum(f_volume * k_component)  # Voigt (upper) bound
        k_reuss = 1 / np.sum(f_volume / k_component)  # Reuss (lower) bound

        return k_voigt, k_reuss

    else:
        raise ValueError('Invalid value for type. Use "voigt-reuss", "hashin-shtrikman", or "fluid".')

    

def bound2(type, f_solid, k_solid, u_solid):
    """
    Calculate elastic bounds (upper and lower) of an aggregate.

    Parameters:
    - type (str): Type of bound. Use 'voigt-reuss' for Voigt-Reuss bounds or 'hashin-shtrikman' for Hashin-Shtrikman bounds.
    - f_solid (numpy.ndarray): Volume fractions (<=1) of the solid components.
    - k_solid (numpy.ndarray): Bulk moduli of the solid components.
    - u_solid (numpy.ndarray): Shear moduli of the solid components.

    Returns:
    - k_voigt (numpy.ndarray): Voigt bound for bulk modulus.
    - k_reuss (numpy.ndarray): Reuss bound for bulk modulus.
    - u_voigt (numpy.ndarray): Voigt bound for shear modulus.
    - u_reuss (numpy.ndarray): Reuss bound for shear modulus.
    - k_avg (numpy.ndarray): Arithmetic average of upper and lower bounds for bulk modulus.
    - u_avg (numpy.ndarray): Arithmetic average of upper and lower bounds for shear modulus.
        (equals the Hill average for Hashin-Shtrikman bounds)

    Raises:
    - ValueError: If the lengths of fractions, k, and u are not the same.

    Note:
    1. Voigt-Reuss bounds are the simplest.
    2. Hashin-Shtrikman bounds are the narrowest possible.
    3. Assumption: Rock is isotropic.

    Source:
    - Berryman, J.G., 1993, Mixture theories for rock properties.
    - Mavko, G., 1993, Rock physics formulas.
    - https://github.com/StanfordRockPhysics/The-Rock-Physics-Handbook-3rd-Edition
    """
    # Ensure f_solid is a 2D array
    if f_solid.ndim == 1:
        f_solid = f_solid[:, np.newaxis]

    if len(f_solid) != len(k_solid) != len(u_solid):
        raise ValueError('Input fractions, k, and u must have the same length')

    c = 4 / 3
    
    k_voigt_list, k_reuss_list, u_voigt_list, u_reuss_list, k_avg_list, u_avg_list = [], [], [], [], [], []

    for i in range(len(f_solid)):
        if type == 'voigt-reuss':  # Voigt-Reuss bounds
            # Voigt (upper) bound for bulk modulus
            k_voigt = np.sum(f_solid[i] * k_solid)
            # Reuss (lower) bound for bulk modulus
            k_reuss = 1 / np.sum(f_solid[i] / k_solid)
    
            # Voigt (upper) bound for shear modulus
            u_voigt = np.sum(f_solid[i] * u_solid)
            # Reuss (lower) bound for shear modulus
            u_reuss = 1 / np.sum(f_solid[i] / u_solid)
    
            # Hill average for bulk and shear moduli
            k_avg = (k_voigt + k_reuss) / 2
            u_avg = (u_voigt + u_reuss) / 2
        
        elif type == 'hashin-shtrikman':  # Hashin-Shtrikman bounds
            kmx, kmn = np.max(k_solid[i]), np.min(k_solid[i])
            umx, umn = np.max(u_solid[i]), np.min(u_solid[i])
    
            # HS upper bound for bulk modulus
            k_hs_upper = 1 / np.sum(f_solid[i] / (k_solid[i] + c * umx)) - c * umx
            # HS lower bound for bulk modulus
            k_hs_lower = 1 / np.sum(f_solid[i] / (k_solid[i] + c * umn)) - c * umn
    
            etamx = umx * (9 * kmx + 8 * umx) / (kmx + 2 * umx) / 6
            etamn = umn * (9 * kmn + 8 * umn) / (kmn + 2 * umn) / 6
    
            # HS upper bound for shear modulus
            u_hs_upper = 1 / np.sum(f_solid[i] / (u_solid[i] + etamx)) - etamx
            # HS lower bound for shear modulus
            u_hs_lower = 1 / np.sum(f_solid[i] / (u_solid[i] + etamn)) - etamn
    
            # Simple arithmetic average for bulk and shear moduli
            k_avg = (k_hs_upper + k_hs_lower) / 2
            u_avg = (u_hs_upper + u_hs_lower) / 2
        
        k_voigt_list.append(k_voigt)
        k_reuss_list.append(k_reuss)
        u_voigt_list.append(u_voigt)
        u_reuss_list.append(u_reuss)
        k_avg_list.append(k_avg)
        u_avg_list.append(u_avg)

    return np.array(k_voigt_list), np.array(k_reuss_list), np.array(u_voigt_list), np.array(u_reuss_list), np.array(k_avg_list), np.array(u_avg_list)
