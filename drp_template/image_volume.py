import numpy as np
import matplotlib.pyplot as plt
from examples.data import load_100cube

data = load_100cube()

# create a figure and 3D axis
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# generate the coordinates of the voxels
x, y, z = np.indices(data.shape)

# loop through unique values and plot voxels with corresponding colors
for val in np.unique(data):
    voxels = (data == val)
    facecolor = plt.get_cmap('viridis')(val / np.max(data))[:3]  # calculate facecolor based on viridis colormap
    ax.voxels(voxels, facecolors=facecolor, edgecolor=(0, 0, 0, 0))

# set the axis labels
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

# make axis scales equal
max_range = np.array([x.max()-x.min(), y.max()-y.min(), z.max()-z.min()]).max()
x_center = (x.max()+x.min()) / 2
y_center = (y.max()+y.min()) / 2
z_center = (z.max()+z.min()) / 2
ax.set_xlim(x_center - max_range/2, x_center + max_range/2)
ax.set_ylim(y_center - max_range/2, y_center + max_range/2)
ax.set_zlim(z_center - max_range/2, z_center + max_range/2)
ax.set_box_aspect([1,1,1])

# show the plot
plt.show()
