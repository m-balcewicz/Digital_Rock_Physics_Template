# Project for Mengqiang Pang
from label_data import label_binary
from import_export_data import import_raw
from save_table import save_table
from show_data import visualize_plane
from subvolume_data import create_subvolume
from fractions_data import get_fractions
import os

# Int   Phase
# 0     Pore
# 1     Quartz
# 2     Plagioclase
# 3     K-Feldspar
# 4     Dolomite
# 5     Clay

raw_size = 800
subvolume_size = 400

make_subvolume = 0 # can be 0 or 1
make_figures = 1 # can be 0 or 1
save_figures = 1  # can be 0 or 1

import_raw_files_800 = 1 # can be 0 or 1
import_segmented_files_800 = 1 # can be 0 or 1
calculate_fractions_800 = 1 # can be 0 or 1

import_raw_files_400 = 1 # can be 0 or 1
import_segmented_files_400 = 1 # can be 0 or 1

path = '/Users/martin/MYDATA/SCIENCE_WORLD/STUDIES/2022_Pang/Python/data'

if import_raw_files_800 == 1:
    dir_path_1_12_800cube_raw = f'{path}/raw/Sandstone_1_12_800cube_raw.raw'
    dir_path_1_23_800cube_raw = f'{path}/raw/Sandstone_1_23_800cube_raw.raw'
    dir_path_1_29_800cube_raw = f'{path}/raw/Sandstone_1_29_800cube_raw.raw'
    dir_path_2_7_800cube_raw = f'{path}/raw/Sandstone_2_7_800cube_raw.raw'

    data_1_12_800cube_raw = import_raw(dir_path_1_12_800cube_raw, raw_size)
    data_1_23_800cube_raw = import_raw(dir_path_1_23_800cube_raw, raw_size)
    data_1_29_800cube_raw = import_raw(dir_path_1_29_800cube_raw, raw_size)
    data_2_7_800cube_raw = import_raw(dir_path_2_7_800cube_raw, raw_size)
    print('raw data_normal 800cube is imported')
else:
    print('No raw files imported')

if import_segmented_files_800 == 1:
    dir_path_1_12_800cube = f'{path}/segmented/Sandstone_1_12_800cube_segmented.raw'
    dir_path_1_23_800cube = f'{path}/segmented/Sandstone_1_23_800cube_segmented.raw'
    dir_path_1_29_800cube = f'{path}/segmented/Sandstone_1_29_800cube_segmented.raw'
    dir_path_2_7_800cube = f'{path}/segmented/Sandstone_2_7_800cube_segmented.raw'

    data_1_12_800cube = import_raw(dir_path_1_12_800cube, raw_size)
    data_1_23_800cube = import_raw(dir_path_1_23_800cube, raw_size)
    data_1_29_800cube = import_raw(dir_path_1_29_800cube, raw_size)
    data_2_7_800cube = import_raw(dir_path_2_7_800cube, raw_size)
    print('segmented data_normal 800cube is imported')
else:
    print('No segmented files imported')


if calculate_fractions_800 == 1 and import_segmented_files_800 == 1:
    fractions_1_12_800cube = get_fractions(data_1_12_800cube)
    save_table(fractions_1_12_800cube, varname='Sandstone_1_12_800cube')
    fractions_1_23_800cube = get_fractions(data_1_23_800cube)
    save_table(fractions_1_23_800cube, varname='Sandstone_1_23_800cube')
    fractions_1_29_800cube = get_fractions(data_1_29_800cube)
    save_table(fractions_1_29_800cube, varname='Sandstone_1_29_800cube')
    fractions_2_7_800cube = get_fractions(data_2_7_800cube)
    save_table(fractions_2_7_800cube, varname='Sandstone_2_7_800cube')
else:
    print('No fractions calculated')
    
if make_subvolume == 1:
    print('create CT raw subvolumes')
    data_1_12_400cube_raw = create_subvolume(data_1_12_800cube_raw, set_subvolume=subvolume_size,
                                             name='Sandstone_1_12_raw')
    data_1_23_400cube_raw = create_subvolume(data_1_23_800cube_raw, set_subvolume=subvolume_size,
                                             name='Sandstone_1_23_raw')
    data_1_29_400cube_raw = create_subvolume(data_1_29_800cube_raw, set_subvolume=subvolume_size,
                                             name='Sandstone_1_29_raw')
    data_2_7_400cube_raw = create_subvolume(data_2_7_800cube_raw, set_subvolume=subvolume_size,
                                            name='Sandstone_2_7_raw')

    print('create CT segmented subvolumes')
    data_1_12_400cube = create_subvolume(data_1_12_800cube, set_subvolume=subvolume_size, name='Sandstone_1_12')
    data_1_23_400cube = create_subvolume(data_1_23_800cube, set_subvolume=subvolume_size, name='Sandstone_1_23')
    data_1_29_400cube = create_subvolume(data_1_29_800cube, set_subvolume=subvolume_size, name='Sandstone_1_29')
    data_2_7_400cube = create_subvolume(data_2_7_800cube, set_subvolume=subvolume_size, name='Sandstone_2_7')

else:
    print('No created today.')


if import_raw_files_400 == 1:
    dir_path_1_12_400cube_raw = f'{path}/subvolume/Sandstone_1_12_raw_400cube.raw'
    dir_path_1_23_400cube_raw = f'{path}/subvolume/Sandstone_1_23_raw_400cube.raw'
    dir_path_1_29_400cube_raw = f'{path}/subvolume/Sandstone_1_29_raw_400cube.raw'
    dir_path_2_7_400cube_raw = f'{path}/subvolume/Sandstone_2_7_raw_400cube.raw'

    data_1_12_400cube_raw = import_raw(dir_path_1_12_400cube_raw, subvolume_size)
    data_1_23_400cube_raw = import_raw(dir_path_1_23_400cube_raw, subvolume_size)
    data_1_29_400cube_raw = import_raw(dir_path_1_29_400cube_raw, subvolume_size)
    data_2_7_400cube_raw = import_raw(dir_path_2_7_400cube_raw, subvolume_size)
    print('raw data_normal 400cube is imported')
else:
    print('No raw files imported')

if import_segmented_files_400 == 1:
    dir_path_1_12_400cube = f'{path}/subvolume/Sandstone_1_12_400cube.raw'
    dir_path_1_23_400cube = f'{path}/subvolume/Sandstone_1_23_400cube.raw'
    dir_path_1_29_400cube = f'{path}/subvolume/Sandstone_1_29_400cube.raw'
    dir_path_2_7_400cube = f'{path}/subvolume/Sandstone_2_7_400cube.raw'

    data_1_12_400cube = import_raw(dir_path_1_12_400cube, subvolume_size)
    data_1_23_400cube = import_raw(dir_path_1_23_400cube, subvolume_size)
    data_1_29_400cube = import_raw(dir_path_1_29_400cube, subvolume_size)
    data_2_7_400cube = import_raw(dir_path_2_7_400cube, subvolume_size)
    print('segmented data_normal 400cube is imported')

    fractions_1_12_400cube = get_fractions(data_1_12_400cube)
    save_table(fractions_1_12_400cube, varname='Sandstone_1_12_400cube')
    fractions_1_23_400cube = get_fractions(data_1_23_400cube)
    save_table(fractions_1_23_400cube, varname='Sandstone_1_23_400cube')
    fractions_1_29_400cube = get_fractions(data_1_29_400cube)
    save_table(fractions_1_29_400cube, varname='Sandstone_1_29_400cube')
    fractions_2_7_400cube = get_fractions(data_2_7_400cube)
    save_table(fractions_2_7_400cube, varname='Sandstone_2_7_400cube')
else:
    print('No raw files imported')


# labels = label_binary(data_1_12_400cube)
labels = [(0, 'Pore'),
          (1, 'Quartz'),
          (2, 'Plagioclase'),
          (3, 'K-Feldspar'),
          (4, 'Dolomite'),
          (5, 'Clay')]


if make_figures == 1:

    # create figures directory if it doesn't exist
    if not os.path.exists('../../figures'):
        os.makedirs('../../figures')

    if import_raw_files_800 == 1 and import_segmented_files_800 == 1:
        fig_1_12_800cube = visualize_plane(data_1_12_800cube, type=2, slice=subvolume_size, plane='xy',
                                           subvolume=subvolume_size, labels=labels)
        fig_1_12_800cube.show()

        fig_1_23_800cube = visualize_plane(data_1_23_800cube, type=2, slice=subvolume_size, plane='xy',
                                           subvolume=subvolume_size, labels=labels)
        fig_1_23_800cube.show()

        fig_1_29_800cube = visualize_plane(data_1_29_800cube, type=2, slice=subvolume_size, plane='xy',
                                           subvolume=subvolume_size, labels=labels)
        fig_1_29_800cube.show()

        fig_2_7_800cube = visualize_plane(data_2_7_800cube, type=2, slice=subvolume_size, plane='xy',
                                          subvolume=subvolume_size,
                                          labels=labels)
        fig_2_7_800cube.show()

        fig_1_29_400cube = visualize_plane(data_1_29_400cube, type=2, slice=200, plane='xy', labels=labels)
        fig_1_29_400cube.show()

        fig_1_12_800cube_raw = visualize_plane(data_1_12_800cube_raw, type=1, slice=subvolume_size, plane='xy',
                                               subvolume=subvolume_size)
        fig_1_12_800cube_raw.show()

        fig_1_23_800cube_raw = visualize_plane(data_1_23_800cube_raw, type=1, slice=subvolume_size, plane='xy',
                                               subvolume=subvolume_size, labels=labels)
        fig_1_23_800cube_raw.show()

        fig_1_29_800cube_raw = visualize_plane(data_1_29_800cube_raw, type=1, slice=subvolume_size, plane='xy',
                                               subvolume=subvolume_size, labels=labels)
        fig_1_29_800cube_raw.show()

        fig_2_7_800cube_raw = visualize_plane(data_2_7_800cube_raw, type=1, slice=subvolume_size, plane='xy',
                                              subvolume=subvolume_size,
                                              labels=labels)
        fig_2_7_800cube_raw.show()

        fig_1_29_400cube_raw = visualize_plane(data_1_29_400cube_raw, type=1, slice=200, plane='xy', labels=labels)
        fig_1_29_400cube_raw.show()

    elif import_segmented_files_800 == 1:
            fig_1_12_800cube = visualize_plane(data_1_12_800cube, type=2, slice=subvolume_size, plane='xy',
                                               subvolume=subvolume_size, labels=labels)
            fig_1_12_800cube.show()

            fig_1_23_800cube = visualize_plane(data_1_23_800cube, type=2, slice=subvolume_size, plane='xy',
                                               subvolume=subvolume_size, labels=labels)
            fig_1_23_800cube.show()

            fig_1_29_800cube = visualize_plane(data_1_29_800cube, type=2, slice=subvolume_size, plane='xy',
                                               subvolume=subvolume_size, labels=labels)
            fig_1_29_800cube.show()

            fig_2_7_800cube = visualize_plane(data_2_7_800cube, type=2, slice=subvolume_size, plane='xy',
                                              subvolume=subvolume_size,
                                              labels=labels)
            fig_2_7_800cube.show()

            fig_1_29_400cube = visualize_plane(data_1_29_400cube, type=2, slice=200, plane='xy', labels=labels)
            fig_1_29_400cube.show()
        

if save_figures == 1:
    print('saving CT raw as .png')
    fig_1_12_800cube_raw.savefig('figures/fig_1_12_800cube_raw.png', dpi=300)
    fig_1_23_800cube_raw.savefig('figures/fig_1_23_800cube_raw.png', dpi=300)
    fig_1_29_800cube_raw.savefig('figures/fig_1_29_800cube_raw.png', dpi=300)
    fig_2_7_800cube_raw.savefig('figures/fig_2_7_800cube_raw.png', dpi=300)
    fig_1_29_400cube_raw.savefig('figures/fig_1_29_400cube_raw.png', dpi=300)

    print('saving CT segmented as .png')
    fig_1_12_800cube.savefig('figures/fig_1_12_800cube.png', dpi=300)
    fig_1_23_800cube.savefig('figures/fig_1_23_800cube.png', dpi=300)
    fig_1_29_800cube.savefig('figures/fig_1_29_800cube.png', dpi=300)
    fig_2_7_800cube.savefig('figures/fig_2_7_800cube.png', dpi=300)
    fig_1_29_400cube.savefig('figures/fig_1_29_400cube.png', dpi=300)
else:
    print('No figures are saved today.')
