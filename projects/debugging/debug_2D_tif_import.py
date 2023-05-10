import drp_template.import_export as ie
from drp_template.plot_save_figure import plot_slice, save_figure

data = ie.import_2d_tiff(path='S-4-X', type='raw')
plane = 'xy'
fig = plot_slice(data=data, slice=49, plane=plane)
fig.show()
sa