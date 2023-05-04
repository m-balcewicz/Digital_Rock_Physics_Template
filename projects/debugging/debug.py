# debugging ideas
from examples.data import load_100cube


data = load_100cube()

# path_out = '/subvolume'
# # ie.export_vtk(data, path=path_out, varname='export')
# plane_of_view = ['xy', 'xz', 'yz']
# slice = 99
# for m in range(len(plane_of_view)):
#     figure = visualize_plane(data, type=2, slice=slice, plane=plane_of_view[m], title=f'{plane_of_view[m]}-plane | slice: {slice}', voxel_size=2.8)
#     figure.show()
