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
from barbara.default_params import read_parameters_file

file_path_3 = '/Users/martin/Library/Mobile Documents/com~apple~CloudDocs/MYDATA/CODING_WORLD/PYTHON_WORLD/Digital_Rock_Physics_Template/examples/data_100cube.raw'
file_path_2 = '/Users/martin/Library/Mobile Documents/com~apple~CloudDocs/MYDATA/CODING_WORLD/PYTHON_WORLD/Digital_Rock_Physics_Template/examples/pore_50_100_400.raw'
file_path = '/Users/martin/Library/Mobile Documents/com~apple~CloudDocs/MYDATA/CODING_WORLD/PYTHON_WORLD/Digital_Rock_Physics_Template/examples/pore_100_100_400.raw'

# import irregular data
dimensions_3 = {'nx': 100, 'ny': 100, 'nz': 100}
dimensions_2 = {'nz': 400, 'ny': 100, 'nx': 50}
dimensions = {'nz': 400, 'ny': 100, 'nx': 100}
data_3 = io.import_model(file_path_3, dtype='uint8', dimensions=dimensions_3)
data_2 = io.import_model(file_path_2, dtype='uint8', dimensions=dimensions_2)
data = io.import_model(file_path, dtype='uint8', dimensions=dimensions)

fig, ax = plot_slice2(data_3, paramsfile='data_100cube.json', cmap_set=None, slice=None, plane='xy', subvolume=None, labels=None, title=None, voxel_size=None, dark_mode=True)
save_figure2(fig, filename='plane_xy')

fig, ax = plot_slice2(data_2, paramsfile='pore_50_100_400.json', cmap_set=None, slice=None, plane='xy', subvolume=None, labels=None, title=None, voxel_size=None, dark_mode=True)
save_figure2(fig, filename='plane_xy_2')

fig, ax = plot_slice2(data, paramsfile='pore_100_100_400.json', cmap_set=None, slice=None, plane='yz', subvolume=None, labels=None, title=None, voxel_size=None, dark_mode=True)
save_figure2(fig, filename='plane_yz')

fig, ax = plot_slice2(data, paramsfile='pore_100_100_400.json', cmap_set=None, slice=None, plane='xz', subvolume=None, labels=None, title=None, voxel_size=None, dark_mode=True)
save_figure2(fig, filename='plane_xz')

fig, ax = plot_slice2(data_3, paramsfile='data_100cube.json', cmap_set=None, slice=None, plane='xz', subvolume=None, labels=None, title=None, voxel_size=None, dark_mode=True)
save_figure2(fig, filename='plane_xz_3')

