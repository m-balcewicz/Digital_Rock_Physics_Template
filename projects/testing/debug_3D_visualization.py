import numpy as np
import matplotlib.pyplot as plt
from test.testing import load_test_data

data = load_test_data()

# create a figure and 3D axis
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# generate the coordinates of the voxels
x, y, z = np.indices(data.shape)
voxels = (data == 3)

# plot the voxels
ax.voxels(voxels, facecolors='blue', edgecolor=(0, 0, 0, 0))

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
