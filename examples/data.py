import os
import numpy as np
import drp_template.import_export as ie


def load_100cube(**kwargs):
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
    data_path = os.path.join(examples_dir, "data.raw")

    dimension = 100

    try:
        cube100 = ie.import_test(data_path, dimension=dimension)
    except Exception as e:
        raise Exception(f'Error loading examples data: {e}')

    # # Read the data_normal from the file
    # with open(data_path, 'rb') as f:
    #     cube100 = np.fromfile(f, dtype=np.uint8)
    #
    # # Reshape the data_normal to the original shape
    # cube100 = cube100.reshape((dimension, dimension, dimension))

    return cube100
