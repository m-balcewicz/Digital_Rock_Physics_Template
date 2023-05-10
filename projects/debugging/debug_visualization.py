import numpy as np
import matplotlib.pyplot as plt

from drp_template import plot_slice, check_binary
from examples.data import load_raw_cube, load_binary_cube

data_raw = load_raw_cube()
data_binary = load_binary_cube()

data_binary = check_binary(data_binary)

labels = ('Pore_iso.', 'Pore_con.', 'Solid')
planes = ('xy', 'xz', 'yz')




fig_raw = plot_slice(data=data_raw, slice=49, plane=planes[0], subvolume=50, voxel_size=2)
fig_raw.show()

fig_binary_xy = plot_slice(data=data_binary, slice=49, plane=planes[0], subvolume=50, labels=labels, title=f'Binary {planes[0]}', voxel_size=2)
fig_binary_xy.show()
fig_binary_xz = plot_slice(data=data_binary, slice=49, plane=planes[1], subvolume=50, labels=labels, title=f'Binary {planes[1]}', voxel_size=2)
fig_binary_xz.show()
fig_binary_yz = plot_slice(data=data_binary, slice=49, plane=planes[2], subvolume=50, labels=labels, title=f'Binary {planes[2]}', voxel_size=2)
fig_binary_yz.show()