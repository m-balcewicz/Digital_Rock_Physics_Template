import numpy as np
from control_data import check_binary
import import_export_data as ie
from show_data import visualize_plane
import struct
import os
import tifffile

path_in = '/Volumes/mbalcewicz/SCIENCE_WORLD/STUDIES/2023_PYTHON_POROSITY/PerGeos/PerGeos_EXPORT'
path_out = '/Volumes/mbalcewicz/SCIENCE_WORLD/STUDIES/2023_PYTHON_POROSITY/PYTHON/PYTHON_EXPORT'
data_raw = ie.import_raw(f'{path_in}/100cube.raw', dimension=100)


slice_no = 49  # This is a characteristic 2D within the 3D volume
fig_data_1_12_100cube_xy = visualize_plane(data_raw, type=2, slice=slice_no, title='XY', plane='xy')
fig_data_1_12_100cube_xy.show()
fig_data_1_12_100cube_xy = visualize_plane(data_raw, type=2, slice=slice_no, title=f'XZ', plane='xz')
fig_data_1_12_100cube_xy.show()
fig_data_1_12_100cube_xy = visualize_plane(data_raw, type=2, slice=slice_no, title='YZ', plane='yz')
fig_data_1_12_100cube_xy.show()

# ie.export_raw(data_raw, path=path_out, varname='export_raw')
# ie.export_3d_tif(data_raw, path=path_out, varname='export_tif')
# ie.export_2d_tif(data_raw, path=path_out, varname='export_data')
