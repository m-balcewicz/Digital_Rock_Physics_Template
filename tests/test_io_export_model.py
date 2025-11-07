import os
import numpy as np

import drp_template.io as io
from drp_template.default_params import read_parameters_file
from drp_template.model import binary_3d


def test_export_model_creates_raw_and_params(tmp_path):
    """Ensure export_model writes raw file and parameters JSON with expected metadata."""
    # Create model - using inverted values to show solid inclusions in pore matrix
    data = binary_3d(
        nx=150, ny=150, nz=150,
        num_inclusions=15,
        inclusion_radius=12,
        inclusion_aspect_ratio=1.5,  # Prolate ellipsoid (elongated)
        orientation='xy',
        random_orientation=True,  # Random rotations
        background_value=0,  # Pore space
        inclusion_value=1,   # Solid grains
        dtype='uint8',
        seed=123
    )
    voxel_size = 5.0

    print(f"Created model with shape: {data.shape}")
    print(f"Unique values: {np.unique(data)}")

    cwd = os.getcwd()
    os.chdir(tmp_path)
    try:
        io.export_model(
            filename='unit_test_sample',
            data=data,
            voxel_size=voxel_size,
            dtype='uint8',
            labels={0: 'Pore', 1: 'Solid'},
            paramsfile='parameters.json',
            ensure_unique_params=False,
            order='C'
        )

        assert os.path.isdir('output'), "output directory should be created"

        raw_path = os.path.join('output', 'unit_test_sample.raw')
        # The JSON name may be 'parameters.json' or numbered 'parameters_#.json'
        json_candidates = [
            os.path.join('output', 'parameters.json'),
        ] + [os.path.join('output', f'parameters_{i}.json') for i in range(1, 6)]
        json_path = next((p for p in json_candidates if os.path.isfile(p)), None)
        assert os.path.isfile(raw_path), "raw file should exist"
        assert json_path is not None, "parameters json should exist (parameters.json or numbered variant)"

        # Read whichever parameters file exists
        params = read_parameters_file(paramsfile=os.path.basename(json_path))
        for key in [
            'schema_version', 'generator', 'modified_at', 'file_path', 'file_format',
            'dtype', 'endian', 'nx', 'ny', 'nz', 'voxel_size', 'file_size_bytes'
        ]:
            assert key in params, f"Missing expected parameter key: {key}"

        assert params['nx'] == 150 and params['ny'] == 150 and params['nz'] == 150
        assert abs(params['voxel_size'] - voxel_size) < 1e-9

        assert 'labels' in params
        assert params['labels']['0'] == 'Pore'
        assert params['labels']['1'] == 'Solid'

    finally:
        os.chdir(cwd)
        
if __name__ == "__main__":
    test_export_model_creates_raw_and_params(tmp_path=os.getcwd())
