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

