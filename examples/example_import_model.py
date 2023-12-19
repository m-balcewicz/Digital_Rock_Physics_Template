import matplotlib.pyplot as plt
from matplotlib.ticker import FixedLocator, FixedFormatter
import numpy as np
from cmcrameri import cm

import barbara.input_output as io
import barbara.image as im

# FIGURE DEFAULTS
font_size=20
cmap_set = cm.batlow
l_axes = [0.22, 0.11, 0.03, 0.8]         # preliminary for the colorbar: on the left side
r_axes = [0.735, 0.11, 0.03, 0.8]         # preliminary for the colorbar: on the right side

XY = True
YZ = True
XZ = True


# z, y, x: 400, 100, 50
# x, y, z: 50, 100, 400
nx = 50
ny = 100
nz = 400
dx = 2.3 # µm per voxel
model = io.import_model(filename='pore_50_100_400.raw', dtype='uint8', shape=(nx, ny, nz), mode='r', order='F')
# fig1, ax = im.plane(data=model_1, cmap_set=None, slice=0, plane='xy', subvolume=None, labels=None, title=None, voxel_size=None)
# fig1.show()


# XY
if XY is True:
    print('XY')
    print(f"dimensions before: {model.shape}")
    model_tmp = np.transpose(model, axes=(1, 0, 2))
    print(f"dimensions before: {model_tmp.shape}")
    xy = model_tmp[:, :, 399]

    plt.rcParams['font.size'] = font_size
    fig, ax = plt.subplots(1, 1, figsize=(6, 8), dpi=300, facecolor='w', edgecolor='k')

    plt.imshow(xy, cmap=cmap_set)
    plt.title('XY')
    plt.xlabel('X-axis (voxel)')
    plt.ylabel('Y-axis (voxel)')
    ax.invert_xaxis()
    ax.invert_yaxis()
    plt.colorbar()

    # Move the y-axis to the right side
    ax.yaxis.tick_right()
    ax.yaxis.set_label_position("right")
    ax.spines["left"].set_visible(True)
    ax.spines["right"].set_visible(True)

    # Set the new tick locations and labels
    # Get the current tick locations
    xticks = ax.get_xticks()
    yticks = ax.get_yticks()

    # Calculate the new tick labels based on the resolution and desired number of ticks
    # if isinstance(dx, int):
    #     # resolution is an integer
    #     xticklabels = [f'{int(tick * dx)}' for tick in np.linspace(xticks[0], xticks[-1], 5)]
    #     yticklabels = [f'{int(tick * dx)}' for tick in np.linspace(yticks[0], yticks[-1], 5)]
    #     ax.set_xlabel('Y-axis (µm)')
    #     ax.set_ylabel('Z-axis (µm)')
    # else:
    #     # resolution is a float
    #     xticklabels = [f'{tick * dx:.1f}' for tick in np.linspace(xticks[0], xticks[-1], 5)]
    #     yticklabels = [f'{tick * dx:.1f}' for tick in np.linspace(yticks[0], yticks[-1], 5)]
    #     ax.set_xlabel('Y-axis (µm)')
    #     ax.set_ylabel('Z-axis (µm)')
    # #
    # ax.xaxis.set_major_locator(FixedLocator(np.linspace(xticks[0], xticks[-1], 5)))
    # ax.xaxis.set_major_formatter(FixedFormatter(xticklabels))
    # ax.yaxis.set_major_locator(FixedLocator(np.linspace(yticks[0], yticks[-1], 5)))
    # ax.yaxis.set_major_formatter(FixedFormatter(yticklabels))

    fig.show()


# XZ
if XZ is True:
    print('XZ')
    print(f"dimensions before: {model.shape}")
    model_tmp = np.transpose(model, axes=(2, 1, 0))
    print(f"dimensions before: {model_tmp.shape}")
    xz = model_tmp[:, 99, :]

    plt.rcParams['font.size'] = font_size
    fig, ax = plt.subplots(1, 1, figsize=(6, 8), dpi=300, facecolor='w', edgecolor='k')

    plt.imshow(xz, cmap=cmap_set)
    plt.title('XZ')
    plt.xlabel('X-axis (voxel)')
    plt.ylabel('Z-axis (voxel)')

    # ax.invert_xaxis()
    ax.invert_yaxis()
    plt.colorbar()
    fig.show()

# YZ
if YZ is True:
    print('YZ')
    print(f"dimensions before: {model.shape}")
    model_tmp = np.transpose(model, axes=(0, 2, 1))
    print(f"dimensions before: {model_tmp.shape}")
    yz = model_tmp[49, :, ]

    plt.rcParams['font.size'] = font_size
    fig, ax = plt.subplots(1, 1, figsize=(6, 8), dpi=300, facecolor='w', edgecolor='k')

    plt.imshow(yz, cmap=cmap_set)
    plt.title('YZ')
    plt.xlabel('Y-axis (voxel)')
    plt.ylabel('Z-axis (voxel)')
    ax.invert_xaxis()
    ax.invert_yaxis()

    # colorbar settings
    cbar = plt.colorbar()
    cbar.ax.yaxis.tick_left()
    # cax = fig.add_axes(l_axes)  # left, bottom, width, height
    # cbar = fig.colorbar(im, cax=cax, orientation='vertical')

    # Move the y-axis to the right side
    ax.yaxis.tick_right()
    ax.yaxis.set_label_position("right")
    ax.spines["left"].set_visible(True)
    ax.spines["right"].set_visible(True)



    fig.show()
