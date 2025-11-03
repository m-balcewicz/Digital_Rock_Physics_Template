import os
import numpy as np
import h5py
import tifffile
import re

from drp_template.default_params import update_parameters_file, check_output_folder

__all__ = [
    'get_dim_order',
    'reorient_volume',
    '_update_params_common',
    'import_model',
    'loadmat',
    'import_tiff_sequence',
    'import_tif_model',
    'export_model',
    'export_header'
]

def get_dim_order(dimensions):
    """
    Returns the order of dimension keys as a tuple, e.g. ('nz', 'ny', 'nx').
    """
    return tuple(dimensions.keys())

def reorient_volume(volume, dim_order):
    """
    Reorient a 3D numpy array to (nx, ny, nz) order.

    Parameters
    ----------
    volume : np.ndarray
        The 3D volume array.
    dim_order : tuple
        The current order of dimensions, e.g., ('nz', 'ny', 'nx').

    Returns
    -------
    np.ndarray
        The reoriented volume.
    """
    if dim_order != ('nx', 'ny', 'nz'):
        print("Reshaping data to the desired order (nx, ny, nz)...")
        if dim_order == ('nx', 'nz', 'ny'):
            return np.moveaxis(volume, (0, 1, 2), (0, 2, 1))
        elif dim_order == ('nz', 'ny', 'nx'):
            return np.moveaxis(volume, (0, 1, 2), (2, 1, 0))
        elif dim_order == ('nz', 'nx', 'ny'):
            return np.moveaxis(volume, (0, 1, 2), (2, 0, 1))
        elif dim_order == ('ny', 'nx', 'nz'):
            return np.moveaxis(volume, (0, 1, 2), (1, 0, 2))
        elif dim_order == ('ny', 'nz', 'nx'):
            return np.moveaxis(volume, (0, 1, 2), (1, 2, 0))
        else:
            raise ValueError(f"Unsupported shape {dim_order}. Unable to determine correct axis order.")
    return volume

def _update_params_common(params_filename, file_path, arr, voxel_size, dtype, endian, file_format):
    """
    Helper to update the parameters JSON file with common fields.
    """
    update_parameters_file(paramsfile=params_filename, file_path=file_path)
    update_parameters_file(paramsfile=params_filename, dim=arr.ndim)
    print(f"Dimensions: {arr.ndim}")
    update_parameters_file(paramsfile=params_filename, nx=arr.shape[0], ny=arr.shape[1], nz=arr.shape[2])
    print(f"nx: {arr.shape[0]}")
    print(f"ny: {arr.shape[1]}")
    print(f"nz: {arr.shape[2]}")
    update_parameters_file(paramsfile=params_filename, voxel_size=voxel_size)
    update_parameters_file(paramsfile=params_filename, endian=endian)
    update_parameters_file(paramsfile=params_filename, dtype=dtype)
    update_parameters_file(paramsfile=params_filename, file_format=file_format)

    # Add on-disk file size (single-file imports)
    # For multi-file imports (e.g., TIFF sequences), this will be overridden later.
    try:
        if isinstance(file_path, str) and os.path.isfile(file_path):
            size_bytes = os.path.getsize(file_path)
            update_parameters_file(paramsfile=params_filename, file_size_bytes=int(size_bytes))
            update_parameters_file(paramsfile=params_filename, file_size_mb=round(size_bytes / (1024 * 1024), 2))
    except Exception:
        # Non-fatal: skip file size if unavailable
        pass

def update_params_after_import(params_filename, file_path, volume, voxel_size, dtype):
    """
    Update the parameters JSON file for a TIFF sequence import.
    """
    _update_params_common(
        params_filename, file_path, volume, voxel_size, dtype,
        endian='small', file_format='tiff'
    )

def import_model(file_path, dtype, voxel_size=None, dimensions=None, mode='r', order='C'):
    """
    Import multidimensional model file using np.memmap.

    Parameters
    ----------
    file_path : str
        Path to the raw file.
    dtype : str
        Data type for the raw file (e.g., 'uint8', 'uint16', 'float32', etc.).
    voxel_size : float, optional
        The size of the voxel.
    dimensions : dict, optional
        Dictionary containing dimensions for x (nx), y (ny), and z (nz).
    mode : str, optional
        Mode in which the file is opened. Default is 'r' (read-only).
    order : str, optional
        The order of the data in the file ('C' for row-major, 'F' for column-major). Default is 'C'.

    Returns
    -------
    model : np.memmap
        Numpy memmap array representing the raw file data.

    Raises
    ------
    ValueError
        If dimensions are not provided or are incomplete.
    """
    from drp_template.tools import check_binary, mk_paramsfile

    params_filename = mk_paramsfile(file_path)
    file_format = file_path.split('.')[-1]

    if order == 'C':
        endianess = 'small'
    elif order == 'F':
        endianess = 'big'
    else:
        raise ValueError("Unsupported order. Please use 'C' for row-major or 'F' for column-major order.")

    if dimensions is None:
        raise ValueError("At least two dimensions (nx, ny, nz) must be provided.")

    nx = dimensions.get('nx', None)
    ny = dimensions.get('ny', None)
    nz = dimensions.get('nz', None)
    if sum(dim is not None for dim in [nx, ny, nz]) < 2:
        raise ValueError("At least two dimensions (nx, ny, nz) must be provided.")

    # Use the order of keys in dimensions for shape
    # Ensure all dimension values are integers (convert from string if needed)
    dim_keys = list(dimensions.keys())
    dim_shape = tuple(int(dimensions[k]) for k in dim_keys)
    model = np.memmap(file_path, dtype=dtype, mode=mode, shape=dim_shape, order=order)

    # Reorient if needed
    model = reorient_volume(model, tuple(dim_keys))

    # Update the parameters.json file
    _update_params_common(
        params_filename, file_path, model, voxel_size, dtype,
        endian=endianess, file_format=file_format
    )

    # Always run check_binary as standard import step
    model = check_binary(model=model, filename=file_path)
    return model

def loadmat(file_path, var_key=None, voxel_size=None):
    """
    Load a .mat file and return the data as a numpy array.

    Parameters
    ----------
    file_path : str
        Path to the .mat file.
    var_key : str, optional
        The key of the variable in the .mat file to load.
    voxel_size : float, optional
        The size of the voxel.

    Returns
    -------
    model : np.ndarray
        Loaded data.
    """
    from drp_template.tools import mk_paramsfile, check_binary

    params_filename = mk_paramsfile(file_path)
    with h5py.File(file_path, 'r') as file:
        if var_key is not None:
            model = np.array(file[var_key], dtype='uint8', order='C')
        else:
            keys = list(file.keys())
            model = {key: np.array(file[key], dtype='uint8', order='C') for key in keys}

    # Always transpose for 3D arrays
    if isinstance(model, np.ndarray) and model.ndim == 3:
        model = np.transpose(model, (2, 1, 0))

    file_format = file_path.split('.')[-1]
    _update_params_common(
        params_filename, file_path, model, voxel_size,
        dtype='Matlab files are uint8', endian='Matlab files are big-endian', file_format=file_format
    )

    model = check_binary(model=model, filename=file_path)
    return model

def import_tiff_sequence(directory, dtype, dimensions=None, voxel_size=None):
    """
    Import a sequence of TIFF files as a 3D volume.

    Parameters
    ----------
    directory : str
        Directory containing TIFF files.
    dtype : str
        Data type for the output volume.
    dimensions : dict, optional
        Dictionary with keys 'nx', 'ny', 'nz' for dimension sizes.
    voxel_size : float, optional
        The size of the voxel.

    Returns
    -------
    volume : np.ndarray
        The loaded 3D volume.
    """
    from drp_template.tools import mk_paramsfile, check_binary

    files = [f for f in os.listdir(directory) if f.lower().endswith(('.tif', '.tiff'))]
    if not files:
        raise FileNotFoundError(f"No TIFF files found in {directory}")

    def extract_index(fname):
        match = re.search(r'(\d+)(?=\.tif{1,2}$)', fname, re.IGNORECASE)
        return int(match.group(1)) if match else -1

    files_sorted = sorted(files, key=extract_index)
    indices = [extract_index(f) for f in files_sorted]

    if indices != list(range(indices[0], indices[0] + len(indices))):
        raise ValueError("TIFF files are not sequentially numbered.")

    first_tiff_path = os.path.join(directory, files_sorted[0])
    # Compute total on-disk size for all TIFF slices
    try:
        total_size_bytes = sum(os.path.getsize(os.path.join(directory, f)) for f in files_sorted)
    except Exception:
        total_size_bytes = None
    params_filename = mk_paramsfile(first_tiff_path)

    first_img = tifffile.imread(first_tiff_path)
    ny, nx = first_img.shape
    nz = len(files_sorted)
    if dimensions is not None:
        ny = dimensions.get('ny', ny)
        nx = dimensions.get('nx', nx)
        nz = dimensions.get('nz', nz)

    volume = np.zeros((nz, ny, nx), dtype=dtype)
    for i, fname in enumerate(files_sorted):
        img = tifffile.imread(os.path.join(directory, fname)).astype(dtype)
        if img.shape != (ny, nx):
            raise ValueError(f"Slice shape mismatch at {fname}: expected {(ny, nx)}, got {img.shape}")
        if i >= nz:
            print(f"[ERROR] Index {i} is out of bounds for volume with nz={nz}")
            break
        volume[i, :, :] = img

    dim_order = get_dim_order(dimensions) if dimensions else ('nz', 'ny', 'nx')
    print(f"[DEBUG] Current dimension order: {dim_order}")
    volume = reorient_volume(volume, dim_order)

    update_params_after_import(params_filename, first_tiff_path, volume, voxel_size, dtype)
    # Override file size with total sequence size (more representative than a single slice)
    if total_size_bytes is not None:
        update_parameters_file(paramsfile=params_filename, file_size_bytes=int(total_size_bytes))
        update_parameters_file(paramsfile=params_filename, file_size_mb=round(total_size_bytes / (1024 * 1024), 2))
    # Always run check_binary as standard import step
    volume = check_binary(model=volume, filename=first_tiff_path)
    print("[DEBUG] Finished loading TIFF sequence and updated parameter file.")
    return volume

def import_tif_model(filename):
    """
    Load a 3D TIFF file as a numpy array.
    """
    import skimage.io
    model = skimage.io.imread(filename)
    return model

def export_model(filename, data, voxel_size, dtype='uint8', order='F', filetype='.raw'):
    """
    Write model data to a binary file and create a corresponding parameters JSON file.

    Parameters
    ----------
    filename : str
        Output file name (without extension).
    data : np.ndarray
        Data to write. Expected shape is (nx, ny, nz) for 3D or (nx, ny, nz, dim) for 4D.
    voxel_size : float
        The size of the voxel in micrometers. This is a required parameter.
    dtype : str, optional
        Data type for output.
    order : str, optional
        Memory layout: 'F' (Fortran) or 'C' (C).
    filetype : str, optional
        File extension.

    Returns
    -------
    None
    
    Raises
    ------
    ValueError
        If voxel_size is None or not provided.
    
    Notes
    -----
    This function automatically creates a validated parameters JSON file with:
    - Schema version and provenance (generator, created_at, modified_at)
    - File path, format, dtype, endianness
    - Dimensions (nx, ny, nz for 3D or nx, ny, nz, dim for 4D)
    - Voxel size (required)
    - File size in bytes and MB
    
    Input data should follow the package standard: (nx, ny, nz) for 3D arrays.
    The raw file is written with the same axis order.
    """
    from drp_template.tools import check_output_folder
    
    # Validate required parameter
    if voxel_size is None:
        raise ValueError("voxel_size is required and cannot be None. Please provide the voxel size in micrometers.")

    output_path = check_output_folder()
    file_path = os.path.join(output_path, filename + filetype)

    if data.ndim == 4:
        # Expect (nx, ny, nz, dim) - package standard
        nx, ny, nz, dim = data.shape
        data_tmp = data.astype(dtype)
    elif data.ndim == 3:
        # Expect (nx, ny, nz) - package standard
        nx, ny, nz = data.shape
        data_tmp = data.astype(dtype)
    else:
        raise ValueError("Data should be a 3D or 4D array")

    model_reshaped = data_tmp.reshape(data_tmp.size, order=order)
    model_reshaped.T.tofile(file_path)
    print(f"data saved: {file_path}")
    
    # Create corresponding parameters JSON file
    params_filename = filename + '.json'
    
    # Determine endianness from order
    endian = 'small' if order == 'C' else 'big'
    
    # Write essential metadata
    update_parameters_file(paramsfile=params_filename, file_path=file_path)
    update_parameters_file(paramsfile=params_filename, file_format=filetype.lstrip('.'))
    update_parameters_file(paramsfile=params_filename, dtype=dtype)
    update_parameters_file(paramsfile=params_filename, endian=endian)
    
    # Write dimensions (using package standard: nx, ny, nz)
    if data.ndim == 4:
        update_parameters_file(paramsfile=params_filename, dim=4)
        update_parameters_file(paramsfile=params_filename, nx=nx, ny=ny, nz=nz)
        # Store 4th dimension info if needed
    elif data.ndim == 3:
        update_parameters_file(paramsfile=params_filename, dim=3)
        update_parameters_file(paramsfile=params_filename, nx=nx, ny=ny, nz=nz)
    
    # Write voxel_size (required)
    update_parameters_file(paramsfile=params_filename, voxel_size=float(voxel_size))
    
    # Add file size metadata
    try:
        size_bytes = os.path.getsize(file_path)
        update_parameters_file(paramsfile=params_filename, file_size_bytes=int(size_bytes))
        update_parameters_file(paramsfile=params_filename, file_size_mb=round(size_bytes / (1024 * 1024), 2))
    except Exception:
        pass
    
    print(f"parameters saved: {os.path.join(output_path, params_filename)}")

def export_header(filename, data):
    """
    Write a SEPlib header file for the given data.

    Parameters
    ----------
    filename : str
        Output file name (without extension).
    data : np.ndarray
        Data array.

    Returns
    -------
    None
    """
    if data.ndim == 4:
        n1, n2, n3, n4 = [format(dim, '06') for dim in data.shape]
    elif data.ndim == 3:
        n1, n2, n3 = [format(dim, '06') for dim in data.shape]
        n4 = '1'
    else:
        raise ValueError("Data should be a 3D or 4D array")

    if n3 == '000001' and data.ndim == 4:
        n3 = n4
    n4 = '1'

    header = "SEPlib Headerfile: quick & dirty: please always check !!!\n"
    header += "so far: only n1,n2,n3,n4 will be part of output\n\n"
    if filename == 'moduli':
        header += f"sets next: in=\"moduli\"\n\n"
    else:
        header += f"sets next: in=\"./{filename}moduli\"\n\n"
    header += f"n1={n1}\nn2={n2}\nn3={n3}\nn4={n4}\n"

    filename = filename + 'header'
    with open(filename, 'w') as f:
        f.write(header)
    print(f"header saved: {filename}")