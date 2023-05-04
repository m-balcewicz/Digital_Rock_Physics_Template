import numpy as np
import matplotlib.pyplot as plt
from examples.data import load_100cube

data = load_100cube()

# Plot the xy slice
fig = plt.figure(figsize=(10, 8))
ax1 = fig.add_subplot(2, 2, 1)
ax1.imshow(np.squeeze(data[:, :, -1]), origin='lower')
# ax1.set_title('XY Slice')
ax1.set_xlabel('X')
ax1.set_ylabel('Y')
# fig.colorbar(ax=ax1)

# Plot the xz slice
ax2 = fig.add_subplot(2, 2, 2)
ax2.imshow(np.squeeze(data[:, -1, :]), origin='lower')
# ax2.set_title('XZ Slice')
ax2.set_xlabel('X')
ax2.set_ylabel('Z')
# fig.colorbar(ax=ax2)

# Plot the yz slice
ax3 = fig.add_subplot(2, 2, 3)
ax3.imshow(np.squeeze(data[-1, :, :]), origin='lower')
# ax3.set_title('YZ Slice')
ax3.set_xlabel('Y')
ax3.set_ylabel('Z')
# fig.colorbar(ax=ax3)

# Show the 3D data as a volume
ax4 = fig.add_subplot(2, 2, 4, projection='3d')

# Set the colors for the xy, yz, and xz slices
colors = ['red', 'green', 'blue']

# Create a 3D boolean array to specify the voxels to plot
voxels = np.zeros_like(data, dtype=bool)

# Set the xy slice
voxels[:, :, -1] = True

# Set the yz slice
voxels[-1, :, :] = True

# Set the xz slice
voxels[:, -1, :] = True

# Get the 2D slices
xy_slice = data[:, :, -1]
yz_slice = data[-1, :, :]
xz_slice = data[:, -1, :]

# Broadcast the 2D slices to the shape of the data array
xy_slice = np.broadcast_to(xy_slice[..., np.newaxis], data.shape)
yz_slice = np.broadcast_to(yz_slice[np.newaxis, ...], data.shape)
xz_slice = np.broadcast_to(xz_slice[:, np.newaxis, :], data.shape)

# Set the facecolors using the viridis colormap and the specified colors
facecolors = [
    plt.get_cmap('viridis')(xy_slice),
    plt.get_cmap('viridis')(xz_slice),
    plt.get_cmap('viridis')(yz_slice)
]

# Plot the voxels using the specified facecolors and edgecolor
ax4.voxels(voxels, facecolors=facecolors, edgecolor='k')

# Set the limits and labels of the axes
ax4.set_xlim3d(0, data.shape[0])
ax4.set_ylim3d(0, data.shape[1])
ax4.set_zlim3d(0, data.shape[2])
ax4.set_xlabel('X')
ax4.set_ylabel('Y')
ax4.set_zlabel('Z')

# Set the aspect ratio of the axes to 'equal'
ax4.set_box_aspect((np.ptp(ax4.get_xlim()), np.ptp(ax4.get_ylim()), np.ptp(ax4.get_zlim())))






# xx, yy, zz = np.meshgrid(np.arange(data.shape[0]),
#                          np.arange(data.shape[1]),
#                          np.arange(data.shape[2]))
# colors = np.empty(data.shape, dtype=object)
# colors[data] = plt.cm.viridis(data[data])
# ax4.voxels(data, facecolors=colors, edgecolor='k', alpha=0.8, cmap='viridis')
# # ax4.voxels(data, facecolors='r', edgecolor='k')
# # ax4.set_title('3D Volume')
# ax4.set_xlabel('X')
# ax4.set_ylabel('Y')
# ax4.set_zlabel('Z')

# Set equal aspect ratio for ax4
# ax4.set_box_aspect((np.ptp(xx), np.ptp(yy), np.ptp(zz)))

plt.show()
