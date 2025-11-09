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

    Parameters
    ----------
    *args : float or array-like
        One or more numbers/arrays in GPa.

    Returns
    -------
    float, list, or array
        - Single arg: returns converted scalar/array
        - Multiple args: returns list of converted values

    Examples
    --------
    >>> GPa2Pa(1.0)
    1000000000.0
    >>> GPa2Pa(1.0, 2.0)
    [1000000000.0, 2000000000.0]
    """
    converted = [arg * 1e9 for arg in args]
    return converted[0] if len(converted) == 1 else converted


def Pa2GPa(*args):
    """
    Convert values from pascals (Pa) to gigapascals (GPa).

    Parameters
    ----------
    *args : float or array-like
        One or more numbers/arrays in Pa.

    Returns
    -------
    float, list, or array
        - Single arg: returns converted scalar/array
        - Multiple args: returns list of converted values

    Examples
    --------
    >>> Pa2GPa(1e9)
    1.0
    >>> Pa2GPa(1e9, 2e9)
    [1.0, 2.0]
    """
    converted = [arg * 1e-9 for arg in args]
    return converted[0] if len(converted) == 1 else converted


def m2mm(*args):
    """
    Convert length values from meters (m) to millimeters (mm).

    Parameters
    ----------
    *args : float or array-like
        One or more numbers/arrays in meters.

    Returns
    -------
    float, list, or array
        - Single arg: returns converted scalar/array
        - Multiple args: returns list of converted values

    Examples
    --------
    >>> m2mm(0.001)
    1.0
    >>> m2mm(0.001, 0.002)
    [1.0, 2.0]
    """
    converted = [arg * 1e3 for arg in args]
    return converted[0] if len(converted) == 1 else converted


def mm2m(*args):
    """
    Convert length values from millimeters (mm) to meters (m).

    Parameters
    ----------
    *args : float or array-like
        One or more numbers/arrays in millimeters.

    Returns
    -------
    float, list, or array
        - Single arg: returns converted scalar/array
        - Multiple args: returns list of converted values

    Examples
    --------
    >>> mm2m(1.0)
    0.001
    >>> mm2m(1.0, 2.0)
    [0.001, 0.002]
    """
    converted = [arg * 1e-3 for arg in args]
    return converted[0] if len(converted) == 1 else converted


def m2um(*args):
    """
    Convert length values from meters (m) to micrometers (µm).

    Parameters
    ----------
    *args : float or array-like
        One or more numbers/arrays in meters.

    Returns
    -------
    float, list, or array
        - Single arg: returns converted scalar/array
        - Multiple args: returns list of converted values

    Examples
    --------
    >>> m2um(1e-6)
    1.0
    >>> m2um(1e-6, 2e-6)
    [1.0, 2.0]
    """
    converted = [arg * 1e6 for arg in args]
    return converted[0] if len(converted) == 1 else converted


def um2m(*args):
    """
    Convert length values from micrometers (µm) to meters (m).

    Parameters
    ----------
    *args : float or array-like
        One or more numbers/arrays in micrometers.

    Returns
    -------
    float, list, or array
        - Single arg: returns converted scalar/array
        - Multiple args: returns list of converted values

    Examples
    --------
    >>> um2m(1.0)
    1e-06
    >>> um2m(1.0, 2.0)
    [1e-06, 2e-06]
    """
    converted = [arg * 1e-6 for arg in args]
    return converted[0] if len(converted) == 1 else converted


