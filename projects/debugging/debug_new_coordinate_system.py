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
from barbara.image import save_figure2, plot_slice2
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

fig, ax = plot_slice2(subvolume, paramsfile='subvolume_100_100_100.json', cmap_set="gray", layer=None, plane='xy', subvolume=50.5, labels=labels, title=None, voxel_size=2.5, dark_mode=False)
save_figure2(fig, filename='subvolume_plane_xy')

fig, ax = plot_slice2(subvolume, paramsfile='subvolume_100_100_100.json', cmap_set="ocean", layer=None, plane='yz', subvolume=None, labels=labels, title=None, voxel_size=None, dark_mode=True)
save_figure2(fig, filename='subvolume_plane_yz')

fig, ax = plot_slice2(subvolume, paramsfile='subvolume_100_100_100.json', cmap_set=None, layer=None, plane='xz', subvolume=None, labels=labels, title=None, voxel_size=2, dark_mode=True)
save_figure2(fig, filename='subvolume_plane_xz')