import drp_template.drp_template.import_export as ie
from drp_template.drp_template import plot_slice

data = ie.import_2d_tiff(path='S-4-X', type='raw')
plane = 'xy'
fig = plot_slice(data=data, slice=49, plane=plane)
fig.show()
sa