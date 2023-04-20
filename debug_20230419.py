import numpy as np
import porespy as ps
import openpnm as op
import matplotlib.pyplot as plt
ps.visualization.set_mpl_style()
np.random.seed(10)

im = ps.generators.blobs(shape=[400, 400], porosity=0.6, blobiness=2)
fig, ax = plt.subplots(figsize=(4, 4))
ax.imshow(im);
path = '/data/GZB/mbalcewicz/SCIENCE_WORLD/STUDIES/2022_Pang/400cube/Python'
fig.savefig(f'{path}/figures/plot-1.png', format='png')

