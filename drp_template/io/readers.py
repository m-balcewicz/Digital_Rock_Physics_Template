"""
Data Readers
============

Functions for importing digital rock models from various file formats.

This module provides readers for:
- Raw binary files (import_model)
- MATLAB .mat files (loadmat)
- TIFF image sequences (import_tiff_sequence)
- Single TIFF files (import_tif_model)

All readers automatically:
- Create parameter JSON files with metadata
- Validate binary data
- Reorient volumes to standard (nx, ny, nz) format

Functions
---------
- import_model: Import raw binary files with memmap
- loadmat: Load MATLAB .mat files
- import_tiff_sequence: Import sequences of TIFF images as 3D volumes
- import_tif_model: Import single 3D TIFF files
"""

import os
import numpy as np
import h5py
import tifffile
import re

from .utils import get_dim_order, reorient_volume, _update_params_common, update_params_after_import, resolve_params_filename
from drp_template.default_params import update_parameters_file, check_output_folder, print_style

__all__ = [
    'import_model',
    'loadmat',
    'import_tiff_sequence',
    'import_tif_model',
]


def import_model(file_path, dtype, voxel_size=None, dimensions=None, mode='r', order='C', paramsfile: str = 'parameters.json'):
    """
    Import multidimensional model file using np.memmap.

    Parameters
    ----------
    file_path : str
        Path to the raw file.
    dtype : str
        Data type for the raw file (e.g., 'uint8', 'uint16', 'float32', etc.).
    voxel_size : float, optional
        The size of the voxel in micrometers.
    dimensions : dict, optional
        Dictionary containing dimensions for x (nx), y (ny), and z (nz).
        Example: {'nx': 400, 'ny': 400, 'nz': 400}
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
    TypeError
        If dimensions is not a dictionary.

    Examples
    --------
    ```python
    import drp_template.io as io
    
    # Import a raw binary file
    data = io.import_model(
        'sample.raw',
        dtype='uint8',
        voxel_size=5.0,
        dimensions={'nx': 400, 'ny': 400, 'nz': 400}
    )
    ```
    """
    from drp_template.tools import check_binary
    
    # Warn user if voxel_size is not provided
    if voxel_size is None:
        print_style(
            "WARNING: voxel_size not provided!\n"
            "Physical scale information will be missing from metadata.\n"
            "Recommended: io.import_model(..., voxel_size=<value_in_meters>)",
            style='box'
        )
    
    # Resolve parameters file name allowing user override and avoiding collisions
    params_filename = resolve_params_filename(paramsfile)
    file_format = file_path.split('.')[-1]

    if order == 'C':
        endianess = 'small'
    elif order == 'F':
        endianess = 'big'
    else:
        raise ValueError("Unsupported order. Please use 'C' for row-major or 'F' for column-major order.")

    if dimensions is None:
        raise ValueError("At least two dimensions (nx, ny, nz) must be provided.")
    
    # Validate that dimensions is a dictionary
    if not isinstance(dimensions, dict):
        raise TypeError(f"dimensions must be a dictionary, got {type(dimensions).__name__}: {dimensions}")

    nx = dimensions.get('nx', None)
    ny = dimensions.get('ny', None)
    nz = dimensions.get('nz', None)
    if sum(dim is not None for dim in [nx, ny, nz]) < 2:
        raise ValueError("At least two dimensions (nx, ny, nz) must be provided.")

    # Use the order of keys in dimensions for shape
    # Ensure all dimension values are integers (convert from string if needed)
    dim_keys = list(dimensions.keys())
    try:
        dim_shape = tuple(int(dimensions[k]) for k in dim_keys)
    except (ValueError, TypeError) as e:
        raise ValueError(
            f"All dimension values must be numeric. Got dimensions={dimensions}. Error: {e}"
        )
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

    # Inform the user where the parameters file was written/updated
    try:
        print_style(f"parameters saved: {os.path.join(check_output_folder(), params_filename)}")
    except Exception:
        # Non-fatal: printing path is best-effort
        pass
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
        If None, returns a dictionary of all variables.
    voxel_size : float, optional
        The size of the voxel in micrometers.

    Returns
    -------
    model : np.ndarray or dict
        Loaded data. If var_key is specified, returns the array.
        Otherwise, returns a dictionary of all variables.

    Examples
    --------
    ```python
    import drp_template.io as io
    
    # Load specific variable from .mat file
    data = io.loadmat('sample.mat', var_key='segmented_image')
    
    # Load all variables
    all_data = io.loadmat('sample.mat')
    ```
    """
    from drp_template.tools import check_binary
    # Derive params filename from source .mat file and resolve uniqueness
    base_name = os.path.splitext(os.path.basename(file_path))[0] + '.json'
    params_filename = resolve_params_filename(base_name)
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
        Data type for the output volume (e.g., 'uint8', 'uint16').
    dimensions : dict, optional
        Dictionary with keys 'nx', 'ny', 'nz' for dimension sizes.
        If not provided, dimensions are inferred from the images.
    voxel_size : float, optional
        The size of the voxel in micrometers.

    Returns
    -------
    volume : np.ndarray
        The loaded 3D volume in (nx, ny, nz) format.

    Raises
    ------
    FileNotFoundError
        If no TIFF files are found in the directory.
    ValueError
        If TIFF files are not sequentially numbered or have shape mismatches.

    Examples
    --------
    ```python
    import drp_template.io as io
    
    # Import TIFF sequence
    volume = io.import_tiff_sequence(
        'path/to/tiff_folder',
        dtype='uint8',
        voxel_size=2.5
    )
    ```
    
    Notes
    -----
    - Files must be sequentially numbered (e.g., slice_0000.tif, slice_0001.tif, ...)
    - All slices must have the same dimensions
    - Creates a parameters JSON file with metadata
    """
    from drp_template.tools import check_binary

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
    # Derive params filename from first TIFF and resolve uniqueness
    # Requirement: drop trailing index in stem (e.g., 'slice_0000.tif' -> 'slice.json')
    first_stem = os.path.splitext(os.path.basename(first_tiff_path))[0]
    # Remove optional underscore/hyphen followed by digits at the end of the stem
    stem_wo_index = re.sub(r'([_\-]?\d+)$', '', first_stem)
    base_name = stem_wo_index + '.json'
    params_filename = resolve_params_filename(base_name)

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
            print_style(f"[ERROR] Index {i} is out of bounds for volume with nz={nz}")
            break
        volume[i, :, :] = img

    dim_order = get_dim_order(dimensions) if dimensions else ('nz', 'ny', 'nx')
    print_style(f"[DEBUG] Current dimension order: {dim_order}")
    volume = reorient_volume(volume, dim_order)

    update_params_after_import(params_filename, first_tiff_path, volume, voxel_size, dtype)
    # Override file size with total sequence size (more representative than a single slice)
    if total_size_bytes is not None:
        update_parameters_file(paramsfile=params_filename, file_size_bytes=int(total_size_bytes))
        update_parameters_file(paramsfile=params_filename, file_size_mb=round(total_size_bytes / (1024 * 1024), 2))
    # Always run check_binary as standard import step
    volume = check_binary(model=volume, filename=first_tiff_path)
    print_style("[DEBUG] Finished loading TIFF sequence and updated parameter file.")
    return volume


def import_tif_model(filename):
    """
    Load a 3D TIFF file as a numpy array.
    
    Parameters
    ----------
    filename : str
        Path to the 3D TIFF file.
    
    Returns
    -------
    model : np.ndarray
        The loaded 3D array.
    
    Examples
    --------
    ```python
    import drp_template.io as io
    
    # Import a single 3D TIFF file
    data = io.import_tif_model('sample_3d.tif')
    ```
    """
    import skimage.io
    model = skimage.io.imread(filename)
    return model
