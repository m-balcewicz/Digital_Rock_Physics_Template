import os
from tools.drp_template import import_export as ie
from tools.drp_template import plot_slice
from tools.drp_template.import_export import import_csv

path_in = '/Users/martin/Library/Mobile Documents/com~apple~CloudDocs/MYDATA/SCIENCE_WORLD/STUDIES/2023_Wave_Attenuation_in_Concrete/concrete_sample_AB16_3pcntAir.raw'
# path_out = '/Volumes/mbalcewicz/SCIENCE_WORLD/STUDIES/2023_PYTHON_POROSITY/PYTHON/PYTHON_EXPORT'
# data_raw = ie.import_raw(os.path.join(path_in, '100cube_raw.raw'), dimension=100, dtype='uint8')
z_size = 800
y_size = 200
x_size = 200

dim =[z_size, y_size, x_size]
data_binary = import_csv(path_in, dim)

slice_no = 400  # This is a characteristic 2D within the 3D volume
# fig_data_1_12_100cube_xy = plot_slice(data_raw, slice=slice_no, plane='xy', title='XY')
# fig_data_1_12_100cube_xy.show()
fig_data_1_12_100cube_xy = plot_slice(data_binary, slice=slice_no, plane='xy', title='XY')
fig_data_1_12_100cube_xy.show()