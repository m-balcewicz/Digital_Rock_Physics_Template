import os
import numpy as np
import h5py
# from tifffile import tifffile

from drp_template.default_params import update_parameters_file, check_output_folder
from drp_template.tools import check_binary, mk_paramsfile, get_model_dimensions, reshape_model
# from drp_template.tools.dirify import mk_dir
# from drp_template.tools.logify import mk_log
# import skimage
# from PIL import Image

__all__ = [
    'import_model',
    'loadmat',
    'import_tiff_sequence',
    'import_tif_model',
    'export_model',
    'export_header'
]


def import_model(file_path, dtype, voxel_size=None, dimensions=None, mode='r', order='C'):
    """
    Import multidimensional model file using np.memmap.

    This function is used to import a raw file into a numpy memmap array. It provides options to specify the data type and dimensions of the data, as well as the mode and order in which the file is read.

    Parameters:
    -----------
    file_path : str
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

    Raises:
    -------
    IOError:
        If the file cannot be read.

    Examples:
    ---------
    ```python
    file_path = 'path/to/your/raw_file.raw'
    dtype = 'uint16'
    dimensions = {'nz': 100, 'ny': 200, 'nx': 300}
    data, used_vars = import_model(file_path, dtype, dimensions=dimensions)
    ```
    """
    
    # filename, extension = os.path.splitext(os.path.basename(file_path))
    # params_filename = filename+'.json'
    # print(f"Parameters filename: {params_filename}")
    params_filename = mk_paramsfile(file_path)
    
    # Get the file format from the file extension of the input file: file_path
    file_format = file_path.split('.')[-1]   

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
    update_parameters_file(paramsfile=params_filename, file_path=file_path)
    update_parameters_file(paramsfile=params_filename,dim=model.ndim)
    print(f"Dimensions: {model.ndim}")
    update_parameters_file(paramsfile=params_filename, nx=model.shape[0], ny=model.shape[1], nz=model.shape[2])
    print(f"nx: {model.shape[0]}")
    print(f"ny: {model.shape[1]}")
    print(f"nz: {model.shape[2]}")
    update_parameters_file(paramsfile=params_filename, voxel_size=voxel_size)
    update_parameters_file(paramsfile=params_filename, dtype=dtype)
    update_parameters_file(paramsfile=params_filename, file_format=file_format)
    
    # Check wrong label numbering
    model = check_binary(model=model, filename=file_path)

    return model


def loadmat(file_path, var_key=None, voxel_size=None):
    """
    Load a .mat file and return the data as a numpy array.

    This function is used to load a .mat file (MATLAB file format) and return the data as a numpy array. It provides options to specify the key of the variable in the .mat file to load and the size of the voxel.

    Parameters:
    -----------
    file_path : str
        Path to the .mat file.
    var_key : str, optional
        The key of the variable in the .mat file to load. If not provided, all data from the file is loaded.
    voxel_size : int, optional
        The size of the voxel. If not provided, the default voxel size is used.

    Returns:
    --------
    model : np.array or dict of np.array
        If var_key is provided, a numpy array of the corresponding data from the file. If var_key is not provided, a dictionary of numpy arrays of all the data from the file.

    Raises:
    -------
    IOError:
        If the file cannot be read.

    Examples:
    ---------
    ```python
    file_path = 'path/to/your/file.mat'
    var_key = 'your_variable_key'
    voxel_size = 10
    data = loadmat(file_path, var_key=var_key, voxel_size=voxel_size)
    """
    
    # Create a new parameters file
    params_filename = mk_paramsfile(file_path)
      
    with h5py.File(file_path, 'r') as file:
        if var_key is not None:
            model = np.array(file[var_key], dtype='uint8', order='C')
        else:
            keys = list(file.keys())
            model = {key: np.array(file[key], dtype='uint8', order='C') for key in keys}
    
    # Transpose the dimensions of the model
    model = np.transpose(model, (2, 1, 0))
    
    # Get the dimensions of the model
    nx = model.shape[0]
    ny = model.shape[1]
    nz = model.shape[2]
    # Get the file format from the file extension of the input file: file_path
    file_format = file_path.split('.')[-1]   
   
    # Update the parameters.json file
    update_parameters_file(paramsfile=params_filename, file_path=file_path)
    update_parameters_file(paramsfile=params_filename,dim=model.ndim)
    print(f"Dimensions: {model.ndim}")
    update_parameters_file(paramsfile=params_filename, nx=model.shape[0], ny=model.shape[1], nz=model.shape[2])
    print(f"nx: {model.shape[0]}")
    print(f"ny: {model.shape[1]}")
    print(f"nz: {model.shape[2]}")
    update_parameters_file(paramsfile=params_filename, voxel_size=voxel_size)
    update_parameters_file(paramsfile=params_filename, file_format=file_format)
    
    # Check wrong label numbering
    model = check_binary(model=model, filename=file_path)
    
    return model

def import_tiff_sequence(directory, filename, dtype, dimensions=None):
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
    # Ensure dimensions is a dictionary
    if dimensions is None:
        raise ValueError("dimensions must be a dictionary")
    else:
        n1, n2, n3 = get_model_dimensions(dimensions)
    
    
    file_path = directory+filename
    params_filename = mk_paramsfile(file_path)

    file_listing = skimage.io.imread_collection(f'{directory}/*.tif*')
    first_image = file_listing[0]
    rows, cols = first_image.shape
    slices = len(file_listing)
    # model must be in the structure of (rows, cols, slices)
    model = np.zeros((rows, cols, slices), dtype=dtype)
    # import the slices into the model
    for m in range(slices):
        model[:, :, m] = file_listing[m]
        if dtype == 'uint8':
            model = model.astype(np.uint8)
        elif dtype == 'uint16':
            model = model.astype(np.uint16)
        elif dtype == 'float32':
            model = model.astype(np.float32)
        else:
            raise ValueError(f"Unsupported data type: {dtype}. Please use 'uint8', 'uint16', or 'float32'.")
        

    # Check wrong label numbering
    model = check_binary(model, filename=filename)

    model = reshape_model(model, n1, n2, n3)
    
    update_parameters_file(paramsfile=params_filename,dim=model.ndim)
    update_parameters_file(paramsfile=params_filename,dtype=dtype)
    update_parameters_file(paramsfile=params_filename, nx=model.shape[0], ny=model.shape[1], nz=model.shape[2])
    

    return model


def import_tif_model(filename):
    # Load the 3D TIFF file
    model = skimage.io.imread(filename)

    return model

def export_model(filename, data, dtype='>f4', order='F', filetype='.raw'):
    """
    Writes moduli data to a binary file in big-endian or little-endian format with Fortran or C ordering.

    Args:
        filename (str): The path to the directory where the binary file will be created.
        data (numpy.ndarray): The moduli data to be written.
        dtype (str, optional): The data type of the elements in the array. Defaults to '>f4'.
        mode (str, optional): The file mode used for opening the binary file.
            - 'w+': Open for reading and writing, create the file if it does not exist.
            - 'wb+': Open for reading and writing in binary mode, create the file if it does not exist.
        order (str, optional): The memory layout of the data.
            - 'F' for Fortran ordering (column-major),
            - 'C' for C ordering (row-major).
            Defaults to 'F'.

    Returns:
        None

    Notes:
        - The 'dtype' parameter specifies the byte order of the data. '>f4' stands for big-endian, and '<f4' stands for little-endian.
        - The 'mode' parameter determines the file opening mode. The 'b' flag in 'wb+' ensures binary mode.
        - The 'order' parameter determines the memory layout of the data, with 'F' for Fortran ordering and 'C' for C ordering.

    Examples:
        To write data in little-endian format with C ordering:
        ```python
        export_endian('output.bin', my_data, dtype='<f4', mode='wb+', order='C')
        ```
    """
    
    output_path = check_output_folder()
    
    file_path = os.path.join(output_path, filename + filetype)
    
    # Ensure that the array is dtype='>f4' or the specified dtype
    # Check the shape of the data
    if len(data.shape) == 4:
        nx, ny, nz, dim = np.shape(data)
        data_tmp = np.zeros((nz, nx, ny, dim), dtype=dtype)
        data_tmp[:, :, :, :] = data[:, :, :, :]
    elif len(data.shape) == 3:
        nx, ny, nz = np.shape(data)
        data_tmp = np.zeros((nz, nx, ny), dtype=dtype)
        data_tmp[:, :, :] = data[:, :, :]
    else:
        raise ValueError("Data should be a 3D or 4D array")
    
    data = data_tmp
    model_reshaped = data.reshape(data.size, order=order)
    model_reshaped.T.tofile(file_path)
    
    print(f"data saved: {file_path}")
    
def export_header(filename, data):
    # Extract the dimensions from the shape of the input data
    if len(data.shape) == 4:
        n1, n2, n3, n4 = [format(dim, '06') for dim in data.shape]
    elif len(data.shape) == 3:
            n1, n2, n3 = [format(dim, '06') for dim in data.shape]
    else:
        raise ValueError("Data should be a 3D or 4D array")
    
    # Add the conditional statement
    if n3 == '000001':
        n3 = n4
    n4 = '1'

    # Define the dimensions
    dim = [n1, n2, n3, n4]

    # Define the header
    header = "SEPlib Headerfile: quick & dirty: please always check !!!\n"
    header += "so far: only n1,n2,n3,n4 will be part of output\n\n"
    if filename == 'moduli':
        header += f"sets next: in=\"moduli\"\n\n"
    else:
        header += f"sets next: in=\"./{filename}moduli\"\n\n"
    header += f"n1={n1}\nn2={n2}\nn3={n3}\nn4={n4}\n"


    filename = filename+'header'
    # Write the header and dimensions to a new file
    with open(filename, 'w') as f:
        f.write(header)

    return print(f"header saved: {filename}")