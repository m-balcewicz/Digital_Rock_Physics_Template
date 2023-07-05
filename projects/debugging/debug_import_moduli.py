from drp_template.import_export import import_moduli
from drp_template.plot_save_figure import plot_moduli, save_figure

path = '/Users/martin/MYDATA/SCIENCE_WORLD/STUDIES/2023_Pang/Carbonate_Limestone/Images_0_C10/VPm/moduli'
moduli = import_moduli(path)
fig = plot_moduli(moduli, voxel_size=None)
save_figure(figure=fig, filename='moduli_Images_0_C10')
fig.show()