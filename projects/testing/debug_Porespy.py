import numpy as np
import porespy as ps
import openpnm as op
import matplotlib.pyplot as plt
a=ps.visualization.set_mpl_style()
a_1=np.random.seed(10)

im = ps.generators.blobs(shape=[400, 400], porosity=0.6, blobiness=2)
fig, ax = plt.subplots(figsize=(4, 4))
ax.imshow(im);
fig.show()

snow_output = ps.networks.snow2(im, voxel_size=1)
pn = op.io.network_from_porespy(snow_output.network)
print(pn)

# import matplotlib.pyplot as plt
# import numpy as np
# import porespy as ps
# import inspect
# ps.visualization.set_mpl_style()
# inspect.signature(ps.visualization.bar)
#
# np.random.seed(10)
# im = ps.generators.blobs(shape=[500, 500])
# im = ps.filters.porosimetry(im)
# results = ps.metrics.pore_size_distribution(im=im, log=False)
# ps.visualization.bar(results)