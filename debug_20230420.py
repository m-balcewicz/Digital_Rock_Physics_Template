from import_data import import_raw
from fractions_data import get_fractions
import porespy as ps
import openpnm as op

dir_path_1_12_100cube = './subvolume/Sandstone_1_29_100cube.raw'
data_1_12_100cube = import_raw(dir_path_1_12_100cube, 100)
fractions = get_fractions(data_1_12_100cube)
print(fractions)

snow_output = ps.networks.snow2(data_1_12_100cube, voxel_size=2.8)
pn = op.io.network_from_porespy(snow_output.network)
print(pn)
