import numpy as np
import os
import matplotlib.pyplot as plt

import drp_template.input_output as in_out
from drp_template.default_params import print_style, update_parameters_file
import drp_template.default_params as dp

__all__ = [
    'check_binary',
    'list_dir_info',
    'mk_paramsfile',
    'get_model_dimensions',
    'reshape_model',
    'create_subvolume',
    'create_binary_model',
    'create_binary_model_2d',
    'create_binary_model_3d',
    'find_slice_with_all_values',
    'label_binary',
    'infer_dimensions_from_filesize',
    'infer_dtype_from_filesize',
    'classify_data_type',
    'get_value_statistics',
    'get_model_properties'
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


def list_dir_info(directory, extension=None, search_subdirs=False, return_count=False):
    """
    List files or subdirectories in a directory with flexible filtering.

    Args:
        directory (str): The directory to search.
        extension (str, optional): File extension to filter (e.g., '.raw', '.txt').
                                   If None, lists subdirectories. Default is None.
        search_subdirs (bool, optional): If True and extension is provided,
                                         returns subdirectories containing files
                                         with that extension. If False, returns
                                         files directly in directory. Default is False.
        return_count (bool, optional): If True, returns a tuple of (list, count).
                                       If False, returns only the list. Default is False.

    Returns:
        list or tuple: 
            - If return_count=False: Sorted list of file names, file paths, or subdirectory names.
            - If return_count=True: Tuple of (sorted list, count).

    Examples:
        # List all subdirectories
        folders = list_dir_info('/path/to/dir')
        
        # List .raw files directly in directory
        files = list_dir_info('/path/to/dir', extension='.raw')
        
        # List .raw files and get count
        files, count = list_dir_info('/path/to/dir', extension='.raw', return_count=True)
        print(f"Found {count} raw files")
        
        # List subdirectories containing .raw files
        folders = list_dir_info('/path/to/dir', extension='.raw', search_subdirs=True)
    """
    import os
    
    if extension is None:
        # List all subdirectories
        directory_listing = []
        for entry in os.scandir(directory):
            if entry.is_dir():
                directory_listing.append(entry.name)
    
    elif search_subdirs:
        # List subdirectories that contain files with the extension
        directory_listing = []
        for entry in os.scandir(directory):
            if entry.is_dir():
                # Check if this subdirectory contains files with the extension
                subdir_path = os.path.join(directory, entry.name)
                has_extension = any(
                    f.endswith(extension) for f in os.listdir(subdir_path)
                    if os.path.isfile(os.path.join(subdir_path, f))
                )
                if has_extension:
                    directory_listing.append(entry.name)
    
    else:
        # List files with extension directly in directory
        directory_listing = []
        for entry in os.scandir(directory):
            if entry.is_file() and entry.name.endswith(extension):
                directory_listing.append(entry.name)
    
    sorted_listing = sorted(directory_listing)
    
    if return_count:
        return sorted_listing, len(sorted_listing)
    else:
        return sorted_listing


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


def create_subvolume(data, set_subvolume, name_subvolume, voxel_size, directory=None, dtype='uint8', order='C'):
    """
    Creates a subvolume from the given data and saves it as a binary file.

    Args:
    data (numpy.ndarray): The original data from which the subvolume will be created.
    set_subvolume (int): The desired size of the subvolume.
    name_subvolume (str): The name of the subvolume.
    voxel_size (float): The size of the voxel in micrometers. This is a required parameter.
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
    subvolume = create_subvolume(my_data, 50, 'my_subvolume', voxel_size=5.0, dtype='uint8', order='C')
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
    in_out.export_model(filename=file_path, data=data_subvolume, voxel_size=voxel_size, dtype=dtype, order=order)

    return data_subvolume

def create_binary_model(nx, ny, nz, 
                       num_inclusions=1,
                       inclusion_radius=10,
                       inclusion_aspect_ratio=1.0,
                       orientation='zx',
                       random_orientation=False,
                       background_value=1,
                       inclusion_value=0,
                       dtype='uint8',
                       seed=None,
                       positions=None,
                       periodic=False):
    """
    Create a binary model with ellipsoidal inclusions in a homogeneous background.
    
    This function generates a 3D volume with a specified number of ellipsoidal
    inclusions (pores, phase 0) placed within a homogeneous background (solid, phase 1).
    By default, this represents a rock matrix (1) with pore inclusions (0).
    
    NOTE: For explicit 2D or 3D models, consider using:
    - create_binary_model_2d() for 2D models (nx × ny × 1)
    - create_binary_model_3d() for 3D models (clearer intent)
    This function remains for backward compatibility and general use.
    
    Parameters
    ----------
    nx, ny, nz : int
        Grid dimensions along x, y, z axes.
        For 2D-like models, set nz=1 (though create_binary_model_2d is preferred).
    num_inclusions : int, optional (default=1)
        Number of ellipsoidal inclusions to create. Maximum 100.
    inclusion_radius : float, optional (default=10)
        Radius of the ellipsoid in the primary plane (in voxels).
    inclusion_aspect_ratio : float, optional (default=1.0)
        Aspect ratio for ellipsoid shape. 
        - 1.0 creates a sphere
        - <1.0 creates an oblate ellipsoid (flattened)
        - >1.0 creates a prolate ellipsoid (elongated)
    orientation : str, optional (default='zx')
        Primary plane for ellipsoid orientation:
        - 'xy': Ellipse in xy-plane
        - 'zx': Ellipse in zx-plane  
        - 'zy': Ellipse in zy-plane
        Ignored when random_orientation=True.
    random_orientation : bool, optional (default=False)
        If True, each inclusion gets full 3D random rotation.
        If False, all inclusions have the same orientation.
    background_value : int, optional (default=1)
        Value for background phase (rock matrix/solid).
    inclusion_value : int, optional (default=0)
        Value for inclusion phase (pore space).
    dtype : str or numpy.dtype, optional (default='uint8')
        Data type of the output model.
    seed : int, optional (default=None)
        Random seed for reproducible placement. If None, uses random positions.
        Ignored if positions is provided.
    positions : numpy.ndarray or list, optional (default=None)
        Explicit positions for inclusion centers. If provided, must be array-like 
        with shape (num_inclusions, 3) where each row is [x, y, z] coordinates.
        If None, inclusions are placed randomly.
        Example: positions = np.array([[50, 50, 50], [30, 30, 30]])
    periodic : bool, optional (default=False)
        If True, implements periodic boundary conditions. Inclusions near boundaries
        are wrapped to the opposite side, creating a seamless, tileable volume.
        Useful for representative volume elements (RVE) and computational homogenization.
        When enabled, inclusions that extend beyond domain boundaries are replicated
        at corresponding periodic positions (up to 27 locations in 3D: 1 original + 
        6 face-adjacent + 12 edge-adjacent + 8 corner-adjacent).
    
    Returns
    -------
    numpy.ndarray
        3D array with shape (nx, ny, nz) containing the binary model.
    
    Notes
    -----
    - Inclusions are placed randomly within the volume
    - Overlapping inclusions are allowed (union behavior)
    - Returned array uses package standard shape (nx, ny, nz)
    - For export with metadata, use export_model() separately
    - Default values represent digital rock physics convention: 
      solid matrix (1) with pore inclusions (0)
    - When random_orientation=True, uses true 3D rotation (Euler angles)
    
    Examples
    --------
    >>> import drp_template.tools as tools
    >>> import numpy as np
    >>> 
    >>> # Single spherical pore in rock matrix (random placement)
    >>> data = tools.create_binary_model(100, 100, 100, 
    ...                                  num_inclusions=1,
    ...                                  inclusion_radius=15,
    ...                                  seed=42)
    >>> # Result: background=1 (solid), inclusion=0 (pore)
    >>> 
    >>> # Single centered sphere (explicit position)
    >>> positions = np.array([[50, 50, 50]])  # Center of 100x100x100 volume
    >>> data = tools.create_binary_model(100, 100, 100,
    ...                                  num_inclusions=1,
    ...                                  inclusion_radius=20,
    ...                                  positions=positions)
    >>> 
    >>> # Multiple ellipsoidal pores with random orientations
    >>> data = tools.create_binary_model(200, 200, 200,
    ...                                  num_inclusions=10,
    ...                                  inclusion_radius=20,
    ...                                  inclusion_aspect_ratio=1.5,
    ...                                  orientation='xy',
    ...                                  random_orientation=True,
    ...                                  seed=42)
    >>> 
    >>> # Multiple inclusions at specific positions
    >>> positions = np.array([[50, 50, 50], [100, 100, 100], [150, 150, 150]])
    >>> data = tools.create_binary_model(200, 200, 200,
    ...                                  num_inclusions=3,
    ...                                  inclusion_radius=15,
    ...                                  positions=positions)
    >>> 
    >>> # Periodic boundary conditions for seamless tiling (RVE)
    >>> data = tools.create_binary_model(100, 100, 100,
    ...                                  num_inclusions=5,
    ...                                  inclusion_radius=20,
    ...                                  periodic=True,
    ...                                  seed=42)
    >>> # Inclusions near boundaries wrap to opposite side
    
    See Also
    --------
    create_binary_model_2d : Create 2D models explicitly
    create_binary_model_3d : Create 3D models explicitly
    export_model : Export with metadata and parameters
    """
    # Set random seed for reproducibility (only if positions not provided)
    if seed is not None and positions is None:
        np.random.seed(seed)
    
    # Validate inputs
    if num_inclusions < 0 or num_inclusions > 100:
        raise ValueError("num_inclusions must be between 0 and 100")
    if inclusion_radius <= 0:
        raise ValueError("inclusion_radius must be positive")
    if inclusion_aspect_ratio <= 0:
        raise ValueError("inclusion_aspect_ratio must be positive")
    if orientation not in ['xy', 'zx', 'zy']:
        raise ValueError("orientation must be 'xy', 'zx', or 'zy'")
    
    # Validate positions if provided
    if positions is not None:
        positions = np.asarray(positions)
        if positions.ndim != 2 or positions.shape[1] != 3:
            raise ValueError("positions must have shape (num_inclusions, 3)")
        if positions.shape[0] != num_inclusions:
            raise ValueError(f"positions has {positions.shape[0]} rows but num_inclusions={num_inclusions}")
        # Check bounds
        if np.any(positions[:, 0] < 0) or np.any(positions[:, 0] >= nx):
            raise ValueError(f"x positions must be in range [0, {nx})")
        if np.any(positions[:, 1] < 0) or np.any(positions[:, 1] >= ny):
            raise ValueError(f"y positions must be in range [0, {ny})")
        if np.any(positions[:, 2] < 0) or np.any(positions[:, 2] >= nz):
            raise ValueError(f"z positions must be in range [0, {nz})")
    
    # Create background volume
    volume = np.full((nx, ny, nz), fill_value=background_value, dtype=dtype)
    
    # Early return if no inclusions requested
    if num_inclusions == 0:
        return volume
    
    # Generate positions for inclusions
    for i in range(num_inclusions):
        if positions is not None:
            # Use provided positions
            pos_x, pos_y, pos_z = positions[i]
        else:
            # Random position within volume
            pos_x = np.random.randint(0, nx)
            pos_y = np.random.randint(0, ny)
            pos_z = np.random.randint(0, nz)
        
        # Handle periodic boundary conditions
        if periodic:
            # Create inclusion at original position and periodic copies
            positions_to_add = [(pos_x, pos_y, pos_z)]
            
            # Check if inclusion extends beyond boundaries
            max_extent = inclusion_radius * max(1.0, inclusion_aspect_ratio)
            
            # Determine which periodic images are needed in 3D
            shifts = []
            
            # Face-adjacent periodic copies
            if pos_x - max_extent < 0:
                shifts.append((nx, 0, 0))
            if pos_x + max_extent >= nx:
                shifts.append((-nx, 0, 0))
            if pos_y - max_extent < 0:
                shifts.append((0, ny, 0))
            if pos_y + max_extent >= ny:
                shifts.append((0, -ny, 0))
            if pos_z - max_extent < 0:
                shifts.append((0, 0, nz))
            if pos_z + max_extent >= nz:
                shifts.append((0, 0, -nz))
            
            # Edge-adjacent periodic copies (12 edges of a cube)
            if (pos_x - max_extent < 0) and (pos_y - max_extent < 0):
                shifts.append((nx, ny, 0))
            if (pos_x - max_extent < 0) and (pos_y + max_extent >= ny):
                shifts.append((nx, -ny, 0))
            if (pos_x + max_extent >= nx) and (pos_y - max_extent < 0):
                shifts.append((-nx, ny, 0))
            if (pos_x + max_extent >= nx) and (pos_y + max_extent >= ny):
                shifts.append((-nx, -ny, 0))
            
            if (pos_x - max_extent < 0) and (pos_z - max_extent < 0):
                shifts.append((nx, 0, nz))
            if (pos_x - max_extent < 0) and (pos_z + max_extent >= nz):
                shifts.append((nx, 0, -nz))
            if (pos_x + max_extent >= nx) and (pos_z - max_extent < 0):
                shifts.append((-nx, 0, nz))
            if (pos_x + max_extent >= nx) and (pos_z + max_extent >= nz):
                shifts.append((-nx, 0, -nz))
            
            if (pos_y - max_extent < 0) and (pos_z - max_extent < 0):
                shifts.append((0, ny, nz))
            if (pos_y - max_extent < 0) and (pos_z + max_extent >= nz):
                shifts.append((0, ny, -nz))
            if (pos_y + max_extent >= ny) and (pos_z - max_extent < 0):
                shifts.append((0, -ny, nz))
            if (pos_y + max_extent >= ny) and (pos_z + max_extent >= nz):
                shifts.append((0, -ny, -nz))
            
            # Corner-adjacent periodic copies (8 corners of a cube)
            if (pos_x - max_extent < 0) and (pos_y - max_extent < 0) and (pos_z - max_extent < 0):
                shifts.append((nx, ny, nz))
            if (pos_x - max_extent < 0) and (pos_y - max_extent < 0) and (pos_z + max_extent >= nz):
                shifts.append((nx, ny, -nz))
            if (pos_x - max_extent < 0) and (pos_y + max_extent >= ny) and (pos_z - max_extent < 0):
                shifts.append((nx, -ny, nz))
            if (pos_x - max_extent < 0) and (pos_y + max_extent >= ny) and (pos_z + max_extent >= nz):
                shifts.append((nx, -ny, -nz))
            if (pos_x + max_extent >= nx) and (pos_y - max_extent < 0) and (pos_z - max_extent < 0):
                shifts.append((-nx, ny, nz))
            if (pos_x + max_extent >= nx) and (pos_y - max_extent < 0) and (pos_z + max_extent >= nz):
                shifts.append((-nx, ny, -nz))
            if (pos_x + max_extent >= nx) and (pos_y + max_extent >= ny) and (pos_z - max_extent < 0):
                shifts.append((-nx, -ny, nz))
            if (pos_x + max_extent >= nx) and (pos_y + max_extent >= ny) and (pos_z + max_extent >= nz):
                shifts.append((-nx, -ny, -nz))
            
            # Add all periodic copies
            for shift_x, shift_y, shift_z in shifts:
                positions_to_add.append((pos_x + shift_x, pos_y + shift_y, pos_z + shift_z))
            
            # Create ellipsoid at each position (original + periodic copies)
            for px, py, pz in positions_to_add:
                ellipsoid_mask = _make_ellipsoid_mask(
                    nx, ny, nz, px, py, pz,
                    inclusion_radius,
                    inclusion_aspect_ratio,
                    orientation,
                    random_orientation
                )
                volume[ellipsoid_mask] = inclusion_value
        else:
            # No periodic boundaries - standard behavior
            ellipsoid_mask = _make_ellipsoid_mask(
                nx, ny, nz,
                pos_x, pos_y, pos_z,
                inclusion_radius,
                inclusion_aspect_ratio,
                orientation,
                random_orientation
            )
            volume[ellipsoid_mask] = inclusion_value

        
        # Add inclusion to volume (union operation)
        volume[ellipsoid_mask] = inclusion_value
    
    return volume


def create_binary_model_2d(nx, ny,
                           num_inclusions=1,
                           inclusion_radius=10,
                           inclusion_aspect_ratio=1.0,
                           random_orientation=False,
                           background_value=1,
                           inclusion_value=0,
                           dtype='uint8',
                           seed=None,
                           positions=None,
                           periodic=False):
    """
    Create a 2D binary model with elliptical inclusions in a homogeneous background.
    
    This function generates a 2D image (stored as nx × ny × 1 volume) with elliptical
    inclusions. Perfect for 2D microstructure models, thin sections, or slice-based analysis.
    
    Parameters
    ----------
    nx, ny : int
        Grid dimensions along x and y axes.
    num_inclusions : int, optional (default=1)
        Number of elliptical inclusions to create. Maximum 100.
    inclusion_radius : float, optional (default=10)
        Radius of the ellipse (in voxels).
    inclusion_aspect_ratio : float, optional (default=1.0)
        Aspect ratio for ellipse shape. 
        - 1.0 creates a circle
        - <1.0 creates an ellipse flattened vertically
        - >1.0 creates an ellipse elongated vertically
    random_orientation : bool, optional (default=False)
        If True, each inclusion gets a random rotation angle (0-180°).
        If False, all inclusions aligned with axes.
    background_value : int, optional (default=1)
        Value for background phase (rock matrix/solid).
    inclusion_value : int, optional (default=0)
        Value for inclusion phase (pore space).
    dtype : str or numpy.dtype, optional (default='uint8')
        Data type of the output model.
    seed : int, optional (default=None)
        Random seed for reproducible placement.
    positions : numpy.ndarray or list, optional (default=None)
        Explicit positions for inclusion centers. If provided, must be array-like 
        with shape (num_inclusions, 2) where each row is [x, y] coordinates.
        Example: positions = np.array([[50, 50], [30, 30]])
    periodic : bool, optional (default=False)
        If True, apply periodic boundary conditions. Inclusions near boundaries
        will wrap around to the opposite side, creating a seamless tileable pattern.
        Useful for creating representative volume elements (RVE) without edge effects.
    
    Returns
    -------
    numpy.ndarray
        3D array with shape (nx, ny, 1) containing the 2D binary model.
        The third dimension has size 1 for consistency with 3D models.
    
    Examples
    --------
    >>> import drp_template.tools as tools
    >>> 
    >>> # 2D model with circular pores
    >>> data_2d = tools.create_binary_model_2d(200, 200,
    ...                                        num_inclusions=10,
    ...                                        inclusion_radius=15,
    ...                                        seed=42)
    >>> print(data_2d.shape)  # (200, 200, 1)
    >>> 
    >>> # 2D model with periodic boundary conditions
    >>> data_2d = tools.create_binary_model_2d(300, 300,
    ...                                        num_inclusions=20,
    ...                                        inclusion_radius=12,
    ...                                        periodic=True,
    ...                                        seed=123)
    >>> # Inclusions wrap around edges - tileable!
    
    See Also
    --------
    create_binary_model_3d : Create 3D models
    create_binary_model : Auto-detect 2D or 3D
    """
    # Set random seed
    if seed is not None and positions is None:
        np.random.seed(seed)
    
    # Validate inputs
    if num_inclusions < 0 or num_inclusions > 100:
        raise ValueError("num_inclusions must be between 0 and 100")
    if inclusion_radius <= 0:
        raise ValueError("inclusion_radius must be positive")
    if inclusion_aspect_ratio <= 0:
        raise ValueError("inclusion_aspect_ratio must be positive")
    
    # Validate positions if provided (2D: only x, y)
    if positions is not None:
        positions = np.asarray(positions)
        if positions.ndim != 2 or positions.shape[1] != 2:
            raise ValueError("For 2D models, positions must have shape (num_inclusions, 2)")
        if positions.shape[0] != num_inclusions:
            raise ValueError(f"positions has {positions.shape[0]} rows but num_inclusions={num_inclusions}")
        if np.any(positions[:, 0] < 0) or np.any(positions[:, 0] >= nx):
            raise ValueError(f"x positions must be in range [0, {nx})")
        if np.any(positions[:, 1] < 0) or np.any(positions[:, 1] >= ny):
            raise ValueError(f"y positions must be in range [0, {ny})")
    
    # Create background (2D slice stored as nx × ny × 1)
    volume = np.full((nx, ny, 1), fill_value=background_value, dtype=dtype)
    
    if num_inclusions == 0:
        return volume
    
    # Generate ellipses in 2D
    for i in range(num_inclusions):
        if positions is not None:
            pos_x, pos_y = positions[i]
        else:
            pos_x = np.random.randint(0, nx)
            pos_y = np.random.randint(0, ny)
        
        # Handle periodic boundary conditions
        if periodic:
            # Create inclusion at original position and periodic copies
            positions_to_add = [(pos_x, pos_y)]
            
            # Check if inclusion extends beyond boundaries
            # Add periodic copies if needed (±nx, ±ny)
            max_extent = inclusion_radius * max(1.0, inclusion_aspect_ratio)
            
            # Determine which periodic images are needed
            shifts = []
            if pos_x - max_extent < 0:
                shifts.append((nx, 0))  # Wrap to right
            if pos_x + max_extent >= nx:
                shifts.append((-nx, 0))  # Wrap to left
            if pos_y - max_extent < 0:
                shifts.append((0, ny))  # Wrap to top
            if pos_y + max_extent >= ny:
                shifts.append((0, -ny))  # Wrap to bottom
            
            # Corner cases (diagonal wrapping)
            if (pos_x - max_extent < 0) and (pos_y - max_extent < 0):
                shifts.append((nx, ny))
            if (pos_x - max_extent < 0) and (pos_y + max_extent >= ny):
                shifts.append((nx, -ny))
            if (pos_x + max_extent >= nx) and (pos_y - max_extent < 0):
                shifts.append((-nx, ny))
            if (pos_x + max_extent >= nx) and (pos_y + max_extent >= ny):
                shifts.append((-nx, -ny))
            
            # Add all periodic copies
            for shift_x, shift_y in shifts:
                positions_to_add.append((pos_x + shift_x, pos_y + shift_y))
            
            # Create ellipse at each position (original + periodic copies)
            for px, py in positions_to_add:
                ellipse_mask = _make_ellipse_mask_2d(
                    nx, ny, px, py,
                    inclusion_radius,
                    inclusion_aspect_ratio,
                    random_orientation
                )
                volume[:, :, 0][ellipse_mask] = inclusion_value
        else:
            # No periodic boundaries - standard behavior
            ellipse_mask = _make_ellipse_mask_2d(
                nx, ny,
                pos_x, pos_y,
                inclusion_radius,
                inclusion_aspect_ratio,
                random_orientation
            )
            volume[:, :, 0][ellipse_mask] = inclusion_value
    
    return volume


def create_binary_model_3d(nx, ny, nz,
                           num_inclusions=1,
                           inclusion_radius=10,
                           inclusion_aspect_ratio=1.0,
                           orientation='xy',
                           random_orientation=False,
                           background_value=1,
                           inclusion_value=0,
                           dtype='uint8',
                           seed=None,
                           positions=None,
                           periodic=False):
    """
    Create a 3D binary model with ellipsoidal inclusions in a homogeneous background.
    
    This is the explicit 3D version of create_binary_model. Use this when you specifically
    want 3D ellipsoids with full 3D orientation control.
    
    Parameters
    ----------
    nx, ny, nz : int
        Grid dimensions along x, y, z axes.
    num_inclusions : int, optional (default=1)
        Number of ellipsoidal inclusions to create. Maximum 100.
    inclusion_radius : float, optional (default=10)
        Radius of the ellipsoid (in voxels).
    inclusion_aspect_ratio : float, optional (default=1.0)
        Aspect ratio for ellipsoid shape. 
        - 1.0 creates a sphere
        - <1.0 creates an oblate ellipsoid (flattened)
        - >1.0 creates a prolate ellipsoid (elongated)
    orientation : str, optional (default='xy')
        Primary plane for ellipsoid orientation when random_orientation=False:
        - 'xy': Ellipse in xy-plane (flattened/elongated in Z)
        - 'zx': Ellipse in zx-plane (flattened/elongated in Y)
        - 'zy': Ellipse in zy-plane (flattened/elongated in X)
        Ignored when random_orientation=True.
    random_orientation : bool, optional (default=False)
        If True, each inclusion gets a random 3D rotation (true 3D orientation).
        If False, all inclusions aligned according to 'orientation' parameter.
    background_value : int, optional (default=1)
        Value for background phase (rock matrix/solid).
    inclusion_value : int, optional (default=0)
        Value for inclusion phase (pore space).
    dtype : str or numpy.dtype, optional (default='uint8')
        Data type of the output model.
    seed : int, optional (default=None)
        Random seed for reproducible placement.
    positions : numpy.ndarray or list, optional (default=None)
        Explicit positions for inclusion centers. If provided, must be array-like 
        with shape (num_inclusions, 3) where each row is [x, y, z] coordinates.
        Example: positions = np.array([[50, 50, 50], [30, 30, 30]])
    periodic : bool, optional (default=False)
        If True, apply periodic boundary conditions. Inclusions near boundaries
        will wrap around to the opposite side in all three dimensions, creating 
        a seamless tileable volume. Useful for creating representative volume 
        elements (RVE) without edge effects.
    
    Returns
    -------
    numpy.ndarray
        3D array with shape (nx, ny, nz) containing the binary model.
    
    Examples
    --------
    >>> import drp_template.tools as tools
    >>> 
    >>> # 3D model with spherical pores
    >>> data_3d = tools.create_binary_model_3d(100, 100, 100,
    ...                                        num_inclusions=10,
    ...                                        inclusion_radius=15,
    ...                                        seed=42)
    >>> 
    >>> # 3D model with periodic boundaries
    >>> data_3d = tools.create_binary_model_3d(200, 200, 200,
    ...                                        num_inclusions=20,
    ...                                        inclusion_radius=12,
    ...                                        inclusion_aspect_ratio=1.5,
    ...                                        random_orientation=True,
    ...                                        periodic=True,
    ...                                        seed=123)
    >>> # Volume is seamlessly tileable in all directions!
    
    See Also
    --------
    create_binary_model_2d : Create 2D models
    create_binary_model : Auto-detect 2D or 3D
    """
    # This wraps the original create_binary_model with periodic support
    return create_binary_model(
        nx=nx, ny=ny, nz=nz,
        num_inclusions=num_inclusions,
        inclusion_radius=inclusion_radius,
        inclusion_aspect_ratio=inclusion_aspect_ratio,
        orientation=orientation,
        random_orientation=random_orientation,
        background_value=background_value,
        inclusion_value=inclusion_value,
        dtype=dtype,
        seed=seed,
        positions=positions,
        periodic=periodic
    )


def _make_ellipse_mask_2d(nx, ny, pos_x, pos_y, radius, aspect_ratio, random_rotation):
    """
    Internal helper to create a 2D ellipse mask.
    
    Parameters
    ----------
    nx, ny : int
        Grid dimensions.
    pos_x, pos_y : float
        Center position of ellipse.
    radius : float
        Primary radius in voxels.
    aspect_ratio : float
        Aspect ratio (width/height).
    random_rotation : bool
        Apply random rotation.
    
    Returns
    -------
    numpy.ndarray
        Boolean mask with shape (nx, ny).
    """
    # Create coordinate grids
    x_grid, y_grid = np.ogrid[:nx, :ny]
    x_grid = x_grid - pos_x
    y_grid = y_grid - pos_y
    
    # Convert to full meshgrid for rotation
    x_full = np.broadcast_to(x_grid, (nx, ny)).astype(float)
    y_full = np.broadcast_to(y_grid, (nx, ny)).astype(float)
    
    if random_rotation:
        # Random 2D rotation
        angle = np.random.uniform(0, 2 * np.pi)
        x_rot = x_full * np.cos(angle) - y_full * np.sin(angle)
        y_rot = x_full * np.sin(angle) + y_full * np.cos(angle)
        x_full, y_full = x_rot, y_rot
    
    # Create ellipse mask
    mask = ((x_full**2 / radius**2) + (y_full**2 / (aspect_ratio * radius)**2)) <= 1
    
    return mask


def _make_ellipsoid_mask(nx, ny, nz, pos_x, pos_y, pos_z, 
                         radius, aspect_ratio, orientation, random_rotation):
    """
    Internal helper to create an ellipsoid mask.
    
    Parameters
    ----------
    nx, ny, nz : int
        Volume dimensions.
    pos_x, pos_y, pos_z : int
        Center position of ellipsoid.
    radius : float
        Primary radius in voxels.
    aspect_ratio : float
        Aspect ratio for ellipsoid.
    orientation : str
        Primary plane ('xy', 'zx', 'zy').
        Only used when random_rotation=False.
    random_rotation : bool
        Apply random 3D rotation. If True, orientation is ignored and
        the ellipsoid is randomly oriented in 3D space.
    
    Returns
    -------
    numpy.ndarray
        Boolean mask with shape (nx, ny, nz).
    """
    # Create coordinate grids centered at ellipsoid position
    x_grid, y_grid, z_grid = np.ogrid[:nx, :ny, :nz]
    x_grid = x_grid - pos_x
    y_grid = y_grid - pos_y
    z_grid = z_grid - pos_z
    
    # Convert ogrid to full meshgrid for rotation
    x_full = np.broadcast_to(x_grid, (nx, ny, nz)).astype(float)
    y_full = np.broadcast_to(y_grid, (nx, ny, nz)).astype(float)
    z_full = np.broadcast_to(z_grid, (nx, ny, nz)).astype(float)
    
    if random_rotation:
        # TRUE 3D RANDOM ROTATION using Euler angles
        # Generate random Euler angles for full 3D orientation
        alpha = np.random.uniform(0, 2 * np.pi)  # Rotation around Z
        beta = np.random.uniform(0, np.pi)        # Rotation around Y (inclination)
        gamma = np.random.uniform(0, 2 * np.pi)  # Rotation around X
        
        # Build 3D rotation matrix (ZYX Euler angles)
        # R = Rz(alpha) * Ry(beta) * Rx(gamma)
        
        # Rotation around Z
        Rz = np.array([
            [np.cos(alpha), -np.sin(alpha), 0],
            [np.sin(alpha), np.cos(alpha), 0],
            [0, 0, 1]
        ])
        
        # Rotation around Y
        Ry = np.array([
            [np.cos(beta), 0, np.sin(beta)],
            [0, 1, 0],
            [-np.sin(beta), 0, np.cos(beta)]
        ])
        
        # Rotation around X
        Rx = np.array([
            [1, 0, 0],
            [0, np.cos(gamma), -np.sin(gamma)],
            [0, np.sin(gamma), np.cos(gamma)]
        ])
        
        # Combined rotation matrix
        R = Rz @ Ry @ Rx
        
        # Apply rotation to coordinate grids
        coords = np.stack([x_full.ravel(), y_full.ravel(), z_full.ravel()], axis=0)
        rotated_coords = R @ coords
        
        x_rot = rotated_coords[0].reshape((nx, ny, nz))
        y_rot = rotated_coords[1].reshape((nx, ny, nz))
        z_rot = rotated_coords[2].reshape((nx, ny, nz))
        
        # For random rotation, use a standard ellipsoid aligned with Z-axis
        # One axis has full radius, the perpendicular axis is scaled by aspect_ratio
        if aspect_ratio != 1.0:
            # Z is the "special" axis (either elongated or flattened)
            mask = ((x_rot**2 / radius**2) + 
                    (y_rot**2 / radius**2) + 
                    (z_rot**2 / (aspect_ratio * radius)**2)) <= 1
        else:
            # Sphere
            mask = ((x_rot**2 / radius**2) + 
                    (y_rot**2 / radius**2) + 
                    (z_rot**2 / radius**2)) <= 1
    else:
        # NO ROTATION: Use fixed orientation based on 'orientation' parameter
        # Create ellipsoid mask based on orientation
        # The aspect_ratio controls the radius in the direction perpendicular to the orientation plane
        if orientation == 'xy':
            # Ellipse in xy-plane (wide in X and Y), flattened in Z direction
            # X and Y have full radius, Z is scaled by aspect_ratio
            mask = ((x_full**2 / radius**2) + 
                    (y_full**2 / radius**2) + 
                    (z_full**2 / (aspect_ratio * radius)**2)) <= 1
        elif orientation == 'zx':
            # Ellipse in zx-plane (wide in Z and X), flattened in Y direction
            # Z and X have full radius, Y is scaled by aspect_ratio
            mask = ((z_full**2 / radius**2) + 
                    (x_full**2 / radius**2) + 
                    (y_full**2 / (aspect_ratio * radius)**2)) <= 1
        elif orientation == 'zy':
            # Ellipse in zy-plane (wide in Z and Y), flattened in X direction
            # Z and Y have full radius, X is scaled by aspect_ratio
            mask = ((z_full**2 / radius**2) + 
                    (y_full**2 / radius**2) + 
                    (x_full**2 / (aspect_ratio * radius)**2)) <= 1
    
    return mask

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


def infer_dimensions_from_filesize(file_size_bytes, dtype=np.uint8):
    """
    Infer cubic dimensions from file size assuming uniform dimensions.
    
    Parameters:
    -----------
    file_size_bytes : int
        Size of the file in bytes.
    dtype : numpy.dtype, optional (default=np.uint8)
        Data type to assume for calculation.
    
    Returns:
    --------
    dict : Dictionary with 'nx', 'ny', 'nz' keys (all equal for cubic).
    
    Examples:
    ---------
    ```python
    dims = infer_dimensions_from_filesize(64000000, dtype=np.uint8)
    # Returns {'nx': 400, 'ny': 400, 'nz': 400}
    ```
    """
    bytes_per_element = np.dtype(dtype).itemsize
    total_voxels = file_size_bytes // bytes_per_element
    cube_side = round(total_voxels ** (1/3))
    
    return {'nx': cube_side, 'ny': cube_side, 'nz': cube_side}


def infer_dtype_from_filesize(file_size_bytes, total_voxels):
    """
    Infer NumPy data type from file size and expected voxel count.
    
    Parameters:
    -----------
    file_size_bytes : int
        Size of the file in bytes.
    total_voxels : int
        Expected total number of voxels.
    
    Returns:
    --------
    numpy.dtype : Inferred NumPy data type.
    
    Examples:
    ---------
    ```python
    dtype = infer_dtype_from_filesize(64000000, 64000000)
    # Returns np.uint8
    
    dtype = infer_dtype_from_filesize(128000000, 64000000)
    # Returns np.uint16
    ```
    """
    bytes_per_voxel = file_size_bytes / total_voxels
    
    if bytes_per_voxel <= 1:
        return np.uint8
    elif bytes_per_voxel <= 2:
        return np.uint16
    elif bytes_per_voxel <= 4:
        return np.float32
    else:
        return np.uint8  # Default fallback


def classify_data_type(num_unique_values):
    """
    Classify data as segmented, grayscale, or continuous based on unique value count.
    
    Parameters:
    -----------
    num_unique_values : int
        Number of unique values in the dataset.
    
    Returns:
    --------
    tuple : (data_type_string, phase_count or None)
        - data_type_string: 'segmented', '8-bit grayscale', '16-bit grayscale', 'continuous'
        - phase_count: Number of phases for segmented data, None otherwise.
    
    Examples:
    ---------
    ```python
    data_type, phases = classify_data_type(3)
    # Returns ('segmented', 3)
    
    data_type, phases = classify_data_type(1500)
    # Returns ('16-bit grayscale', None)
    ```
    """
    if num_unique_values <= 10:
        return 'segmented', num_unique_values
    elif num_unique_values <= 256:
        return '8-bit grayscale', None
    elif num_unique_values <= 65536:
        return '16-bit grayscale', None
    else:
        return 'continuous', None


def get_value_statistics(data):
    """
    Calculate statistics for unique values in the data.
    
    Parameters:
    -----------
    data : numpy.ndarray
        Input data array.
    
    Returns:
    --------
    dict : Dictionary containing:
        - 'unique_values': Sorted array of unique values
        - 'num_unique': Number of unique values
        - 'value_counts': Dict mapping value to count
        - 'value_percentages': Dict mapping value to percentage
        - 'min_value': Minimum value
        - 'max_value': Maximum value
    
    Examples:
    ---------
    ```python
    stats = get_value_statistics(data)
    print(f"Found {stats['num_unique']} unique values")
    print(f"Value 0 appears {stats['value_percentages'][0]:.2f}% of the time")
    ```
    """
    unique_values, counts = np.unique(data, return_counts=True)
    total_voxels = len(data)
    
    value_counts = dict(zip(unique_values.tolist(), counts.tolist()))
    value_percentages = {val: (count / total_voxels * 100) 
                        for val, count in value_counts.items()}
    
    return {
        'unique_values': unique_values,
        'num_unique': len(unique_values),
        'value_counts': value_counts,
        'value_percentages': value_percentages,
        'min_value': int(np.min(data)),
        'max_value': int(np.max(data))
    }


def get_model_properties(filepath, dimensions=None, labels=None, verbose=True):
    """
    Analyze a raw binary file to determine its properties and data characteristics.
    
    This function provides a quick overview of file-level properties and basic statistics.
    For detailed phase analysis with DataFrame output and saving to parameters file,
    use drp_template.math.get_phase_fractions() instead.
    
    Parameters:
    -----------
    filepath : str
        Path to the raw binary file.
    dimensions : dict, optional (default=None)
        Dictionary with 'nx', 'ny', 'nz' keys. If None, will be inferred from file size.
    labels : dict, optional (default=None)
        Dictionary mapping phase values (as strings) to phase names.
        Example: {"0": "Pore", "1": "Quartz", "2": "Feldspar"}
        If provided, phase names will be shown inline in the quick overview.
        For detailed labeled output, use drp_template.math.get_phase_fractions().
    verbose : bool, optional (default=True)
        Print detailed information about the model.
    
    Returns:
    --------
    dict : Dictionary containing:
        - 'unique_values': Sorted array of unique values in the data
        - 'num_unique': Number of unique values
        - 'min_value': Minimum value
        - 'max_value': Maximum value
        - 'data_type': Inferred data type ('segmented', '8-bit grayscale', '16-bit grayscale', 'continuous')
        - 'phase_count': Number of phases (for segmented data, None otherwise)
        - 'value_counts': Dictionary mapping each unique value to its count
        - 'value_percentages': Dictionary mapping each unique value to its percentage
        - 'file_size_mb': File size in megabytes
        - 'dimensions': Actual or inferred dimensions
        - 'total_voxels': Total number of voxels
        - 'dtype': NumPy data type used
        - 'dimensions_inferred': Boolean indicating if dimensions were inferred
    
    Examples:
    ---------
    ```python
    import drp_template.tools as tools
    import drp_template.math as drp_math
    
    # Quick file overview
    props = tools.get_model_properties('model.raw', 
                                       dimensions={'nx': 400, 'ny': 400, 'nz': 400})
    
    # Quick overview with labels shown inline
    labels = {"0": "Pore", "1": "Quartz", "2": "Feldspar"}
    props = tools.get_model_properties('model.raw', 
                                       dimensions={'nx': 400, 'ny': 400, 'nz': 400},
                                       labels=labels)
    
    # For detailed phase analysis (recommended for segmented data):
    # Load the data first
    data = io.import_model(file_path='model.raw', dtype='uint8', dimensions=dimensions)
    # Then use get_phase_fractions for detailed analysis
    table = drp_math.get_phase_fractions(data, labels=labels, log=True)
    
    # Auto-detect dimensions (assumes cubic)
    props = tools.get_model_properties('model.raw')
    ```
    
    Notes:
    ------
    - This function provides a QUICK OVERVIEW of file properties
    - For DETAILED PHASE ANALYSIS with formatted tables and parameter file saving,
      use drp_template.math.get_phase_fractions() instead
    - If dimensions are not provided, assumes cubic geometry
    - Automatically determines data type (uint8, uint16, float32) from file size
    - Uses modular helper functions: infer_dimensions_from_filesize, 
      infer_dtype_from_filesize, classify_data_type, get_value_statistics
    
    See Also:
    ---------
    drp_template.math.get_phase_fractions : Detailed phase analysis with DataFrame,
                                            formatted tables, and parameter file saving
    """
    # Get file size
    file_size_bytes = os.path.getsize(filepath)
    file_size_mb = file_size_bytes / (1024 * 1024)
    
    # Determine dimensions
    if dimensions is None:
        dimensions = infer_dimensions_from_filesize(file_size_bytes, dtype=np.uint8)
        dimensions_inferred = True
    else:
        dimensions_inferred = False
    
    total_voxels = dimensions['nx'] * dimensions['ny'] * dimensions['nz']
    
    # Determine dtype
    dtype = infer_dtype_from_filesize(file_size_bytes, total_voxels)
    
    # Read the data
    data = np.fromfile(filepath, dtype=dtype, count=total_voxels)
    
    # Get value statistics
    stats = get_value_statistics(data)
    
    # Classify data type
    data_type, phase_count = classify_data_type(stats['num_unique'])
    
    # Build results dictionary
    results = {
        'unique_values': stats['unique_values'],
        'num_unique': stats['num_unique'],
        'min_value': stats['min_value'],
        'max_value': stats['max_value'],
        'data_type': data_type,
        'phase_count': phase_count,
        'value_counts': stats['value_counts'],
        'value_percentages': stats['value_percentages'],
        'file_size_mb': round(file_size_mb, 2),
        'dimensions': dimensions,
        'total_voxels': total_voxels,
        'dtype': str(dtype),
        'dimensions_inferred': dimensions_inferred
    }
    
    # Print verbose output
    if verbose:
        filename = os.path.basename(filepath)
        print(f"\n{'='*60}")
        print(f"MODEL PROPERTIES: {filename}")
        print(f"{'='*60}")
        print(f"File size:        {file_size_mb:.2f} MB")
        print(f"Dimensions:       [{dimensions['nz']}, {dimensions['ny']}, {dimensions['nx']}]")
        if dimensions_inferred:
            print(f"                  (⚠ inferred - please verify!)")
        print(f"Total voxels:     {total_voxels:,}")
        print(f"Data type:        {dtype.__name__}")
        print(f"\n{'-'*60}")
        print(f"DATA ANALYSIS")
        print(f"{'-'*60}")
        print(f"Classification:   {data_type}")
        print(f"Unique values:    {stats['num_unique']}")
        print(f"Value range:      [{stats['min_value']}, {stats['max_value']}]")
        
        if data_type == 'segmented':
            print(f"Number of phases: {phase_count}")
            print(f"\n{'-'*60}")
            print(f"PHASE DISTRIBUTION (Quick Overview)")
            print(f"{'-'*60}")
            print(f"{'Phase':<8} {'Count':>12} {'Percentage':>12}")
            print(f"{'-'*60}")
            
            for val in stats['unique_values']:
                count = stats['value_counts'][val]
                percentage = stats['value_percentages'][val]
                # Show label if available
                if labels is not None:
                    phase_name = labels.get(str(val), f"Phase {val}")
                    label_str = f" ({phase_name})"
                else:
                    label_str = ""
                print(f"{val:<8} {count:>12,} {percentage:>11.2f}%{label_str}")
            
            print(f"{'-'*60}")
            print(f"TIP: For detailed phase analysis with DataFrame output,")
            print(f"   saving to parameters file, and formatted tables, use:")
            print(f"   drp_template.math.get_phase_fractions(data, labels=labels)")
        else:
            print(f"\n{'-'*60}")
            print(f"VALUE DISTRIBUTION (showing first 10)")
            print(f"{'-'*60}")
            print(f"{'Value':<8} {'Count':>12} {'Percentage':>12}")
            print(f"{'-'*60}")
            for i, val in enumerate(stats['unique_values'][:10]):
                count = stats['value_counts'][val]
                percentage = stats['value_percentages'][val]
                print(f"{val:<8} {count:>12,} {percentage:>11.2f}%")
            if stats['num_unique'] > 10:
                print(f"... and {stats['num_unique'] - 10} more values")
        
        print(f"{'='*60}\n")
    
    return results


def label_binary(data, paramsfile='parameters.json'):
    """
    Label binary phases in a 3D volume based on user input.

    Parameters:
    -----------
    data : numpy.ndarray
        3D binary volume to be labeled.
    paramsfile : str, optional (default='parameters.json')
        Name of the JSON file containing plotting parameters.

    Returns:
    --------
    labels : dict
        Dictionary mapping phase values to user-defined labels.
        
    Examples:
    ---------
    ```python
    import drp_template.tools as tools
    
    # Label phases interactively
    labels = tools.label_binary(data, paramsfile='my_data.json')
    ```
    
    Notes:
    ------
    - This function displays each phase visually using orthogonal slices
    - User is prompted to name each phase interactively
    - Labels are saved to the parameter file for future reference
    - Requires IPython/Jupyter environment for interactive display
    """
    from IPython.display import display
    from drp_template.image import ortho_slice

    # Ensure the input is a binary array (contains only integers)
    if not np.issubdtype(data.dtype, np.integer):
        raise ValueError("Input data must be a binary array containing only integers (0 or 1).")

    # Get the unique values and their counts
    unique, counts = np.unique(data, return_counts=True)

    # Create an empty labels dictionary
    labels = {}
    
    # Get the slice in the xy plane that contains all unique values corresponding to 0
    slice = find_slice_with_all_values(data)
    slice_index = slice['xy']

    for m, value in enumerate(unique):
        # Create a copy of the input array and set all values to 0
        data_temp = np.zeros_like(data)

        # Set the values that match the current unique value to 1
        data_temp[data == value] = 1

        # Set the values that match the current unique value to 1
        data_temp[data == unique[m]] = 1

        # Make the colormap red for the phase of interest
        cmap_reds = plt.cm.Reds
        fig, ax, pcm = ortho_slice(data=data_temp, plane='xy', cmap_set=cmap_reds, paramsfile=paramsfile, title=f"Phase: {m}", slice=slice_index)
        
        # Display the figure in the Jupyter Notebook
        display(fig)

        # Prompt the user to name the presented phase and store the input in labels
        phase_name = input(f'Name the presented phase {value} with index {m}: ')
        labels[str(value)] = phase_name  # Convert the key to a string
        
        # Close the figure to avoid displaying it again
        plt.close(fig)
           
    # update the parameters file with the new labels dictionary
    update_parameters_file(paramsfile, labels=labels)

    return labels