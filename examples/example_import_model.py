import numpy as np

import barbara.input_output as io
from barbara.drp_template import plot_slice

# import regular cube
im = io.import_model(filename='data_100cube.raw', dtype='uint8', shape=100)
fig = plot_slice(im)
fig.show()


# import irregular data
im = io.import_model(filename='pore_100_100_400.raw', dtype='uint8', shape=(400, 100, 100))
fig = plot_slice(im)
fig.show()

im = io.import_model(filename='pore_50_100_400.raw', dtype='uint8', shape=(400, 100, 50))
fig = plot_slice(im)
fig.show()