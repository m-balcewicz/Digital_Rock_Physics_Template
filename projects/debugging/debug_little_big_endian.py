import drp_template
from drp_template.plot_save_figure import plot_slice
import drp_template.import_export as ie



dir_path_raw = 'S-1-Z_500_400_100.raw'
dimensions = [100, 400, 500]
plane = 'xy'
data_in = ie.import_raw(path=dir_path_raw, dtype='uint16', endian='little', dimension=dimensions)
fig = plot_slice(data=data_in, type=1, cmap_set='coolwarm', slice=49, plane=plane)
fig.show()

drp_template.data_review.check_endian(data_in)
output = drp_template.change_endianess.little_to_big(data_in)
ie.export_raw(data=output, dtype='uint16', endian='big')