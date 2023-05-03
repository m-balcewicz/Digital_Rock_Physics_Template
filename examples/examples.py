# May 2023
from drp_template.plot_save_figure import visualize_plane
import drp_template.import_export as ie
import numpy as np
from drp_template.data_review import check_binary
#
dir_path_segmented = '/Volumes/mbalcewicz/SCIENCE_WORLD/STUDIES/2022_CONCRETE/PerGeos_Segmentation/PerGeos_Export/S-4-X_0_1-MPa_subvolume_600_600_988.tif'
data = ie.import_3d_tiff(dir_path_segmented)

type = 1
plane = 'xy'
fig = visualize_plane(data=data, type=1, plane=plane, cmap_set='coolwarm')
fig.show()
# data_normal = data_segmented
# type = 2
# slice = int(np.shape(data_normal)[0]/2)
# show_ct(data_normal, type, slice, 'xy')

# data_subvolume = create_subvolume(data_segmented, 400, varname)

# num_phases = 2
# # data_normal = make_model(size, num_phases)
# figure1 = show_ct(data_segmented, 2, 350, 'xy')
# path = './data_normal'
# varname = 'homogeneous_model_800cube'
# export_model(data_normal, path, varname)
