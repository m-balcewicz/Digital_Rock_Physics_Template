from scipy import ndimage
from tifffile import tifffile

from import_data import import_raw, import_2d_tiff, import_3d_tiff
from show_data import visualize_plane
from fractions_data import get_fractions
import platform
import numpy as np
from tqdm import tqdm
import cc3d
from export_data import export_raw, export_3d_tif

data_100cube_raw = import_raw('./subvolume/100cube.raw', dimension=100)
data_100cube_2d_tiff = import_2d_tiff('./subvolume/2D_Tiff', type=2)
data_100cube_3d_tiff = import_3d_tiff('./subvolume/3D_Tiff/100cube.tif')

slice_no = 99

fig_data_1_12_100cube_2d_tiff = visualize_plane(data_100cube_2d_tiff, type=2, slice=slice_no, title='2D Tiff')
fig_data_1_12_100cube_2d_tiff.show()

fig_data_1_12_100cube_raw = visualize_plane(data_100cube_raw, type=2, slice=slice_no, title='3D Raw')
fig_data_1_12_100cube_raw.show()

fig_data_1_12_100cube_3d_tiff = visualize_plane(data_100cube_3d_tiff, type=2, slice=slice_no, title='3D Tiff')
fig_data_1_12_100cube_3d_tiff.show()



total_porosity = get_fractions(data_100cube_2d_tiff)
print(total_porosity)

export_raw(data_100cube_raw, path='./subvolume', varname='export_1' )

# labels_out = cc3d.connected_components(data_100cube, connectivity=6)
# fig_connected_6 = visualize_plane(labels_out, type=2, slice=99)
# fig_connected_6.show()







"""
def compute_connectivity(data, connectivity):
    # Create a zero-filled array to store the connectivity counts
    global neighbourhood
    connectivity_counts = np.zeros_like(data)

    # Define the neighbourhood based on the desired connectivity
    if connectivity == 6:
        neighbourhood = np.array([[0, 0, 1], [0, 1, 0], [1, 0, 0],
                                  [0, 0, -1], [0, -1, 0], [-1, 0, 0]])
    elif connectivity == 18:
        neighbourhood = np.array([[1, 1, 1], [1, 1, 0], [1, 1, -1],
                                  [1, 0, 1], [1, 0, 0], [1, 0, -1],
                                  [1, -1, 1], [1, -1, 0], [1, -1, -1],
                                  [0, 1, 1], [0, 1, 0], [0, 1, -1],
                                  [0, 0, 1], [0, 0, -1],
                                  [-1, 1, 1], [-1, 1, 0], [-1, 1, -1]])
    elif connectivity == 26:
        neighbourhood = np.array([[1, 1, 1], [1, 1, 0], [1, 1, -1],
                                  [1, 0, 1], [1, 0, 0], [1, 0, -1],
                                  [1, -1, 1], [1, -1, 0], [1, -1, -1],
                                  [0, 1, 1], [0, 1, 0], [0, 1, -1],
                                  [0, 0, 1], [0, 0, -1],
                                  [-1, 1, 1], [-1, 1, 0], [-1, 1, -1],
                                  [-1, 0, 1], [-1, 0, 0], [-1, 0, -1],
                                  [-1, -1, 1], [-1, -1, 0], [-1, -1, -1]])

    # Iterate over each element in the array
    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
            for k in range(data.shape[2]):
                # Check if the element is equal to 1
                if data[i, j, k] == 1:
                    # Count the number of adjacent elements that are also equal to 1
                    count = 0
                    for n in neighbourhood:
                        ni = i + n[0]
                        nj = j + n[1]
                        nk = k + n[2]
                        if ni >= 0 and ni < data.shape[0] and \
                                nj >= 0 and nj < data.shape[1] and \
                                nk >= 0 and nk < data.shape[2] and \
                                data[ni, nj, nk] == 1:
                            count += 1
                    # Store the connectivity count in the connectivity_counts array
                    connectivity_counts[i, j, k] = count


# Compute the connectivity counts for the 6-connectivity neighbourhood
connectivity_6 = compute_connectivity(data_100cube, connectivity=6)
print(connectivity_6)

# Compute the connectivity counts for the 18-connectivity neighbourhood
connectivity_18 = compute_connectivity(data_100cube, connectivity=18)
print(connectivity_18)

# Compute the connectivity counts for the 26-connectivity neighbourhood
connectivity_26 = compute_connectivity(data_100cube, connectivity=26)
print(connectivity_26)


# find connected components in the binary array
# The first argument specifies the dimensionality of the structuring
# element (in this case, 3 for a 3D array), and the second argument
# specifies the connectivity (1 for 6-connectivity, 2 for 18-connectivity,
# or 3 for 26-connectivity).

# define the connectivity
connectivity = 1 # 1 for 6-connectivity, 2 for 18-connectivity, or 3 for 26-connectivity

# define structuring element based on connectivity
if connectivity == 1:
    structure = np.array([[[0,0,0],[0,1,0],[0,0,0]],
                          [[0,1,0],[1,1,1],[0,1,0]],
                          [[0,0,0],[0,1,0],[0,0,0]]])
elif connectivity == 2:
    structure = np.ones((3, 3, 3), dtype=bool)
else:
    structure = ndimage.generate_binary_structure(3, connectivity)


labeled_array, num_features = ndimage.label(data_100cube, structure=structure)


num_components = len(np.unique(labeled_array)) - 1  # subtract 1 to exclude background label
print(num_components)

for i in range(1, num_components+1):
    component_mask = (labeled_array == i)  # boolean mask for current connected component
    component_voxels = data_100cube[component_mask]  # extract voxels for current connected component
    # do something with component_voxels


labeled_array_frac = get_fractions(labeled_array)
print(labeled_array_frac)

# print the number of connected components found
print("Number of connected components:", num_features)

# create a new array made of ones based on labeled_array
connected_array = np.where(labeled_array > 0, 1, 0)
fracs = get_fractions(connected_array)
print(fracs)

fig=visualize_plane(labeled_array, type=2, title='Figure Labeled Array')
fig.show()

fig_2=visualize_plane(connected_array, type=2, title='Figure Connected Array')
fig_2.show()
#
# # create an array with only the connected cells within
# connected_array = np.zeros_like(data_100cube)
# connected_array[labeled_array > 0] = 1
#

#
# fig=visualize_plane(connected_array, type=2)
# fig.show()


running_os = platform.system()
if running_os == 'Darwin':
    print(f'Sorry, still waiting for updated python packages')
elif running_os == 'Windows' or running_os == 'Linux':
    import porespy as ps
    import openpnm as op

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



# Save the data as a text file
np.savetxt("data.txt", data, header=header, fmt=fmt, delimiter="|")
# Define the headers for the ascii file
header = "Phase Count Fraction"

# Define the format string for the data columns
fmt = ["%.0f", "%.8e", "%.8f"]


# footprint_6=np.ones((3, 3, 1))
# footprint_18=np.ones((3, 3, 2))
# footprint_26=np.ones((3, 3, 3))
#
# # Create a copy of the input array and set all values to 0
# data_porosity = np.zeros_like(data_100cube)
#
# # find all voxels with entry = 0
# data_porosity[data_100cube == 0] = 1
#
# # label connected regions of non-zero values
# labeled_array, num_features = ndimage.label(data_porosity)
#
# # define a filter function to calculate the adjacent voxels for each label
# def adjacent_filter(x, labeled_array):
#     # get the label of the current pixel
#     current_label = x[len(x) // 2]
#     # select all pixels that belong to the current label
#     label_mask = (labeled_array == current_label)
#     # dilate the label mask to get the adjacent voxels
#     adjacent_mask = ndimage.binary_dilation(label_mask, structure=np.ones((3, 3, 1))) & (labeled_array != 0)
#     # get the values of the adjacent voxels
#     adjacent_values = data_100cube[adjacent_mask]
#     # return the values of the adjacent voxels as a tuple
#     return tuple(adjacent_values)
#
# # apply the filter to the labeled array with a progress bar
# adjacent_voxels = np.zeros_like(labeled_array)
# for i in tqdm(range(1, num_features + 1)):
#     label_mask = (labeled_array == i)
#     adjacent_voxels[label_mask] = ndimage.generic_filter(labeled_array, adjacent_filter, footprint=np.ones((3, 3, 1)), mode='constant', cval=0, extra_arguments=(labeled_array,))[label_mask]
#
# # set the values of connected_voxels to 1 for all voxels in adjacent_voxels
# connected_voxels = np.zeros_like(data_porosity)
# connected_voxels[adjacent_voxels != 0] = 1
"""