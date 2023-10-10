from barbara.drp_template import import_moduli
from barbara.drp_template import plot_moduli

path = '/Users/martin/Library/Mobile Documents/com~apple~CloudDocs/MYDATA/CODING_WORLD/PYTHON_WORLD/Digital_Rock_Physics_Template/projects/2022_Pang/moduli'
moduli, moduli_header = import_moduli(path)
fig = plot_moduli(moduli, image=0, slice=0, voxel_size=None)
# save_figure(figure=fig, filename='moduli_Images_0_C10')
fig.show()