from drp_template.import_export import import_moduli
from drp_template.plot_save_figure import plot_moduli, save_figure

path = '/Users/martin/Library/Mobile Documents/com~apple~CloudDocs/MYDATA/CODING_WORLD/PYTHON_WORLD/Digital_Rock_Physics_Template/projects/2022_Pang/moduli'
moduli, moduli_header = import_moduli(path)
fig = plot_moduli(moduli, slice=0, voxel_size=None)
# save_figure(figure=fig, filename='moduli_Images_0_C10')
fig.show()