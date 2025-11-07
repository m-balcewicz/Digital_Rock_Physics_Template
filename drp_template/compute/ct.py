"""
CT Geometry Calculations
=======================

Functions for geometric calculations in X-ray computed tomography (CT),
including magnification, voxel size, spatial resolution, and sample projection checks.

SI Units Standard
-----------------
All inputs and outputs use SI base units (meters). This is the package-wide convention
for scientific computations. If your instrument parameters are provided in millimeters
or micrometers, convert them to meters before calling these functions (e.g., mm → m: /1e3,
µm → m: /1e6). Example conversions:

- 26 mm → 0.026 m
- 127 µm → 127e-6 m

Author: Martin Balcewicz (martin.balcewicz@rockphysics.org)

References
----------
- Basic CT geometry: https://en.wikipedia.org/wiki/X-ray_computed_tomography

"""

def ct_geometry(SOD, SDD, detector_pixel_size, focal_spot_size, sample_diameter, detector_width):
    """
    Compute CT geometric magnification, voxel size, spatial resolution, and projected sample diameter.

    Parameters
    ----------
    SOD : float
        Source-to-object distance (m)
    SDD : float
        Source-to-detector distance (m)
    detector_pixel_size : float
        Physical size of detector pixel (m)
    focal_spot_size : float
        X-ray source focal spot size (m)
    sample_diameter : float
        Diameter of the sample (m)
    detector_width : float
        Width of the detector (m)

    Returns
    -------
    dict
        Dictionary with keys:
        - 'geometric_magnification': float
        - 'voxel_size_m': float (voxel size in meters)
        - 'spatial_resolution_m': float (estimated spatial resolution in meters)
        - 'projected_sample_diameter_m': float
    Raises
    ------
    ValueError
        If the projected sample diameter exceeds the detector width.
    """
    geometric_magnification = SDD / SOD
    projected_sample_diameter = sample_diameter * geometric_magnification
    if projected_sample_diameter > detector_width:
        raise ValueError("Sample projection exceeds detector width. Adjust SOD or sample size.")
    voxel_size = detector_pixel_size / geometric_magnification
    effective_focal_spot = focal_spot_size * (1 / geometric_magnification)
    spatial_resolution = max(voxel_size, effective_focal_spot)
    return {
        "geometric_magnification": geometric_magnification,
        "voxel_size_m": voxel_size,
        "spatial_resolution_m": spatial_resolution,
        "projected_sample_diameter_m": projected_sample_diameter,
    }
