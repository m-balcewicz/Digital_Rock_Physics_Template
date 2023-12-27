# debugging ideas
from drp_template.drp_template import plot_slice
from drp_template.drp_template import plot_histogram
from drp_template.drp_template import import_raw

path = 'fracture_raw.raw'
data = import_raw(path=path, dtype='uint16', dimension=400, endian='little')

fig = plot_slice(data=data)
fig.show()

fig_hist = plot_histogram(data=data)
fig_hist.show()

# export_raw(data=data, varname='fracture_binary_ex', dtype='uint8')