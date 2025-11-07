import numpy as np
from drp_template.default_params import print_style

__all__ = [
    'check_binary',
    'infer_dimensions_from_filesize',
    'infer_dtype_from_filesize',
    'classify_data_type',
    'get_value_statistics'
]


def check_binary(model, filename):
    """Normalize binary-like data so minimum is 0."""
    unique_phases = np.unique(model)
    if min(unique_phases) == 0:
        print_style(f'{filename}:\nNice data; the minimum value in your data is 0')
    elif min(unique_phases) == -1:
        print_style(f'{filename}:\nUps, minimum value is -1. Adjusting by +1.')
        model = model + 1
    elif min(unique_phases) == 1:
        print_style(f'{filename}:\nUps, minimum value is 1. Adjusting by -1.')
        model = model - 1
    return model


def infer_dimensions_from_filesize(file_size_bytes, dtype=np.uint8):
    """Infer cubic dimensions from file size assuming uniform dimensions."""
    bytes_per_element = np.dtype(dtype).itemsize
    total_voxels = file_size_bytes // bytes_per_element
    cube_side = round(total_voxels ** (1/3))
    return {'nx': cube_side, 'ny': cube_side, 'nz': cube_side}


def infer_dtype_from_filesize(file_size_bytes, total_voxels):
    """Infer NumPy dtype from file size and expected voxel count.

    Matches legacy behavior: uint8, uint16, float32; falls back to uint8.
    """
    bytes_per_voxel = file_size_bytes / total_voxels
    if bytes_per_voxel <= 1:
        return np.uint8
    elif bytes_per_voxel <= 2:
        return np.uint16
    elif bytes_per_voxel <= 4:
        return np.float32
    else:
        return np.uint8


def classify_data_type(num_unique_values):
    """Classify data as segmented, 8/16-bit grayscale, or continuous (legacy-compatible)."""
    if num_unique_values <= 10:
        return 'segmented', num_unique_values
    elif num_unique_values <= 256:
        return '8-bit grayscale', None
    elif num_unique_values <= 65536:
        return '16-bit grayscale', None
    else:
        return 'continuous', None


def get_value_statistics(data):
    """Return statistics of unique values including counts, percentages, and range."""
    unique_vals, counts = np.unique(data, return_counts=True)
    total = int(counts.sum())
    percentages = counts / total * 100 if total > 0 else np.zeros_like(counts, dtype=float)
    return {
        'unique_values': unique_vals,  # keep as numpy array (legacy-compatible)
        'value_counts': {int(k): int(v) for k, v in zip(unique_vals, counts)},
        'value_percentages': {int(k): float(p) for k, p in zip(unique_vals, percentages)},
        'num_unique': int(len(unique_vals)),
        'min_value': int(np.min(data)) if total > 0 else None,
        'max_value': int(np.max(data)) if total > 0 else None,
        'total_count': total,
    }
