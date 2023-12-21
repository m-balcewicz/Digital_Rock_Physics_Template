import os
import numpy as np
from tifffile import tifffile

from barbara.default_params import update_parameters_file
from barbara.tools import check_binary
from barbara.tools.dirify import mk_dir
from barbara.tools.logify import mk_log
import skimage
from PIL import Image

__all__ = [
    'import_model',
    'import_tiff_sequence',
    'import_tif_model',
    # 'export_tif_model'
]


def import_model(file_path, dtype, dimensions=None, mode='r', order='C'):
    """
    Import multidimensional model file using np.memmap.

    Parameters:
    -----------
    file_path  : str
        Path to the raw file.
    dtype : str
        Data type for the raw file (e.g., 'uint8', 'uint16', 'float32', etc.).
    dimensions : dict (optional)
        Dictionary containing dimensions for x (nx), y (ny), and z (nz).
    mode : str (optional)
        Mode in which the file is opened. Default is 'r' (read-only).
    order : str (optional)
        The order of the data in the file ('C' for row-major, 'F' for column-major). Default is 'C'.

    Returns:
    --------
    model : np.memmap
        Numpy memmap array representing the raw file data.
    used_variables : dict
        Dictionary containing the used variables.

    Examples:
    ---------
    ```python
    file_path = 'path/to/your/raw_file.raw'
    dtype = 'uint16'
    dimensions = {'nz': 100, 'ny': 200, 'nx': 300}
    data, used_vars = import_model(file_path, dtype, dimensions=dimensions)
    ```
    """
    
    filename, extension = os.path.splitext(os.path.basename(file_path))
    params_filename = filename+'.json'
    print(f"Parameters filename: {params_filename}")

    # Ensure dimensions is a dictionary
    if dimensions is None:
        raise ValueError("At least two dimensions (nx, ny, nz) must be provided.")

    # Unpack dimensions in the determined order
    nx = dimensions.get('nx', None)
    ny = dimensions.get('ny', None)
    nz = dimensions.get('nz', None)

    # Check if at least two dimensions are provided
    if sum(dim is not None for dim in [nx, ny, nz]) < 2:
        raise ValueError("At least two dimensions (nx, ny, nz) must be provided.")

    # Create separate iterators for n1, n2, and n3
    iterator = iter(dimensions.items())
    n1 = next(iterator)
    n2 = next(iterator)
    n3 = next(iterator)

    model = np.memmap(file_path, dtype=dtype, mode=mode, shape=(n1[1], n2[1], n3[1]), order=order)

    # Check if the dimensions order is not in the desired order (nx, ny, nz)
    if (n1[0], n2[0], n3[0]) != ('nx', 'ny', 'nz'):
        print("Reshaping data to the desired order (nx, ny, nz)...")

        # Check the specific reshaping conditions
        if (n1[0], n2[0], n3[0]) == ('nx', 'nz', 'ny'):
            model = np.moveaxis(model, (0, 1, 2), (0, 2, 1))
        elif (n1[0], n2[0], n3[0]) == ('nz', 'ny', 'nx'):
            model = np.moveaxis(model, (0, 1, 2), (2, 1, 0))
        elif (n1[0], n2[0], n3[0]) == ('nz', 'nx', 'ny'):
            model = np.moveaxis(model, (0, 1, 2), (2, 0, 1))
        elif (n1[0], n2[0], n3[0]) == ('ny', 'nx', 'nz'):
            model = np.moveaxis(model, (0, 1, 2), (1, 0, 2))
        elif (n1[0], n2[0], n3[0]) == ('ny', 'nz', 'nx'):
            model = np.moveaxis(model, (0, 1, 2), (1, 2, 0))
        elif (n1[0], n2[0], n3[0]) == ('nx', 'ny', 'nz'):
            # No need to move axes, dimensions are already correct
            pass
        else:
            raise ValueError("Unsupported shape. Unable to determine correct axis order.")

    # Update the parameters.json file
    update_parameters_file(paramsfile=params_filename,dim=model.ndim)
    print(f"Dimensions: {model.ndim}")
    update_parameters_file(paramsfile=params_filename, nx=model.shape[0], ny=model.shape[1], nz=model.shape[2])
    print(f"nx: {model.shape[0]}")
    print(f"ny: {model.shape[1]}")
    print(f"nz: {model.shape[2]}")
    update_parameters_file(paramsfile=params_filename, file_path=file_path)

    # Check wrong label numbering
    model = check_binary(model=model, filename=file_path)

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
