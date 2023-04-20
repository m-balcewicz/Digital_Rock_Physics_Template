from import_data import import_raw
from show_data import visualize_plane
from fractions_data import get_fractions
import porespy as ps
import openpnm as op

data_100cube = import_raw('./subvolume/Sandstone_1_29_100cube.raw', dimension=100)

fig_data_1_12_800cube = visualize_plane(data_100cube, type=2, slice=50)
fig_data_1_12_800cube.show()

fractions = get_fractions(data_100cube)
print(fractions)

snow_output = ps.networks.snow2(data_100cube, voxel_size=2.8)
pn = op.io.network_from_porespy(snow_output.network)
print(pn)
"""
# Save the data as a text file
np.savetxt("data.txt", data, header=header, fmt=fmt, delimiter="|")
# Define the headers for the ascii file
header = "Phase Count Fraction"

# Define the format string for the data columns
fmt = ["%.0f", "%.8e", "%.8f"]
"""
