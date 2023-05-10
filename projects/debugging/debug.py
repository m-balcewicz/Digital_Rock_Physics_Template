# debugging ideas
from drp_template.plot_save_figure import plot_slice, save_figure
from drp_template.histogram_analysis import plot_histogram
from examples.data import load_raw_cube, load_binary_cube
import matplotlib.pyplot as plt
import numpy as np
from drp_template.cubehelix import helix

data_raw = load_raw_cube()
data_binary = load_binary_cube()

fig_slice_xy = plot_slice(data_raw, cmap_set=None, slice=None, plane='xy', subvolume=None, labels=None, title=None, voxel_size=None)
fig_slice_xy.show()
save_figure(figure=fig_slice_xy, name='fig_slice_xy')

fig_slice_xz = plot_slice(data_raw, cmap_set=None, slice=None, plane='xz', subvolume=None, labels=None, title=None, voxel_size=None)
fig_slice_xz.show()
save_figure(figure=fig_slice_xz, name='fig_slice_xz')

fig_slice_yz = plot_slice(data_raw, cmap_set=None, slice=None, plane='yz', subvolume=None, labels=None, title=None, voxel_size=None)
fig_slice_yz.show()
save_figure(figure=fig_slice_yz, name='fig_slice_yz')

# fig_slice_2 = plot_slice(data_binary, cmap_set=None, slice=None, plane='xy', subvolume=None, labels=None, title=None, voxel_size=None)
# fig_slice_2.show()
#
fig_hist = plot_histogram(data_raw, dtype='uint8')
fig_hist.show()
save_figure(figure=fig_hist, name='fig_hist')
