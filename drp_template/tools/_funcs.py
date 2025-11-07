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