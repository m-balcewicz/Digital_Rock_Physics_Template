from label_data import label_binary
from import_data import import_raw
from import_data import import_heidi
from show_data import visualize_plane
from subvolume_data import create_subvolume
from fractions_data import get_fractions
import numpy as np

dir_path_1_12_800cube = './data/Sandstone_1_12_800cube_segmented.raw'
data_1_12_800cube = import_raw(dir_path_1_12_800cube, 800)

labels = [(0, 'Pore'),
 (1, 'Quartz'),
 (2, 'Plagioclase'),
 (3, 'K-Feldspar'),
 (4, 'Dolomite'),
 (5, 'Clay')]

fig_data_1_12_800cube = visualize_plane(data_1_12_800cube, type=2, slice=200, plane='xy', labels=labels, subvolume=400)
fig_data_1_12_800cube.show()

fractions, header = get_fractions(data_1_12_800cube)
"""
# Save the data as a text file
np.savetxt("data.txt", data, header=header, fmt=fmt, delimiter="|")
# Define the headers for the ascii file
header = "Phase Count Fraction"

# Define the format string for the data columns
fmt = ["%.0f", "%.8e", "%.8f"]
"""
