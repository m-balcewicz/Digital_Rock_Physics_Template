import numpy as np
import os

import drp_template.input_output as io
from drp_template.default_params import print_style
import drp_template.default_params as dp

__all__ = [
    'check_binary',
    'list_dir_info',
    'mk_paramsfile',
    'get_model_dimensions',
    'reshape_model',
    'create_subvolume',
    'find_slice_with_all_values'
]

def check_binary(model, filename):
    unique_phases = np.unique(model)

    if min(unique_phases) == 0:
        print_style(f'{filename}:\n'
                    f'Nice data; the minimum value in your data is 0'
                    )
    elif min(unique_phases) == -1:
        # print("+++ automatic adjustment is needed")
        print_style(f'{filename}:\n'
                    f'Ups, the minimum value in your data is -1. Automatic adjustments are needed.'
                    )
        # print(f"min value: {min(unique_phases)}")
        model = model + 1
    elif min(unique_phases) == 1:
        # print("+++ automatic adjustment is needed")
        print_style(f'{filename}: \n'
                    f'Ups, the minimum value in your data is 1. Automatic adjustments are needed.'
                    )
        # print(f"min value: {min(unique_phases)}")
        model = model - 1

    return model


def list_dir_info(directory, extension=None):
    """
    List all files with a specific extension in a directory,
    or list all subfolders if no extension is provided.

    Args:
        directory (str): The directory to search for files and subfolders.
        extension (str, optional): The file extension to filter the files.
                                   Default is None.

    Returns:
        list: A list of file names with the specified extension in the directory,
              or a list of subfolder names in the directory.

    """
    directory_listing = []
    for entry in os.scandir(directory):
        if entry.is_dir():
            directory_listing.append(entry.name)

    if extension is not None:
        directory_listing = [file for file in directory_listing
                             if any(file.endswith(extension) for file in os.listdir(os.path.join(directory, file)))]

    return directory_listing


def mk_paramsfile(file_path):
    filename, extension = os.path.splitext(os.path.basename(file_path))
    params_filename = filename+'.json'
    print(f"Parameters filename: {params_filename}")
    
    return params_filename


def get_model_dimensions(dimensions_dict):
    """_summary_

    Args:
        dimensions_dict (_type_): _description_

    Raises:
        ValueError: _description_
        ValueError: _description_

    Returns:
        _type_: _description_
        
    Example:
        dimensions_dict = {'nz': 100, 'ny': 200, 'nx': 300}
    """
    # Ensure dimensions is a dictionary
    if dimensions_dict is None:
        raise ValueError("At least two dimensions (nx, ny, nz) must be provided.")

    # Unpack dimensions in the determined order
    nx = dimensions_dict.get('nx', None)
    ny = dimensions_dict.get('ny', None)
    nz = dimensions_dict.get('nz', None)

    # Check if at least two dimensions are provided
    if sum(dim is not None for dim in [nx, ny, nz]) < 2:
        raise ValueError("At least two dimensions (nx, ny, nz) must be provided.")

    # Create separate iterators for n1, n2, and n3
    iterator = iter(dimensions_dict.items())
    n1 = next(iterator)
    n2 = next(iterator)
    n3 = next(iterator)
    
    return n1, n2, n3

def reshape_model(model, n1, n2, n3):
    # Check if the dimensions order is not in the desired order (nx, ny, nz)
    if (n1[0], n2[0], n3[0]) != ('nx', 'ny', 'nz'):
        print("Reshaping data to the desired order (nx, ny, nz)...")

        # Check the specific reshaping conditions
        if (n1[0], n2[0], n3[0]) == ('nx', 'nz', 'ny'):
            model_reshaped = np.moveaxis(model, (0, 1, 2), (0, 2, 1))
        elif (n1[0], n2[0], n3[0]) == ('nz', 'ny', 'nx'):
            model_reshaped = np.moveaxis(model, (0, 1, 2), (2, 1, 0))
        elif (n1[0], n2[0], n3[0]) == ('nz', 'nx', 'ny'):
            model_reshaped = np.moveaxis(model, (0, 1, 2), (2, 0, 1))
        elif (n1[0], n2[0], n3[0]) == ('ny', 'nx', 'nz'):
            model_reshaped = np.moveaxis(model, (0, 1, 2), (1, 0, 2))
        elif (n1[0], n2[0], n3[0]) == ('ny', 'nz', 'nx'):
            model_reshaped = np.moveaxis(model, (0, 1, 2), (1, 2, 0))
    elif (n1[0], n2[0], n3[0]) == ('nx', 'ny', 'nz'):
        # No need to move axes, dimensions are already correct
        print("Model dimensions are already in the desired order (nx, ny, nz).")
        model_reshaped = model
        pass
    else:
        raise ValueError("Unsupported shape. Unable to determine correct axis order.")
    
    return model_reshaped


def create_subvolume(data, set_subvolume, name_subvolume, directory=None, dtype='uint8', order='C'):
    """
    Creates a subvolume from the given data and saves it as a binary file.

    Args:
    data (numpy.ndarray): The original data from which the subvolume will be created.
    set_subvolume (int): The desired size of the subvolume.
    name_subvolume (str): The name of the subvolume.
    directory (str, optional): The directory where the subvolume will be saved. If not provided, the 'output' directory is used.
    dtype (str, optional): The data type of the elements in the array. Defaults to 'uint8'.
    order (str, optional): The memory layout of the data.
        - 'F' for Fortran ordering (column-major),
        - 'C' for C ordering (row-major).
        Defaults to 'C'.

    Returns:
    numpy.ndarray: The created subvolume.

    Notes:
    - The 'dtype' parameter specifies the data type of the elements in the array.
    - The 'order' parameter determines the memory layout of the data, with 'F' for Fortran ordering and 'C' for C ordering.
    - The subvolume is created by cutting the original data from the center. The size of the cut is determined by the 'set_subvolume' parameter. 
      For example, if the original data has a shape of (100, 100, 100) and 'set_subvolume' is 50, the subvolume will have a shape of (50, 50, 50) 
      and will be centered in the original data.

    Examples:
    To create a subvolume of size 50 with C ordering:
    ```python
    subvolume = create_subvolume(my_data, 50, 'my_subvolume', dtype='uint8', order='C')
    `
    """
    x, y, z = data.shape

    # define cutting
    cut_x = (x - set_subvolume) // 2
    cut_y = (y - set_subvolume) // 2
    cut_z = (z - set_subvolume) // 2

    # create subvolume
    data_subvolume = data[cut_x:x - cut_x, cut_y:y - cut_y, cut_z:z - cut_z]

    varname = f"{name_subvolume}_{set_subvolume}cube"

    # set the directory to 'output' if not provided
    if directory is None:
        directory = dp.check_output_folder()
        
    file_path = os.path.join(directory, varname)

    # Save new data_subvolume as a 'uint8' raw file
    io.export_model(filename=file_path, data=data_subvolume, dtype=dtype, order=order)

    return data_subvolume

def find_slice_with_all_values(data):
    # Get all unique values in the 3D array
    unique_values = np.unique(data)

    # Helper function to check if a 2D slice contains all unique values
    def check_slice(slice):
        slice_unique_values = np.unique(slice)
        return np.all(np.isin(unique_values, slice_unique_values))

    # Initialize the result dictionary
    slice_with_all_values = {"xy": None, "yz": None, "xz": None}

    # Check the xy slices
    for i in range(data.shape[2]):
        if check_slice(data[:, :, i]):
            slice_with_all_values["xy"] = i
            break

    # Check the yz slices
    for i in range(data.shape[0]):
        if check_slice(data[i, :, :]):
            slice_with_all_values["yz"] = i
            break

    # Check the xz slices
    for i in range(data.shape[1]):
        if check_slice(data[:, i, :]):
            slice_with_all_values["xz"] = i
            break

    return slice_with_all_values