import os

import numpy as np
from drp_template.drp_template import import_export as ie
from drp_template.drp_template import plot_slice

path_in = '/Volumes/files/mbalcewicz/SCIENCE_WORLD/STUDIES/2023_PYTHON_POROSITY/PerGeos/PerGeos_EXPORT'
path_out = '/Volumes/mbalcewicz/SCIENCE_WORLD/STUDIES/2023_PYTHON_POROSITY/PYTHON/PYTHON_EXPORT'
data_raw = ie.import_raw(os.path.join(path_in, '100cube_raw.raw'), dimension=100, dtype='uint8')
data_binary = ie.import_raw(os.path.join(path_in, '100cube_binary.raw'), dimension=100, dtype='uint8')

slice_no = 49  # This is a characteristic 2D within the 3D volume
fig_data_1_12_100cube_xy = plot_slice(data_raw, slice=slice_no, plane='xy', title='XY')
fig_data_1_12_100cube_xy.show()
fig_data_1_12_100cube_xy = plot_slice(data_binary, slice=slice_no, plane='xy', title='XY')
fig_data_1_12_100cube_xy.show()

# extract pore space
set_pore = 0
im_pore = np.where(data_binary == set_pore, set_pore, -1)
im_pore = np.where(im_pore == set_pore, 1, im_pore)
im_pore = np.where(im_pore == -1, 0, im_pore)

fig_data_pore_xy = plot_slice(im_pore, slice=slice_no, plane='xy', title='XY')
fig_data_pore_xy.show()


ie.export_raw(im_pore, path=None, filename='im_pore', dtype='uint8', endian='little')
# ie.export_3d_tif(data_raw, path=path_out, varname='export_tif')
# ie.export_2d_tif(data_raw, path=path_out, varname='export_data')
