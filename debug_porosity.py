from import_data import import_raw
from show_data import visualize_plane
from fractions_data import get_fractions
import porespy as ps
import openpnm as op

data_100cube = import_raw('./subvolume/Sandstone_1_29_100cube.raw', dimension=100)

fig_data_1_12_100cube = visualize_plane(data_100cube, type=2, slice=50)
fig_data_1_12_100cube.show()
fig_data_1_12_100cube.savefig('./figures/figure-1.png', format='png')

fractions = get_fractions(data_100cube)
print(fractions)

snow_output = ps.networks.snow2(data_100cube, voxel_size=2.8)
pn = op.io.network_from_porespy(snow_output.network)
print(pn)

# # sphinx_gallery_thumbnail_number = 2
# import spam.mesh
# import matplotlib.pyplot as plt
# import spam.label
# import spam.plotting
# import scipy.ndimage
# import spam.datasets
# import numpy
#
# midSlice = data_100cube.shape[0] // 2
# binary = numpy.logical_and(data_100cube > 28000, data_100cube < 40000)
# cyl = spam.mesh.createCylindricalMask(data_100cube.shape, 40)
# binary = numpy.logical_and(binary, cyl)
# pores = scipy.ndimage.binary_dilation(data_100cube < 26000, iterations=1)
# binary[pores] = 0
# labelled = spam.label.ITKwatershed.watershed(binary)
# print("{} particles have been identified".format(labelled.max()))
# plt.figure()
# plt.title("Labelled volume")
# plt.imshow(labelled[midSlice], cmap=spam.label.randomCmap)
# plt.savefig('/data/GZB/mbalcewicz/SCIENCE_WORLD/STUDIES/2023_PYTHON_POROSITY/spam-figure-2.png', format='png')


"""
# Save the data as a text file
np.savetxt("data.txt", data, header=header, fmt=fmt, delimiter="|")
# Define the headers for the ascii file
header = "Phase Count Fraction"

# Define the format string for the data columns
fmt = ["%.0f", "%.8e", "%.8f"]
"""
