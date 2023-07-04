# debugging ideas
from drp_template.plot_save_figure import plot_slice, save_figure
from drp_template.histogram_analysis import plot_histogram
from examples.load_models import raw_cube, binary_cube
from drp_template.import_export import import_2d_tiff, export_raw, import_raw
import matplotlib.pyplot as plt
import numpy as np

path = 'fracture_raw.raw'
data = import_raw(path=path, dtype='uint16', dimension=400, endian='little')

fig = plot_slice(data=data)
fig.show()

fig_hist = plot_histogram(data=data)
fig_hist.show()

# export_raw(data=data, varname='fracture_binary_ex', dtype='uint8')