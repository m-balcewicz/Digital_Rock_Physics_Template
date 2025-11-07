import os
import numpy as np
from .validation import (
    infer_dimensions_from_filesize,
    infer_dtype_from_filesize,
    classify_data_type,
    get_value_statistics,
)

__all__ = [
    'list_dir_info',
    'get_model_properties'
]


def list_dir_info(directory, extension=None, search_subdirs=False, return_count=False):
    """List files or subdirectories in a directory with flexible filtering."""
    if extension is None:
        directory_listing = [entry.name for entry in os.scandir(directory) if entry.is_dir()]
    elif search_subdirs:
        directory_listing = []
        for entry in os.scandir(directory):
            if entry.is_dir():
                subdir_path = os.path.join(directory, entry.name)
                has_extension = any(
                    f.endswith(extension) for f in os.listdir(subdir_path)
                    if os.path.isfile(os.path.join(subdir_path, f))
                )
                if has_extension:
                    directory_listing.append(entry.name)
    else:
        directory_listing = [entry.name for entry in os.scandir(directory) if entry.is_file() and entry.name.endswith(extension)]
    sorted_listing = sorted(directory_listing)
    return (sorted_listing, len(sorted_listing)) if return_count else sorted_listing

def get_model_properties(filepath, dimensions=None, labels=None, verbose=True):
    """
    Analyze a raw binary file to determine its properties and data characteristics.

    Provides a quick overview of file-level properties and basic statistics.
    For detailed phase analysis with DataFrame output and saving to parameters file,
    use drp_template.compute.phase_fractions() instead.

    Parameters:
    -----------
    filepath : str
        Path to the raw binary file.
    dimensions : dict, optional (default=None)
        Dictionary with 'nx', 'ny', 'nz' keys. If None, will be inferred from file size.
    labels : dict, optional (default=None)
        Dictionary mapping phase values (as strings) to phase names.
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
    """
    file_size_bytes = os.path.getsize(filepath)
    file_size_mb = file_size_bytes / (1024 * 1024)

    # Determine dimensions (assume cubic if not provided)
    if dimensions is None:
        dimensions = infer_dimensions_from_filesize(file_size_bytes, dtype=np.uint8)
        dimensions_inferred = True
    else:
        dimensions_inferred = False

    total_voxels = int(dimensions['nx'] * dimensions['ny'] * dimensions['nz'])

    # Determine dtype from file size and voxel count
    dtype = infer_dtype_from_filesize(file_size_bytes, total_voxels)

    # Read flat data
    data = np.fromfile(filepath, dtype=dtype, count=total_voxels)

    # Stats and classification
    stats = get_value_statistics(data)
    data_type, phase_count = classify_data_type(stats['num_unique'])

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
        'dimensions_inferred': dimensions_inferred,
    }

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
        try:
            dtype_name = dtype.__name__
        except AttributeError:
            dtype_name = str(dtype)
        print(f"Data type:        {dtype_name}")
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
                count = stats['value_counts'][int(val)]
                percentage = stats['value_percentages'][int(val)]
                if labels is not None:
                    phase_name = labels.get(str(int(val)), f"Phase {int(val)}")
                    label_str = f" ({phase_name})"
                else:
                    label_str = ""
                print(f"{int(val):<8} {count:>12,} {percentage:>11.2f}%{label_str}")
            print(f"{'-'*60}")
            print(f"TIP: For detailed phase analysis with DataFrame output,")
            print(f"   saving to parameters file, and formatted tables, use:")
            print(f"   drp_template.compute.phase_fractions(data, labels=labels)")
        else:
            print(f"\n{'-'*60}")
            print(f"VALUE DISTRIBUTION (showing first 10)")
            print(f"{'-'*60}")
            print(f"{'Value':<8} {'Count':>12} {'Percentage':>12}")
            print(f"{'-'*60}")
            uv = stats['unique_values']
            for i, val in enumerate(uv[: min(10, len(uv))]):
                count = stats['value_counts'][int(val)]
                percentage = stats['value_percentages'][int(val)]
                print(f"{int(val):<8} {count:>12,} {percentage:>11.2f}%")
            if stats['num_unique'] > 10:
                print(f"... and {stats['num_unique'] - 10} more values")

        print(f"{'='*60}\n")

    return results
