"""
Data Writers
============

Functions for exporting digital rock models to various file formats.

This module provides writers for:
- Raw binary files with parameter JSON metadata (export_model)
- SEPlib header files (export_header)

All writers automatically:
- Create validated parameter JSON files
- Include comprehensive metadata (dimensions, voxel size, labels, etc.)
- Calculate and store file sizes

Functions
---------
- export_model: Write model data to binary file with parameters JSON
- export_header: Write SEPlib header file for data
- export_vti: Write VTK ImageData (.vti) with sidecar JSON metadata
"""

import os
import json
from datetime import datetime
import numpy as np

from drp_template.default_params import update_parameters_file, check_output_folder, print_style
from .utils import reorient_volume

try:
    import vtk  # type: ignore
    from vtk.util import numpy_support  # type: ignore
except Exception:  # pragma: no cover - optional dependency
    vtk = None
    numpy_support = None

__all__ = [
    'export_model',
    'export_header',
    'export_vti',
]


def _ensure_vtk():
    if vtk is None or numpy_support is None:
        raise ImportError(
            "VTK is required for this operation. Install with `pip install vtk` or add it to requirements.txt."
        )


_VTK_DTYPE_MAP = {
    np.dtype('uint8'): 'VTK_UNSIGNED_CHAR',
    np.dtype('int8'): 'VTK_CHAR',
    np.dtype('uint16'): 'VTK_UNSIGNED_SHORT',
    np.dtype('int16'): 'VTK_SHORT',
    np.dtype('uint32'): 'VTK_UNSIGNED_INT',
    np.dtype('int32'): 'VTK_INT',
    np.dtype('float32'): 'VTK_FLOAT',
    np.dtype('float64'): 'VTK_DOUBLE',
}


def export_model(filename, data, voxel_size, dtype='uint8', order='F', filetype='.raw', labels=None, paramsfile: str = 'parameters.json', ensure_unique_params: bool = True):
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
        Data type for output (default: 'uint8').
    order : str, optional
        Memory layout: 'F' (Fortran/column-major) or 'C' (C/row-major). Default is 'F'.
    filetype : str, optional
        File extension (default: '.raw').
    labels : dict, optional
        Dictionary mapping phase values to phase names, e.g., {0: 'Pore', 1: 'Solid'}.
        If provided, will be saved to the parameters JSON file.

    Returns
    -------
    None
    
    Raises
    ------
    ValueError
        If voxel_size is None, not provided, or data dimensionality is invalid.
    
    Notes
    -----
    This function automatically creates a validated parameters JSON file with:
    - Schema version and provenance (generator, created_at, modified_at)
    - File path, format, dtype, endianness
    - Dimensions (nx, ny, nz for 3D or nx, ny, nz, dim for 4D)
    - Voxel size (required)
    - Labels (optional, if provided)
    - File size in bytes and MB
    
    Input data should follow the package standard: (nx, ny, nz) for 3D arrays.
    The raw file is written with the same axis order.
    
    Examples
    --------
    ```python
    import drp_template.io as io
    import numpy as np
    
    # Create sample data
    data = np.random.randint(0, 2, (100, 100, 100), dtype=np.uint8)
    
    # Export with labels
    io.export_model(
        filename='binary_sample',
        data=data,
        voxel_size=5.0,
        dtype='uint8',
        labels={0: 'Pore', 1: 'Solid'}
    )
    ```
    """
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
    print_style(f"data saved: {file_path}")
    
    # Determine parameters filename: user override OR derive from filename OR default 'parameters.json'
    # If user passed the default 'parameters.json', we permit uniqueness handling to avoid overwrites.
    if paramsfile == 'parameters.json':
        from .utils import resolve_params_filename
        params_filename = resolve_params_filename(paramsfile=paramsfile, ensure_unique=ensure_unique_params)
    else:
        # Use user-specified name directly (no automatic uniqueness unless they opt-in via ensure_unique_params)
        if ensure_unique_params:
            from .utils import resolve_params_filename
            params_filename = resolve_params_filename(paramsfile=paramsfile, ensure_unique=True)
        else:
            params_filename = paramsfile
    
    # Determine endianness from order
    endian = 'little' if order == 'C' else 'big'
    
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
    
    # Write labels if provided
    if labels is not None:
        update_parameters_file(paramsfile=params_filename, labels=labels)
    
    # Add file size metadata
    try:
        size_bytes = os.path.getsize(file_path)
        update_parameters_file(paramsfile=params_filename, file_size_bytes=int(size_bytes))
        update_parameters_file(paramsfile=params_filename, file_size_mb=round(size_bytes / (1024 * 1024), 2))
    except Exception:
        pass
    
    print_style(f"parameters saved: {os.path.join(output_path, params_filename)}")


def export_vti(
    volume: np.ndarray,
    path: str | None = None,
    *,
    spacing: tuple[float, float, float] = (1.0, 1.0, 1.0),
    origin: tuple[float, float, float] = (0.0, 0.0, 0.0),
    scalar_name: str = 'scalars',
    data_order: str = 'xyz',
    cast: str | None = None,
    compress: bool = True,
    log: bool = True,
) -> str:
    """
    Export a 3D numpy array as VTK ImageData (.vti) with sidecar JSON metadata.

    Parameters
    ----------
    volume : np.ndarray
        3D array with shape (nx, ny, nz) by default.
    path : str, optional
        Output file path. If None, a timestamped file is written into the
        standard output directory.
    spacing : tuple of float, default (1.0, 1.0, 1.0)
        Voxel spacing in meters (dx, dy, dz).
    origin : tuple of float, default (0.0, 0.0, 0.0)
        Volume origin in meters (x0, y0, z0).
    scalar_name : str, default 'scalars'
        Name for the scalar array in VTK.
    data_order : {'xyz','zyx'}, default 'xyz'
        Interpret input array axes. 'xyz' means (nx, ny, nz). 'zyx' will be
        transposed to VTK's (x, y, z) before writing.
    cast : str, optional
        If provided, cast the data to this dtype before export. Options:
        'uint8','uint16','float32','float64'.
    compress : bool, default True
        Enable zlib compression if available.
    log : bool, default True
        Print an informational message with the saved paths.

    Returns
    -------
    str
        Absolute path to the written .vti file.
    """
    _ensure_vtk()

    # Determine output path
    if path is None:
        out_dir = check_output_folder()
        ts = datetime.now().strftime('%Y%m%d_%H%M%S')
        path = os.path.join(out_dir, f'volume_{ts}.vti')

    # Ensure extension
    base, ext = os.path.splitext(path)
    if ext.lower() != '.vti':
        vti_path = base + '.vti'
    else:
        vti_path = path
        base = base  # unchanged

    # Normalize data order: only standard 'xyz' is supported (legacy removed)
    order = data_order.lower()
    if order != 'xyz':
        raise ValueError("data_order must be 'xyz'. Normalize your array before export.")
    vol_xyz = volume

    # Optional casting
    if cast is not None:
        cast_map = {
            'uint8': np.uint8,
            'uint16': np.uint16,
            'float32': np.float32,
            'float64': np.float64,
        }
        if cast not in cast_map:
            raise ValueError("Unsupported cast dtype. Use one of: 'uint8','uint16','float32','float64'")
        vol_xyz = vol_xyz.astype(cast_map[cast], copy=False)

    # Validate dtype
    dtype = vol_xyz.dtype
    if dtype not in _VTK_DTYPE_MAP:
        raise TypeError(
            f"Unsupported dtype {dtype}. Cast to one of {list(_VTK_DTYPE_MAP.keys())} via cast=..."
        )

    # Build VTK image
    nx, ny, nz = vol_xyz.shape
    vtk_data = numpy_support.numpy_to_vtk(
        num_array=vol_xyz.ravel(order='F'),
        deep=True,
        array_type=getattr(vtk, _VTK_DTYPE_MAP[dtype])
    )
    vtk_data.SetName(scalar_name)

    image = vtk.vtkImageData()
    image.SetDimensions(nx, ny, nz)
    image.SetSpacing(float(spacing[0]), float(spacing[1]), float(spacing[2]))
    image.SetOrigin(float(origin[0]), float(origin[1]), float(origin[2]))
    image.GetPointData().SetScalars(vtk_data)

    writer = vtk.vtkXMLImageDataWriter()
    writer.SetFileName(os.path.abspath(vti_path))
    writer.SetInputData(image)
    if compress:
        try:
            comp = vtk.vtkZLibDataCompressor()
            writer.SetCompressor(comp)
        except Exception:
            pass  # compression optional
    writer.Write()

    # Sidecar JSON metadata (SI units)
    meta = {
        'file': os.path.abspath(vti_path),
        'created': datetime.now().isoformat(),
        'shape_xyz': [int(nx), int(ny), int(nz)],
        'dtype': str(dtype),
        'spacing_m': [float(spacing[0]), float(spacing[1]), float(spacing[2])],
        'origin_m': [float(origin[0]), float(origin[1]), float(origin[2])],
        'scalar_name': scalar_name,
        'data_order_input': data_order,
        'compress': bool(compress),
        'format': 'vti',
        'software': 'drp_template',
    }
    json_path = base + '.json'
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(meta, f, indent=2)

    if log:
        print_style(f"Saved VTI: {os.path.abspath(vti_path)}\nSaved JSON: {os.path.abspath(json_path)}")

    return os.path.abspath(vti_path)


def export_header(filename, data):
    """
    Write a SEPlib header file for the given data.
    
    SEPlib is a file format commonly used in seismic processing and imaging.
    This function creates a simple header file describing the data dimensions.

    Parameters
    ----------
    filename : str
        Output file name (without extension).
    data : np.ndarray
        Data array (3D or 4D).

    Returns
    -------
    None
    
    Raises
    ------
    ValueError
        If data is not 3D or 4D.
    
    Notes
    -----
    The header file format is:
    - Sets the data file name
    - Includes n1, n2, n3, n4 dimensions
    - n4 defaults to 1 for 3D arrays
    
    Examples
    --------
    ```python
    import drp_template.io as io
    import numpy as np
    
    # Create sample data
    data = np.random.rand(100, 100, 100)
    
    # Export SEPlib header
    io.export_header('sample', data)
    # Creates 'sampleheader' file
    ```
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
    print_style(f"header saved: {filename}")
