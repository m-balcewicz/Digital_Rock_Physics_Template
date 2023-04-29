import import_export_data as ie
from show_data import visualize_plane
from test.testing import load_test_data

data = load_test_data()

path_out = '/Users/martin/Library/Mobile Documents/com~apple~CloudDocs/MYDATA/CODING_WORLD/PYTHON_WORLD/Digital_Rock_Physics_Template/subvolume'
# ie.export_vtk(data, path=path_out, varname='export')
plane_of_view = 'xy'
figure = visualize_plane(data, type=2, resolution=2.8, plane=plane_of_view, title=f'{plane_of_view}-plane')
figure.show()