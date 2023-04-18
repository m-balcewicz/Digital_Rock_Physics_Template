import numpy as np
from matplotlib import pyplot as plt

from import_data import import_raw

dir_path_1_12_800cube = './data/Sandstone_1_12_800cube_raw.raw'
data_1_12_800cube_raw = import_raw(dir_path_1_12_800cube, 800)
xy_raw = data_1_12_800cube_raw[:, :, 1]
plt.hist(xy_raw.flat, bins=200, range=(0, 255))
plt.show()

dir_path_1_12_800cube = './data/Sandstone_1_12_800cube_nlm.raw'
data_1_12_800cube_nlm = import_raw(dir_path_1_12_800cube, 800)
xy_raw = data_1_12_800cube_nlm[:, :, 1]
plt.hist(xy_raw.flat, bins=200, range=(0, 255))
plt.show()
