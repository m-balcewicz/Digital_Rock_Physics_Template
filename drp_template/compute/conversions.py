__all__ = [
    'GPa2Pa',
    'Pa2GPa',
    'm2mm',
    'mm2m',
    'm2um',
    'um2m'
]

def GPa2Pa(*args):
    """
    Convert values from gigapascals (GPa) to pascals (Pa).

    Parameters:
    - *args: One or more numbers/arrays in GPa.

    Returns:
    - list: Values converted to Pa, preserving input shapes, returned in order.
    """
    return [arg * 1e9 for arg in args]


def Pa2GPa(*args):
    """
    Convert values from pascals (Pa) to gigapascals (GPa).

    Parameters:
    - *args: One or more numbers/arrays in Pa.

    Returns:
    - list: Values converted to GPa, preserving input shapes, returned in order.
    """
    return [arg * 1e-9 for arg in args]


def m2mm(*args):
    """
    Convert length values from meters (m) to millimeters (mm).

    Parameters:
    - *args: One or more numbers/arrays in meters.

    Returns:
    - list: Values converted to millimeters.
    """
    return [arg * 1e3 for arg in args]


def mm2m(*args):
    """
    Convert length values from millimeters (mm) to meters (m).

    Parameters:
    - *args: One or more numbers/arrays in millimeters.

    Returns:
    - list: Values converted to meters.
    """
    return [arg * 1e-3 for arg in args]


def m2um(*args):
    """
    Convert length values from meters (m) to micrometers (µm).

    Parameters:
    - *args: One or more numbers/arrays in meters.

    Returns:
    - list: Values converted to micrometers.
    """
    return [arg * 1e6 for arg in args]


def um2m(*args):
    """
    Convert length values from micrometers (µm) to meters (m).

    Parameters:
    - *args: One or more numbers/arrays in micrometers.

    Returns:
    - list: Values converted to meters.
    """
    return [arg * 1e-6 for arg in args]


