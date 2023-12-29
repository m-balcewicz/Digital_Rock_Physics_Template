import numpy as np

__all__ = [
    'bound',
]

def bound(type, fractions, k, u):
    """
    Calculate elastic bounds (upper and lower) of an aggregate.

    Parameters:
    - type (str): Type of bound. Use 'voigt-reuss' for Voigt-Reuss bounds or 'hashin-shtrikman' for Hashin-Shtrikman bounds.
    - fractions (numpy.ndarray): Volume fractions (<=1) of the components.
    - k (numpy.ndarray): Bulk moduli of the components.
    - u (numpy.ndarray): Shear moduli of the components.

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
    if len(fractions) != len(k) != len(u):
        raise ValueError('Input fractions, k, and u must have the same length')
    
    if not np.isclose(np.sum(fractions), 1):
        raise ValueError('Fractions must sum up to 1')
    
    c = 4 / 3
    
    if type == 'voigt-reuss':  # Voigt-Reuss bounds
        k_voigt = np.sum(fractions * k)  # Voigt (upper) bound
        k_reuss = 1 / np.sum(fractions / k)  # Reuss (lower) bound

        u_voigt = np.sum(fractions * u)  # Voigt (upper) bound
        u_reuss = 1 / np.sum(fractions / u)  # Reuss (upper) bound

        k_avg = (k_voigt + k_reuss) / 2  # Hill average
        u_avg = (u_voigt + u_reuss) / 2
        
        return k_voigt, k_reuss, u_voigt, u_reuss, k_avg, u_avg

    elif type == 'hashin-shtrikman':  # Hashin-Shtrikman bounds
        kmx, kmn = np.max(k), np.min(k)
        umx, umn = np.max(u), np.min(u)

        k_hs_upper = 1 / np.sum(fractions / (k + c * umx)) - c * umx  # HS upper bound
        k_hs_lower = 1 / np.sum(fractions / (k + c * umn)) - c * umn  # HS lower bound

        etamx = umx * (9 * kmx + 8 * umx) / (kmx + 2 * umx) / 6
        etamn = umn * (9 * kmn + 8 * umn) / (kmn + 2 * umn) / 6

        u_hs_upper = 1 / np.sum(fractions / (u + etamx)) - etamx  # HS upper bound
        u_hs_lower = 1 / np.sum(fractions / (u + etamn)) - etamn  # HS lower bound

        k_avg = (k_hs_upper + k_hs_lower) / 2  # Simple arithmetic average
        u_avg = (u_hs_upper + u_hs_lower) / 2
        
        return k_hs_upper, k_hs_lower, u_hs_upper, u_hs_lower, k_avg, u_avg

    else:
        raise ValueError('Invalid value for type. Use "voigt-reuss" or "hashin-shtrikman".')

    

