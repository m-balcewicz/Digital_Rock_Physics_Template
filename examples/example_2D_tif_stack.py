import drp_template.import_export as ie
from drp_template.plot_save_figure import visualize_plane

data = ie.import_2d_tiff(path='/Volumes/files/mbalcewicz/XRAY_COMPUTED_TOMOGRAPHY/2022_CONCRETE/CoDA/PLUGS_SMALL/S-4-X/04_Perth/0_1MPa/S-4-X_0_1MPa_1_9999um', type='raw')
plane = 'xy'
fig = visualize_plane(data=data, type='raw', plane=plane, slice=0)
fig.show()