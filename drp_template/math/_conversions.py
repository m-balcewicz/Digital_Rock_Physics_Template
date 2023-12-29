__all__ = [
    'GPa2Pa',
    'GP2GPa'
]

def GPa2Pa(*args):
    """
    Convert multiple arrays from Pa to GPa.

    Parameters:
    - *args: Variable number of arrays containing values in Pa.

    Returns:
    - gpa_arrays: List of arrays containing values converted to GPa.
    """
    return [arg * 1e+9 for arg in args]


def Pa2GPa(*args):
    """
    Convert multiple arrays from Pa to GPa.

    Parameters:
    - *args: Variable number of arrays containing values in Pa.

    Returns:
    - gpa_arrays: List of arrays containing values converted to GPa.
    """
    return [arg * 1e-9 for arg in args]


