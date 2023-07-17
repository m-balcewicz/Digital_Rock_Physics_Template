import tools.drp_template.import_export as ie
from tools.drp_template import plot_slice

data = ie.import_2d_tiff(path='/Volumes/files/mbalcewicz/XRAY_COMPUTED_TOMOGRAPHY/2022_CONCRETE/CoDA/PLUGS_SMALL/S-4-X/04_Perth/0_1MPa/S-4-X_0_1MPa_1_9999um', type='raw')
plane = 'xy'

fig = plot_slice(data=data, cmap_set='helix', slice=0, plane=plane)
fig.show()

