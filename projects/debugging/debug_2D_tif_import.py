import drp_template.import_export as ie
from drp_template.plot_save_figure import visualize_plane

data = ie.import_2d_tiff(path='S-4-X', type='raw')
plane = 'xy'
fig = visualize_plane(data=data, type='raw', plane=plane, slice=49)
fig.show()