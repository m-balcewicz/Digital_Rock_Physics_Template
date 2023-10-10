import os
import numpy as np
from tifffile import tifffile

from barbara.tools import check_binary
from barbara.tools.dirify import mk_dir
from barbara.tools.logify import mk_log
import skimage
from PIL import Image

__all__ = [
    'import_model',
    'import_tiff_sequence',
    'import_tif_model',
    'export_tif_model'
]


def import_model(filename, dtype, shape, mode='r', order='C'):
    """
    Import multidimensional model file using np.memmap.

    Parameters:
    -----------
    file_path  : str
        Path to the raw file.
    dtype : str
        Data type for the raw file (e.g., 'uint8', 'uint16', 'float32', etc.).
    shape : tuple
        Shape of the data is z, y, x.
    mode : str (optional)
        Mode in which the file is opened. Default is 'r' (read-only).
    order : str (optional)
        The order of the data in the file ('C' for row-major, 'F' for column-major). Default is 'C'.

    Returns:
    model : np.memmap
        Numpy memmap array representing the raw file data.

    Examples:
    >>> file_path = 'path/to/your/raw_file.raw'
    >>> dtype = 'uint16'
    >>> shape = (100, 200, 300)
    >>> data = import_model(file_path,dtype,shape)
    """

    # If shape is a single int, assume x_shape = y_shape = z_shape
    if isinstance(shape, int):
        shape = (shape, shape, shape)
    elif not isinstance(shape, tuple):
        raise ValueError("Shape must be either an integer or a tuple.")

    model = np.memmap(filename, dtype=dtype, mode=mode, shape=shape, order=order)

    # Check wrong label numbering
    model = check_binary(model=model, filename=filename)

    return model


def import_tiff_sequence(directory, filename, dtype):
    """
    Import raw data from a binary file.

    Parameters:
    -----------
    directory : str
        Path to directory with multiple 2D tiff files.
    filename : str
        . . .
    dtype : str
        Data type of the binary file. Valid values are 'raw' and 'binary'.

    """

    file_listing = skimage.io.imread_collection(f'{directory}/*.tif*')
    first_image = file_listing[0]
    rows, cols = first_image.shape
    slices = len(file_listing)
    model = np.zeros((slices, rows, cols))
    for m in range(slices):
        model[m, :, :] = file_listing[m]
    if dtype == 'uint8':
        model = model.astype(np.int8)
        mk_log(f'{filename} is uint8')
    elif dtype == 'uint16':
        mk_log(f'{filename} is uint16')
    else:
        raise IOError(f"Unable to read file: {filename}")

    # Check wrong label numbering
    model = check_binary(model, filename=filename)

    return model


def import_tif_model(filename):
    # Load the 3D TIFF file
    model = skimage.io.imread(filename)

    return model


# def export_tif_model(model, directory, filename):
#     # Create the directory if it doesn't exist
#     directory = mk_dir(directory)
#
#     # Combine the directory and file name variables using os.path.join
#     filepath = os.path.join(directory, filename + '.tif')  # add '.tif' to the file name
#
#     # Check if the model is a memmap
#     if isinstance(model, np.memmap):
#         # If it is a memmap, convert it to a regular NumPy array
#         model = np.array(model)
#
#     # Create a TiffWriter instance
#     with tifffile.TiffWriter(filepath, bigtiff=True) as tif:
#         # Iterate over each slice and write it to the TIFF file
#         for slice_idx in range(model.shape[0]):
#             tif.save(model[slice_idx], compress=6)  # Adjust compress level as needed
