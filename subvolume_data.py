# This is a script to visualize CT data (int8)
# 04-05-2022
# Martin Balcewicz (Bochum University of Applied Sciences)
# website: https://rockphysics.org/people/members/martin-balcewicz

import numpy as np
import os
from datetime import datetime
from export_data import export_raw

def create_subvolume(data, set_subvolume, name):
    x, y, z = data.shape

    # calculate center of sample
    center_x = x / 2
    center_y = y / 2
    center_z = z / 2

    # define cutting
    cut_x = (x - set_subvolume) // 2
    cut_y = (y - set_subvolume) // 2
    cut_z = (z - set_subvolume) // 2

    # create subvolume
    data_subvolume = data[cut_x:x - cut_x, cut_y:y - cut_y, cut_z:z - cut_z]

    # x11 = cut_x
    # x22 = x-cut_x-1
    # y11 = cut_y
    # y22 = y-cut_y-1

    t = datetime.now().strftime("%Y%m%d")
    varname = str(t)
    varname = str(name + '_' + str(set_subvolume)+'cube')

    # create the subvolume directory if it does not already exist
    if not os.path.exists('subvolume'):
        os.mkdir('subvolume')

    # Save new data_subvolume as a 'uint8' raw file
    export_raw(data_subvolume, path='subvolume', varname=varname)

    return data_subvolume
