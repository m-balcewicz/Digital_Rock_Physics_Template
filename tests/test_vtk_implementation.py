"""
Simple script: generate a centered sphere volume and export to VTI.

Usage (inside your conda env):
  python tests/test_vtk_implementation.py --nx 100 --radius 20 --spacing-mm 1.0 --open

Notes:
- Spacing/origin use SI units (meters) in the exporter; spacing-mm is converted to meters.
- Pass --open to attempt launching ParaView (non-blocking). Supply a custom path with --paraview-path.
"""

import os
import sys
import json
import argparse
import numpy as np

from drp_template.model import binary_3d
from drp_template.io import export_vti, open_in_paraview


def main():
    parser = argparse.ArgumentParser(description="Generate centered sphere and export to VTI")
    parser.add_argument("--nx", type=int, default=100, help="Grid size in x (nx=ny=nz)")
    parser.add_argument("--radius", type=float, default=20, help="Sphere radius (voxels)")
    parser.add_argument("--spacing-mm", type=float, default=1.0, help="Voxel spacing in mm (applied to x,y,z)")
    parser.add_argument("--origin-m", type=float, nargs=3, default=(0.0, 0.0, 0.0), help="Origin in meters (x0 y0 z0)")
    parser.add_argument("--scalar-name", type=str, default="phases", help="Scalar name in VTK")
    parser.add_argument("--out", type=str, default=None, help="Output .vti path (defaults to timestamped file in output/)")
    parser.add_argument("--open", action="store_true", help="Try to open result in ParaView (non-blocking)")
    parser.add_argument("--paraview-path", type=str, default=None, help="Explicit path to ParaView executable")
    args = parser.parse_args()

    nx = ny = nz = int(args.nx)
    center_position = np.array([[nx // 2, ny // 2, nz // 2]])

    # Create model
    data = binary_3d(
        nx=nx, ny=ny, nz=nz,
        num_inclusions=1,
        inclusion_radius=float(args.radius),
        inclusion_aspect_ratio=1.0,
        orientation='zx',
        random_orientation=False,
        dtype='uint8',
        positions=center_position,
    )

    print(f"Created model with shape: {data.shape}")
    uniq = np.unique(data)
    print(f"Unique values: {uniq}")
    print(f"Center position: {center_position[0]}")

    # Export (convert spacing from mm to meters)
    s = float(args.spacing_mm) * 1e-3
    origin = tuple(float(x) for x in args.origin_m)

    vti_path = export_vti(
        volume=data,
        path=args.out,
        spacing=(s, s, s),
        origin=origin,
        scalar_name=args.scalar_name,
        data_order='xyz',
        cast=None,
        compress=False,
        log=True,
    )

    json_path = vti_path.replace('.vti', '.json')
    print(f"Sidecar JSON: {json_path}")
    if os.path.isfile(json_path):
        with open(json_path, 'r', encoding='utf-8') as f:
            meta = json.load(f)
        print("Metadata summary:")
        print(json.dumps({
            'file': meta.get('file'),
            'shape_xyz': meta.get('shape_xyz'),
            'spacing_m': meta.get('spacing_m'),
            'origin_m': meta.get('origin_m'),
            'scalar_name': meta.get('scalar_name'),
            'format': meta.get('format'),
        }, indent=2))

    if args.open:
        try:
            open_in_paraview(state_or_vti_path=vti_path, paraview_path=args.paraview_path, block=False)
            print("ParaView launch requested (non-blocking).")
        except Exception as e:
            print(f"Could not launch ParaView: {e}")


if __name__ == "__main__":
    sys.exit(main())
