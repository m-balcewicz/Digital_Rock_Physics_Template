from import_data import import_raw
from fractions_data import get_fractions

dir_path_1_12_100cube = './subvolume/Sandstone_1_29_100cube.raw'
data_1_12_100cube = import_raw(dir_path_1_12_100cube, 100)
fractions = get_fractions(data_1_12_100cube)
print(fractions)
