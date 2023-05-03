# May 2023
from drp_template.plot_save_figure import visualize_plane
import drp_template.import_export as ie
import numpy as np
from drp_template.data_review import check_binary


def main():
    # dir_path_segmented = '/Volumes/mbalcewicz/SCIENCE_WORLD/STUDIES/2022_CONCRETE/PerGeos_Segmentation/PerGeos_Export/S-4-X_0_1-MPa_subvolume_600_600_988.tif'
    # data = ie.import_3d_tiff(dir_path_segmented)

    dir_path_raw = '/Volumes/mbalcewicz/SCIENCE_WORLD/STUDIES/2022_CONCRETE/PerGeos_Segmentation/LARGE_SAMPLES/S-1-Z/PerGeos_Export/S-1-Z_2283_2283_200' \
                  '.raw'
    dimensions = [200, 2283, 2283]
    data = ie.import_raw(path=dir_path_raw, dtype='uint16', endian='little', dimension=dimensions)

    # dir_path_3d_tif = '/Volumes/mbalcewicz/SCIENCE_WORLD/STUDIES/2022_CONCRETE/PerGeos_Segmentation/LARGE_SAMPLES/S-1-Z/PerGeos_Export/S-1-Z.tif'
    # data = ie.import_3d_tiff(dir_path_3d_tif)

    plane = 'xy'
    fig = visualize_plane(data=data, type=1, plane=plane, cmap_set='coolwarm', slice=0)
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


if __name__ == '__main__':
    main()
