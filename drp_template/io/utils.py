"""
I/O Utility Functions
=====================

Internal helper functions for data reorientation and parameter updates.

These utilities support the readers and writers modules by handling
common operations like volume reorientation and parameter file updates.

Functions
---------
- get_dim_order: Get dimension order from dictionary keys
- reorient_volume: Reorient 3D arrays to standard (nx, ny, nz) order
- _update_params_common: Update parameters JSON with common metadata
- update_params_after_import: Update parameters after TIFF sequence import
"""

import os
import numpy as np
import sys
import glob
import shutil
import subprocess
from typing import Optional, Tuple

from drp_template.default_params import update_parameters_file

__all__ = [
    'get_dim_order',
    'reorient_volume',
    '_update_params_common',
    'update_params_after_import',
    'resolve_params_filename',
    'open_in_paraview',
]


def get_dim_order(dimensions):
    """
    Returns the order of dimension keys as a tuple, e.g. ('nz', 'ny', 'nx').
    
    Parameters
    ----------
    dimensions : dict
        Dictionary with dimension keys (e.g., {'nx': 400, 'ny': 400, 'nz': 400})
    
    Returns
    -------
    tuple
        Ordered tuple of dimension names
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
        The reoriented volume in (nx, ny, nz) order.
        
    Raises
    ------
    ValueError
    If the dimension order is unsupported.
    """
    if dim_order == ('nx', 'ny', 'nz'):
        return volume

    # Generic normalization (broader set supported for historical imports)
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


def _update_params_common(params_filename, file_path, arr, voxel_size, dtype, endian, file_format):
    """
    Helper to update the parameters JSON file with common fields.
    
    Parameters
    ----------
    params_filename : str
        Name of the parameters JSON file
    file_path : str
        Path to the data file
    arr : np.ndarray
        The data array
    voxel_size : float or None
        Voxel size in micrometers
    dtype : str
        Data type string
    endian : str
        Endianness ('small', 'big', 'little')
    file_format : str
        File format extension
    """
    update_parameters_file(paramsfile=params_filename, file_path=file_path)
    update_parameters_file(paramsfile=params_filename, dim=arr.ndim)
    print(f"Dimensions: {arr.ndim}")
    update_parameters_file(paramsfile=params_filename, nx=arr.shape[0], ny=arr.shape[1], nz=arr.shape[2])
    print(f"nx: {arr.shape[0]}")
    print(f"ny: {arr.shape[1]}")
    print(f"nz: {arr.shape[2]}")
    
    # Only update fields that have actual values (not None)
    if voxel_size is not None:
        update_parameters_file(paramsfile=params_filename, voxel_size=voxel_size)
    if endian is not None:
        update_parameters_file(paramsfile=params_filename, endian=endian)
    if dtype is not None:
        update_parameters_file(paramsfile=params_filename, dtype=dtype)
    if file_format is not None:
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
    
    Parameters
    ----------
    params_filename : str
        Name of the parameters JSON file
    file_path : str
        Path to the first TIFF file
    volume : np.ndarray
        The loaded volume
    voxel_size : float or None
        Voxel size in micrometers
    dtype : str
        Data type string
    """
    _update_params_common(
        params_filename, file_path, volume, voxel_size, dtype,
        endian='small', file_format='tiff'
    )


def resolve_params_filename(paramsfile: str = 'parameters.json', ensure_unique: bool = True) -> str:
    """
    Resolve a parameters filename within the output folder, ensuring uniqueness.

    If a file with the requested name already exists in the output folder, and
    ensure_unique is True, this appends an incrementing suffix before the file
    extension, e.g., parameters.json -> parameters_1.json -> parameters_2.json.

    Parameters
    ----------
    paramsfile : str, optional
        Desired parameters filename (default: 'parameters.json').
    ensure_unique : bool, optional
        If True, avoid overwriting by adding a numeric suffix when needed.

    Returns
    -------
    str
        A parameters filename (basename only) that does not collide in output/.
    """
    from drp_template.default_params import check_output_folder

    # Normalize name (basename only; update_parameters_file will place it under output/)
    base_name = os.path.basename(paramsfile) if paramsfile else 'parameters.json'

    if not ensure_unique:
        return base_name

    output_dir = check_output_folder()
    name, ext = os.path.splitext(base_name)
    ext = ext or '.json'

    candidate = base_name
    counter = 1
    while os.path.exists(os.path.join(output_dir, candidate)):
        candidate = f"{name}_{counter}{ext}"
        counter += 1
    return candidate


def _find_paraview_executable(user_path: Optional[str] = None) -> str:
    """Locate ParaView executable across platforms.

    Search order:
    1) Explicit user_path if provided and exists
    2) shutil.which('paraview')
    3) Platform-specific fallbacks:
       - macOS: /Applications/ParaView*.app/Contents/MacOS/paraview (latest)
       - Linux: /usr/bin/paraview, /snap/bin/paraview, /opt/paraview/bin/paraview
       - Windows: C:\\Program Files\\ParaView*\\bin\\paraview.exe (latest), PATH lookup
    """
    if user_path and os.path.isfile(user_path):
        return user_path

    which = shutil.which('paraview')
    if which:
        return which

    if sys.platform == 'darwin':
        candidates = sorted(
            glob.glob('/Applications/ParaView*.app/Contents/MacOS/paraview')
        )
        if candidates:
            return candidates[-1]
    elif os.name == 'nt':
        candidates = []
        for root in [
            os.environ.get('ProgramFiles', r'C:\\Program Files'),
            os.environ.get('ProgramFiles(x86)', r'C:\\Program Files (x86)')
        ]:
            if root:
                candidates.extend(glob.glob(os.path.join(root, 'ParaView*', 'bin', 'paraview.exe')))
        if candidates:
            candidates.sort()
            return candidates[-1]
        which = shutil.which('paraview.exe')
        if which:
            return which
    else:
        for p in ('/usr/bin/paraview', '/snap/bin/paraview', '/opt/paraview/bin/paraview'):
            if os.path.isfile(p):
                return p

    raise RuntimeError(
        "ParaView executable not found. Install ParaView or provide paraview_path explicitly."
    )


def open_in_paraview(
    state_or_vti_path: Optional[str] = None,
    *,
    volume: Optional[np.ndarray] = None,
    spacing: Tuple[float, float, float] = (1.0, 1.0, 1.0),
    origin: Tuple[float, float, float] = (0.0, 0.0, 0.0),
    scalar_name: str = 'scalars',
    data_order: str = 'xyz',
    cast: Optional[str] = None,
    compress: bool = True,
    paraview_path: Optional[str] = None,
    block: bool = False,
) -> None:
    """
    Open a ParaView state file (.pvsm) or dataset (.vti). If a volume is provided,
    it will be exported via export_vti and then opened.

    Parameters
    ----------
    state_or_vti_path : str, optional
        Path to a .pvsm (state) or .vti (dataset) file. If None, a volume must be provided.
    volume : np.ndarray, optional
        3D array to export-and-open if no file path is given.
    spacing, origin, scalar_name, data_order, cast, compress
        Parameters forwarded to export_vti when exporting a provided volume.
    paraview_path : str, optional
        Explicit path to the ParaView executable. If not provided, auto-detection is used.
    block : bool, default False
        If True, wait for the ParaView process to exit; otherwise return immediately.
    """
    from .writers import export_vti  # local import to avoid circular dependency
    from drp_template.default_params import check_output_folder

    # Resolve target file
    vti_to_open: Optional[str] = None
    if state_or_vti_path is None and volume is None:
        raise ValueError("Either state_or_vti_path or volume must be provided.")

    if volume is not None:
        # If no path given, create a timestamped output in standard folder
        if state_or_vti_path is None:
            out_dir = check_output_folder()
            from datetime import datetime
            ts = datetime.now().strftime('%Y%m%d_%H%M%S')
            state_or_vti_path = os.path.join(out_dir, f'volume_{ts}.vti')
        vti_to_open = export_vti(
            volume=volume,
            path=state_or_vti_path,
            spacing=spacing,
            origin=origin,
            scalar_name=scalar_name,
            data_order=data_order,
            cast=cast,
            compress=compress,
            log=True,
        )
    else:
        # Validate existence
        if not os.path.isfile(state_or_vti_path):
            raise FileNotFoundError(f"File not found: {state_or_vti_path}")
        vti_to_open = state_or_vti_path

    # Determine what to open
    open_target = vti_to_open
    base, ext = os.path.splitext(state_or_vti_path)
    if ext.lower() == '.pvsm':
        open_target = state_or_vti_path

    # Find ParaView executable
    exe = _find_paraview_executable(paraview_path)

    # Launch
    if block:
        subprocess.run([exe, open_target], check=False)
    else:
        subprocess.Popen([exe, open_target])
