import numpy as np
from scipy import ndimage
from import_data import import_raw
from fractions_data import get_fractions
from tqdm import tqdm
from subvolume_data import create_subvolume


footprint_6=np.ones((3, 3, 1))
footprint_18=np.ones((3, 3, 2))
footprint_26=np.ones((3, 3, 3))
path = '/Users/martin/MYDATA/SCIENCE_WORLD/STUDIES/2022_Pang/Python/data'
dir_path_1_12_800cube = f'{path}/segmented/Sandstone_1_12_800cube_segmented.raw'
data_1_12_800cube = import_raw(dir_path_1_12_800cube, 800)
fractions = get_fractions(data_1_12_800cube)
save_subvolume_directory = '/Users/martin/Library/Mobile Documents/com~apple~CloudDocs/MYDATA/SCIENCE_WORLD/STUDIES/2022_Pang'
subvolume_1_12_100cube = create_subvolume(data=data_1_12_800cube, set_subvolume=100, name='subvolume_1_12_100cube')

'''
# Create a subvolume for faster calculations
create_subvolume(data=data_100cube, set_subvolume=100, name='data_1_12_100cube')

# Create a copy of the input array and set all values to 0
data_porosity = np.zeros_like(data_100cube)

# find all voxels with entry = 0
data_porosity[data_100cube == 0] = 1

# label connected regions of non-zero values
labeled_array, num_features = ndimage.label(data_porosity)

# define a filter function to calculate the adjacent voxels for each label
def adjacent_filter(x, labeled_array):
    # get the label of the current pixel
    current_label = x[len(x) // 2]
    # select all pixels that belong to the current label
    label_mask = (labeled_array == current_label)
    # dilate the label mask to get the adjacent voxels
    adjacent_mask = ndimage.binary_dilation(label_mask) & (labeled_array != 0)
    # get the values of the adjacent voxels
    adjacent_values = data_100cube[adjacent_mask]
    # return the values of the adjacent voxels as a tuple
    return tuple(adjacent_values)

# apply the filter to the labeled array with a progress bar
adjacent_voxels = np.zeros_like(labeled_array)
for i in tqdm(range(1, num_features + 1)):
    label_mask = (labeled_array == i)
    adjacent_voxels[label_mask] = ndimage.generic_filter(labeled_array, adjacent_filter, footprint=footprint_6, mode='constant', cval=0, extra_arguments=(labeled_array,))[label_mask]
    print(f'it: {i}')

# set the values of connected_voxels to 1 for all voxels in adjacent_voxels
connected_voxels = np.zeros_like(data_porosity)
connected_voxels[adjacent_voxels != 0] = 1
'''