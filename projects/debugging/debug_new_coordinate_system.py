# New Python script

import sys
sys.path.append('/Users/martin/Library/Mobile Documents/com~apple~CloudDocs/MYDATA/CODING_WORLD/PYTHON_WORLD/Digital_Rock_Physics_Template')

import matplotlib.pyplot as plt
import barbara.default_parameters as params
from matplotlib.ticker import FixedLocator, FixedFormatter
from cmcrameri import cm

from barbara.drp_template import export_raw
import barbara.input_output as io
from barbara.drp_template import plot_slice
from barbara.image import save_figure2, plot_slice
from barbara.drp_template import get_fractions
from barbara.drp_template import label_binary
from barbara.default_params import read_parameters_file, update_parameters_file

file_path = '/Users/martin/Library/Mobile Documents/com~apple~CloudDocs/MYDATA/CODING_WORLD/PYTHON_WORLD/Digital_Rock_Physics_Template/examples/pore_100_100_400.raw'

# import irregular data
dimensions = {'nz': 400, 'ny': 100, 'nx': 100}
data = io.import_model(file_path, dtype='uint8', dimensions=dimensions)

subvolume = data[:, :, :100]
subvolume_params = {'dim': 3, 'nx': 100, 'ny': 100, 'nz': 100}
update_parameters_file(paramsfile='subvolume_100_100_100.json', **subvolume_params)

labels = ['Pore', 'Matrix']

fig_xy, ax = plot_slice(subvolume, paramsfile='subvolume_100_100_100.json', cmap_set=None, slice=None, plane='xy', subvolume=None, labels=labels, title=None, voxel_size=None, dark_mode=True)
fig_yz, ax = plot_slice(subvolume, paramsfile='subvolume_100_100_100.json', cmap_set=None, slice=None, plane='yz', subvolume=None, labels=labels, title=None, voxel_size=None, dark_mode=True)
fig_xz, ax = plot_slice(subvolume, paramsfile='subvolume_100_100_100.json', cmap_set=None, slice=None, plane='xz', subvolume=None, labels=labels, title=None, voxel_size=None, dark_mode=True)


# Save figures
save_figure2(fig_xy, filename='subvolume_plane_xy')
save_figure2(fig_yz, filename='subvolume_plane_yz')
save_figure2(fig_xz, filename='subvolume_plane_xz')