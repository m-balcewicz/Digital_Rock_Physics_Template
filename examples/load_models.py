import os
import numpy as np
import drp_template.import_export as ie


def raw_cube(**kwargs):
    """
    Loads examples data from a raw file.

    Args:
        **kwargs: Optional arguments for file_path and dimension.

    Returns:
        A numpy array containing the examples data and the dimension of the data.
    """

    # Get the absolute path of the directory containing this script
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Construct the path to the examples directory relative to the script directory
    examples_dir = os.path.join(script_dir, "..", "examples")

    # Construct the path to data.raw relative to the examples directory
    data_path = os.path.join(examples_dir, "data_raw.raw")

    dimension = 100

    try:
        cube_raw = ie.import_test(path=data_path, dimension=dimension)
    except Exception as e:
        raise Exception(f'Error loading examples data: {e}')

    # # Read the data_normal from the file
    # with open(data_path, 'rb') as f:
    #     cube_raw = np.fromfile(f, dtype=np.uint8)
    #
    # # Reshape the data_normal to the original shape
    # cube_raw = cube_raw.reshape((dimension, dimension, dimension))

    return cube_raw

def binary_cube(**kwargs):
    """
    Loads examples data from a raw file.

    Args:
        **kwargs: Optional arguments for file_path and dimension.

    Returns:
        A numpy array containing the examples data and the dimension of the data.
    """

    # Get the absolute path of the directory containing this script
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Construct the path to the examples directory relative to the script directory
    examples_dir = os.path.join(script_dir, "..", "examples")

    # Construct the path to data.raw relative to the examples directory
    data_path = os.path.join(examples_dir, "data_binary.raw")

    dimension = 100

    try:
        cube_binary = ie.import_test(path=data_path, dimension=dimension)
    except Exception as e:
        raise Exception(f'Error loading examples data: {e}')

    return cube_binary

def binary_fracture(**kwargs):
    """
    Loads examples data from a raw file.

    Args:
        **kwargs: Optional arguments for file_path and dimension.

    Returns:
        A numpy array containing the examples data and the dimension of the data.
    """

    # Get the absolute path of the directory containing this script
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Construct the path to the examples directory relative to the script directory
    examples_dir = os.path.join(script_dir, "..", "examples")

    # Construct the path to data.raw relative to the examples directory
    data_path = os.path.join(examples_dir, "fracture_binary.raw")

    dimension = 500

    try:
        fracture_binary = ie.import_test(path=data_path, dimension=dimension)
    except Exception as e:
        raise Exception(f'Error loading examples data: {e}')

    return fracture_binary
