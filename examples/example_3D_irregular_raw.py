# May 2023
import sys
from drp_template.plot_save_figure import plot_slice, save_figure
import drp_template.import_export as ie
import drp_template.data_review
import numpy as np
from drp_template.data_review import check_binary

# dir_path_segmented = '/Volumes/mbalcewicz/SCIENCE_WORLD/STUDIES/2022_CONCRETE/PerGeos_Segmentation/PerGeos_Export/S-4-X_0_1-MPa_subvolume_600_600_988.tif'
# data = ie.import_3d_tiff(dir_path_segmented)

dir_path_raw = '/Users/martin/Library/Mobile Documents/com~apple~CloudDocs/MYDATA/SCIENCE_WORLD/STUDIES/2022_CONCRETE_TRIAX_CT_PERTH/Large_Sample_S' \
               '-1-Z/S-1-Z_2283_2283_200.raw'
dimensions = [200, 2283, 2283]
data = ie.import_raw(path=dir_path_raw, dtype='uint16', endian='little', dimension=dimensions)

check_endian = drp_template.data_review.check_endian(data)
print(f'importd data is: {check_endian}')

# dir_path_3d_tif = '/Volumes/mbalcewicz/SCIENCE_WORLD/STUDIES/2022_CONCRETE/PerGeos_Segmentation/LARGE_SAMPLES/S-1-Z/PerGeos_Export/S-1-Z.tif'
# data = ie.import_3d_tiff(dir_path_3d_tif)

plane = 'xy'
fig = plot_slice(data=data, cmap_set='coolwarm', slice=0, plane=plane)
fig.show()

# save_fig(figure=fig, name='/Users/martin/Library/Mobile Documents/com~apple~CloudDocs/MYDATA/SCIENCE_WORLD/STUDIES/2022_CONCRETE_TRIAX_CT_PERTH'
#                           '/Large_Sample_S-1-Z/Large_Sample_S-1-Z')

ie.export_raw(data=data, path='/Users/martin/Library/Mobile '
                              'Documents/com~apple~CloudDocs/MYDATA/SCIENCE_WORLD/STUDIES/2022_CONCRETE_TRIAX_CT_PERTH/Large_Sample_S-1-Z',
              filename='S-1-Z_big_endian', dtype='uint16', endian='big')
print('Finished')

## READ exported big-endian file
dir_path_big = '/Users/martin/Library/Mobile Documents/com~apple~CloudDocs/MYDATA/SCIENCE_WORLD/STUDIES/2022_CONCRETE_TRIAX_CT_PERTH/Large_Sample_S' \
              '-1-Z/S-1-Z_big_endian.raw'
dimensions = [200, 2283, 2283]
data_big = ie.import_raw(path=dir_path_big, dtype='uint16', endian='little', dimension=dimensions)
check_endian = drp_template.data_review.check_endian(data_big)
print(f'importd data is: {check_endian}')


## TEST
dir_path_raw = '/Users/martin/Library/Mobile Documents/com~apple~CloudDocs/MYDATA/SCIENCE_WORLD/STUDIES/2022_CONCRETE_TRIAX_CT_PERTH/Large_Sample_S' \
               '-1-Z/S-1-Z_2283_2283_200.raw'
dimensions = [200, 2283, 2283]
data = ie.import_raw(path=dir_path_raw, dtype='uint16', endian='little', dimension=dimensions)


data_le = data
data_be = data_le.byteswap().newbyteorder('>')
# Write the array to a file in little-endian byte order
with open('output_le.raw', 'wb') as f:
    data.tofile(f, sep='', format='>')

dir = 'output_le.raw'
data_test = ie.import_raw(path=dir, dtype='uint16', endian='big', dimension=dimensions)
check_endian = drp_template.data_review.check_endian(data_test)
fig = plot_slice(data=data_test, cmap_set='coolwarm', slice=0, plane=plane)
fig.show()
