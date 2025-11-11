import numpy as np
from typing import Optional, Union, Iterable

Array2DPositions = Union[np.ndarray, Iterable[Iterable[float]]]
Array3DPositions = Union[np.ndarray, Iterable[Iterable[float]]]

__all__ = [
    'binary_2d',
    'binary_3d',
    'binary_vti',
]


def binary_2d(nx: int, ny: int,
                           num_inclusions: int = 1,
                           inclusion_radius: float = 10,
                           inclusion_aspect_ratio: float = 1.0,
                           random_orientation: bool = False,
                           background_value: int = 1,
                           inclusion_value: int = 0,
                           dtype: Union[str, np.dtype] = 'uint8',
                           seed: Optional[int] = None,
                           positions: Optional[Array2DPositions] = None,
                           periodic: bool = False) -> np.ndarray:
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


def binary_3d(nx: int, ny: int, nz: int,
                           num_inclusions: int = 1,
                           inclusion_radius: float = 10,
                           inclusion_aspect_ratio: float = 1.0,
                           orientation: str = 'xy',
                           random_orientation: bool = False,
                           background_value: int = 1,
                           inclusion_value: int = 0,
                           dtype: Union[str, np.dtype] = 'uint8',
                           seed: Optional[int] = None,
                           positions: Optional[Array3DPositions] = None,
                           periodic: bool = False) -> np.ndarray:
    """
    Create a 3D binary model with ellipsoidal inclusions in a homogeneous background.
    
    This function generates a 3D volume with ellipsoidal inclusions (pores, phase 0) 
    placed within a homogeneous background (solid, phase 1). Perfect for true 3D digital 
    rock physics models with full 3D orientation control.
    
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
    
    Notes
    -----
    - Inclusions are placed randomly within the volume
    - Overlapping inclusions are allowed (union behavior)
    - Returned array uses package standard shape (nx, ny, nz)
    - Default values represent digital rock physics convention: 
      solid matrix (1) with pore inclusions (0)
    - When random_orientation=True, uses true 3D rotation (Euler angles)
    - With periodic=True, inclusions can wrap to up to 27 locations (1 original + 
      6 face-adjacent + 12 edge-adjacent + 8 corner-adjacent)
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
    
    return volume


def _make_ellipse_mask_2d(nx: int, ny: int, pos_x: float, pos_y: float, radius: float, aspect_ratio: float, random_rotation: bool) -> np.ndarray:
    """
    Internal helper to create a 2D ellipse mask.
    
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


def _make_ellipsoid_mask(nx: int, ny: int, nz: int, pos_x: float, pos_y: float, pos_z: float, 
                         radius: float, aspect_ratio: float, orientation: str, random_rotation: bool) -> np.ndarray:
    """
    Internal helper to create an ellipsoid mask.
    
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
        alpha = np.random.uniform(0, 2 * np.pi)  # Rotation around Z
        beta = np.random.uniform(0, np.pi)        # Rotation around Y (inclination)
        gamma = np.random.uniform(0, 2 * np.pi)  # Rotation around X
        
        # Build 3D rotation matrix (ZYX Euler angles)
        Rz = np.array([
            [np.cos(alpha), -np.sin(alpha), 0],
            [np.sin(alpha), np.cos(alpha), 0],
            [0, 0, 1]
        ])
        
        Ry = np.array([
            [np.cos(beta), 0, np.sin(beta)],
            [0, 1, 0],
            [-np.sin(beta), 0, np.cos(beta)]
        ])
        
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
        if aspect_ratio != 1.0:
            # Z is the "special" axis
            mask = ((x_rot**2 / radius**2) + 
                    (y_rot**2 / radius**2) + 
                    (z_rot**2 / (aspect_ratio * radius)**2)) <= 1
        else:
            # Sphere
            mask = ((x_rot**2 / radius**2) + 
                    (y_rot**2 / radius**2) + 
                    (z_rot**2 / radius**2)) <= 1
    else:
        # NO ROTATION: Use fixed orientation based on 'orientation'
        if orientation == 'xy':
            mask = ((x_full**2 / radius**2) + 
                    (y_full**2 / radius**2) + 
                    (z_full**2 / (aspect_ratio * radius)**2)) <= 1
        elif orientation == 'zx':
            mask = ((z_full**2 / radius**2) + 
                    (x_full**2 / radius**2) + 
                    (y_full**2 / (aspect_ratio * radius)**2)) <= 1
        elif orientation == 'zy':
            mask = ((z_full**2 / radius**2) + 
                    (y_full**2 / radius**2) + 
                    (x_full**2 / (aspect_ratio * radius)**2)) <= 1
        else:
            raise ValueError("orientation must be 'xy', 'zx', or 'zy'")
    
    return mask


def binary_vti(
    nx: int,
    ny: int,
    nz: int,
    layer_thicknesses: Iterable[float],
    phase_sequence: Optional[Iterable[int]] = None,
    num_phases: Optional[int] = None,
    dtype: Union[str, np.dtype] = 'uint8',
    repeat_pattern: bool = True,
    scale_to_nz: bool = False,
    start_phase: int = 1,
    num_cycles: Optional[int] = None,
    return_metadata: bool = False,
):
    """Generate a vertically layered (VTI) binary model with optional cycle control.

    Creates horizontal layers (perpendicular to z) suitable for Backus averaging
    and anisotropy studies. Supports three modes:

    1. Repeating pattern (repeat_pattern=True):
       The provided thickness sequence is cycled until nz is filled.
       Use for fine-scale layering (Backus regime: many thin layers).

    2. Exact number of cycles (num_cycles specified):
       Repeat the layer pattern exactly num_cycles times, scaling if needed to fit nz.
       Useful when you need precise control over the number of layer repetitions.

    3. Single scaled stack (scale_to_nz=True):
       The thickness ratios are preserved but scaled so the sequence occurs once
       and fills nz exactly (macroscopic two-/multi-layer model).

    Parameters
    ----------
    nx, ny, nz : int
        Volume dimensions.
    layer_thicknesses : iterable of float
        Thickness for each layer in *pattern units* (can be fractional). Example: [0.75, 0.50].
    phase_sequence : iterable of int, optional
        Phase IDs for each thickness. Must match length of layer_thicknesses.
        If None, auto-generated using num_phases (alternating) starting at start_phase.
    num_phases : int, optional
        Number of phases if phase_sequence not supplied. Required when phase_sequence=None.
    dtype : numpy dtype or str, optional
        Output array dtype (default 'uint8').
    repeat_pattern : bool, optional (default True)
        Repeat the pattern until nz is filled. Ignored if scale_to_nz=True or num_cycles is set.
    scale_to_nz : bool, optional (default False)
        Scale thicknesses so they sum to nz exactly (one occurrence). Overrides repeat_pattern.
    start_phase : int, optional (default 1)
        Starting phase index for auto-generated sequences.
    num_cycles : int, optional
        Exact number of complete cycles to generate. When set, the layer pattern is scaled
        to fit exactly this many repetitions into nz. Overrides repeat_pattern but not scale_to_nz.
        Useful for reproducible models: num_cycles=10 always produces 10 complete layer sequences.
    return_metadata : bool, optional (default False)
        If True, return a tuple (volume, metadata) where metadata is a dict containing:
        - 'num_cycles_actual': Actual number of complete cycles generated
        - 'num_cycles_partial': Fractional part of final incomplete cycle (0.0 to 1.0)
        - 'total_layers': Total number of individual layers placed
        - 'pattern_length': Number of layers in one cycle (len of layer_thicknesses)
        - 'layer_thicknesses_voxels': Actual voxel thickness per layer in final model
        - 'mode': 'scaled' (scale_to_nz), 'cycled' (num_cycles), or 'repeated' (repeat_pattern)

    Returns
    -------
    numpy.ndarray or tuple
        If return_metadata=False: 3D array of shape (nx, ny, nz) with layered phase indices.
        If return_metadata=True: (volume, metadata_dict) tuple.

    Notes
    -----
    - Fractional thicknesses are accumulated in floating point and rounded only
      when converting to voxel indices (minimizes drift).
    - If rounding causes a gap at the top, remaining voxels are filled with the
      last phase to ensure full coverage.
    - For Backus averaging consistency, choose many thin layers (repeat_pattern)
      or a single scaled stack (scale_to_nz) depending on analysis scale.
    - The metadata dict is JSON-serializable and suitable for storing in parameter files.

    Examples
    --------
    >>> # Fine layering (many cycles) preserving 60:40 ratio
    >>> m = binary_vti(200, 200, 400, [0.75, 0.50], phase_sequence=[1, 2], repeat_pattern=True)
    >>> # Single two-layer model (scaled to nz)
    >>> m2 = binary_vti(200, 200, 400, [0.75, 0.50], phase_sequence=[1, 2], scale_to_nz=True)
    >>> # Exactly 10 cycles of the pattern, scaled to fit nz
    >>> m3, meta = binary_vti(200, 200, 400, [0.75, 0.50], phase_sequence=[1, 2], 
    ...                       num_cycles=10, return_metadata=True)
    >>> print(f"Generated {meta['num_cycles_actual']} complete cycles")
    >>> # Auto-generate sequence for 3 thickness entries and 2 phases
    >>> m4 = binary_vti(100, 100, 150, [10, 5, 8], num_phases=2)

    """
    # Convert to arrays
    layer_thicknesses = np.asarray(layer_thicknesses, dtype=float)
    if layer_thicknesses.ndim != 1 or layer_thicknesses.size == 0:
        raise ValueError("layer_thicknesses must be a non-empty 1D sequence")
    if np.any(layer_thicknesses <= 0):
        raise ValueError("All layer thicknesses must be positive")

    # Phase sequence handling
    if phase_sequence is None:
        if num_phases is None:
            raise ValueError("Provide phase_sequence or num_phases for auto-generation")
        n_layers = layer_thicknesses.size
        phase_sequence = [start_phase + (i % num_phases) for i in range(n_layers)]
    phase_sequence = np.asarray(phase_sequence, dtype=int)
    if phase_sequence.size != layer_thicknesses.size:
        raise ValueError("phase_sequence length must match layer_thicknesses length")
    if not np.all(phase_sequence >= start_phase):
        raise ValueError("Phase values must be >= start_phase")

    # Scaling mode
    mode = 'repeated'  # default
    if scale_to_nz:
        mode = 'scaled'
        total = layer_thicknesses.sum()
        if total <= 0:
            raise ValueError("Total thickness must be > 0 for scaling")
        factor = nz / total
        layer_thicknesses = layer_thicknesses * factor
        repeat_pattern = False  # override - single stack
    elif num_cycles is not None:
        # Exact number of cycles mode
        mode = 'cycled'
        if num_cycles <= 0:
            raise ValueError("num_cycles must be positive")
        total = layer_thicknesses.sum()
        if total <= 0:
            raise ValueError("Total thickness must be > 0 for cycling")
        # Scale to fit exactly num_cycles repetitions into nz
        factor = nz / (num_cycles * total)
        layer_thicknesses = layer_thicknesses * factor
        repeat_pattern = True  # will repeat exactly num_cycles times

    # Prepare volume
    volume = np.zeros((nx, ny, nz), dtype=dtype)

    current_z: float = 0.0
    layer_idx = 0
    n_layers = layer_thicknesses.size
    last_end = 0
    total_layers_placed = 0
    cycles_completed = 0
    pattern_sum = layer_thicknesses.sum()

    while current_z < nz:
        thickness = layer_thicknesses[layer_idx]
        phase = phase_sequence[layer_idx]
        z_start = int(round(current_z))
        z_end = int(round(current_z + thickness))
        if z_end <= z_start:
            z_end = z_start + 1  # guarantee at least one voxel
        if z_start >= nz:
            break
        if z_end > nz:
            z_end = nz
        volume[:, :, z_start:z_end] = phase
        last_end = z_end
        total_layers_placed += 1
        current_z += thickness
        
        # Track cycles
        prev_idx = layer_idx
        if repeat_pattern:
            layer_idx = (layer_idx + 1) % n_layers
            # Cycle completed when we wrap around
            if layer_idx < prev_idx:
                cycles_completed += 1
        else:
            layer_idx = min(layer_idx + 1, n_layers - 1)

        # Stop early logic for num_cycles mode
        if num_cycles is not None and cycles_completed >= num_cycles:
            break

        # Stop early logic retained (placeholder for potential optimization)
        if not repeat_pattern and layer_idx == n_layers - 1 and current_z >= layer_thicknesses[:-1].sum():
            pass

    # Fill any residual gap (due to rounding) with last phase
    if last_end < nz:
        volume[:, :, last_end:nz] = phase_sequence[-1]

    # Calculate partial cycle (fractional part of incomplete final cycle)
    partial_cycle = 0.0
    if repeat_pattern and cycles_completed > 0:
        # Estimate how far into the next cycle we got
        z_used_by_complete = cycles_completed * pattern_sum
        if current_z > z_used_by_complete:
            partial_cycle = (current_z - z_used_by_complete) / pattern_sum
            partial_cycle = min(max(partial_cycle, 0.0), 1.0)  # clamp [0,1]
    
    # Build metadata
    metadata = {
        'num_cycles_actual': int(cycles_completed),
        'num_cycles_partial': float(partial_cycle),
        'total_layers': int(total_layers_placed),
        'pattern_length': int(n_layers),
        'layer_thicknesses_voxels': layer_thicknesses.tolist(),
        'mode': mode,
        'nz': int(nz),
        'phase_sequence': phase_sequence.tolist(),
    }
    
    if return_metadata:
        return volume, metadata
    else:
        return volume
