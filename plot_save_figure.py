# ------------------------------------------------------------------------------------------------- #
# ------------------------------------------------------------------------------------------------- #
# This is a script to visualize CT data_normal (int8)
# 31-03-2022
# Martin Balcewicz (Bochum University of Applied Sciences)
# website: https://rockphysics.org/people/members/martin-balcewicz
# 1 = RAW
# 2 = segmented
# ------------------------------------------------------------------------------------------------- #
# ------------------------------------------------------------------------------------------------- #
import matplotlib.pyplot as plt
from matplotlib.ticker import FixedLocator, FixedFormatter
import numpy as np


def main():
    print('-------------------------------------------------------------------------------------------------')
    print('-------------------------------------------------------------------------------------------------')
    print('Welcome CT visualizer')
    print('developed 01/2023 by Martin Balcewicz (mail: martin.balcewicz@rockphysics.org)')
    print('-------------------------------------------------------------------------------------------------')
    print('-------------------------------------------------------------------------------------------------')
    print(' ')


def visualize_plane(data, type, cmap_set=None, slice=None, plane='xy', subvolume=None, labels=None, title=None, voxel_size=None):
    """
    data: is a numpy array in which each cell will be visualized as a voxel.
    cmap_set: can be any matplotlib colormap that is available.
    """

    dimensions = data.shape
    center = np.array([dimensions[0] / 2, dimensions[0] / 2])

    # set the font size and typeface for all text in the plot
    plt.rcParams.update({'font.size': 14, 'font.family': 'Arial'})

    if type == 1 and cmap_set is None:
        cmap_set = 'gray'
    elif type == 2 and cmap_set is None:
        cmap_set = 'viridis'
    elif cmap_set is not None:
        cmap_set = cmap_set
    else:
        print('## ERROR: Please define type = 1 (for RAW CT images) or type = 2 (for segmented CT images)')
        F1 = 'NaN'

    F1 = plt.figure()

    if slice is not None:
        slice = slice

    else:
        slice = int(dimensions[0] / 2)

    if plane == 'yz':
        plt.pcolormesh(data[:, :, slice], cmap=cmap_set)
        # Get the current Axes object
        ax = plt.gca()
        # Invert the Y-axis
        ax.invert_xaxis()

        if voxel_size is not None:
            # Get the current Axes object
            ax = plt.gca()
            # Get the current tick locations
            xticks = ax.get_xticks()
            yticks = ax.get_yticks()

            # Calculate the new tick labels based on the resolution
            # Check if resolution is an integer
            if isinstance(voxel_size, int):
                # resolution is an integer
                xticklabels = [f'{int(tick * voxel_size)}' for tick in xticks]
                yticklabels = [f'{int(tick * voxel_size)}' for tick in yticks]
                plt.xlabel('X-axis (µm)')
                plt.ylabel('Y-axis (µm)')
            else:
                # resolution is a float
                xticklabels = [f'{tick * voxel_size:.1f}' for tick in xticks]
                yticklabels = [f'{tick * voxel_size:.1f}' for tick in yticks]
                plt.xlabel('X-axis (µm)')
                plt.ylabel('Y-axis (µm)')

            # Set the new tick locations and labels
            ax.xaxis.set_major_locator(FixedLocator(xticks))
            ax.xaxis.set_major_formatter(FixedFormatter(xticklabels))
            ax.yaxis.set_major_locator(FixedLocator(yticks))
            ax.yaxis.set_major_formatter(FixedFormatter(yticklabels))
        else:
            # Set the Y-axis and Z-axis labels
            plt.xlabel('Y-axis (voxel)')
            plt.ylabel('Z-axis (voxel)')

    elif plane == 'xz':
        plt.pcolormesh(data[:, slice, :], cmap=cmap_set)
        if voxel_size is not None:
            # Get the current Axes object
            ax = plt.gca()
            # Get the current tick locations
            xticks = ax.get_xticks()
            yticks = ax.get_yticks()

            # Calculate the new tick labels based on the resolution
            # Check if resolution is an integer
            if isinstance(voxel_size, int):
                # resolution is an integer
                xticklabels = [f'{int(tick * voxel_size)}' for tick in xticks]
                yticklabels = [f'{int(tick * voxel_size)}' for tick in yticks]
                plt.xlabel('X-axis (µm)')
                plt.ylabel('Y-axis (µm)')
            else:
                # resolution is a float
                xticklabels = [f'{tick * voxel_size:.1f}' for tick in xticks]
                yticklabels = [f'{tick * voxel_size:.1f}' for tick in yticks]
                plt.xlabel('X-axis (µm)')
                plt.ylabel('Y-axis (µm)')

            # Set the new tick locations and labels
            ax.xaxis.set_major_locator(FixedLocator(xticks))
            ax.xaxis.set_major_formatter(FixedFormatter(xticklabels))
            ax.yaxis.set_major_locator(FixedLocator(yticks))
            ax.yaxis.set_major_formatter(FixedFormatter(yticklabels))
        else:
            # Set the X-axis and Z-axis labels
            plt.xlabel('X-axis (voxel)')
            plt.ylabel('Z-axis (voxel)')

    elif plane == 'xy':
        plt.pcolormesh(data[slice, :, :], cmap=cmap_set)
        # Get the current Axes object
        ax = plt.gca()
        # Invert the Y-axis
        ax.invert_xaxis()

        if voxel_size is not None:
            # Get the current Axes object
            ax = plt.gca()
            # Get the current tick locations
            xticks = ax.get_xticks()
            yticks = ax.get_yticks()

            # Calculate the new tick labels based on the resolution
            # Check if resolution is an integer
            if isinstance(voxel_size, int):
                # resolution is an integer
                xticklabels = [f'{int(tick * voxel_size)}' for tick in xticks]
                yticklabels = [f'{int(tick * voxel_size)}' for tick in yticks]
                plt.xlabel('X-axis (µm)')
                plt.ylabel('Y-axis (µm)')
            else:
                # resolution is a float
                xticklabels = [f'{tick * voxel_size:.1f}' for tick in xticks]
                yticklabels = [f'{tick * voxel_size:.1f}' for tick in yticks]
                plt.xlabel('X-axis (µm)')
                plt.ylabel('Y-axis (µm)')

            # Set the new tick locations and labels
            ax.xaxis.set_major_locator(FixedLocator(xticks))
            ax.xaxis.set_major_formatter(FixedFormatter(xticklabels))
            ax.yaxis.set_major_locator(FixedLocator(yticks))
            ax.yaxis.set_major_formatter(FixedFormatter(yticklabels))
        else:
            # Set the X-axis and Y-axis labels
            plt.xlabel('X-axis (voxel)')
            plt.ylabel('Y-axis (voxel)')

    if subvolume is not None:
        rect = plt.Rectangle(center - subvolume / 2, subvolume, subvolume, fill=False, linewidth=2, edgecolor='r')
        plt.gca().add_patch(rect)

    plt.axis('tight')
    if labels is not None and type == 2:
        cbar = plt.colorbar(orientation='vertical', ticks=[m for m in range(len(labels))])
        cbar.ax.set_yticklabels([label[1] for label in labels])
    else:
        cbar = plt.colorbar(orientation='vertical')

    plt.gca().set_aspect('equal', 'box')

    if title is not None:
        plt.title(f'{title}')

    return F1


def save_fig(figure, name, format=None, dpi=None):
    # Set default format to "png" if not specified
    if format is None:
        format = "png"
    else:
        format = format
    # Set default DPI to 300 for "png" format if not specified
    if dpi is None:
        dpi = 300
    else:
        dpi = dpi
    # Save the figure
    figure.savefig(name + "." + format, dpi=dpi)

    return


# ------------------------------------------------------------------------------------------------- #


if __name__ == '__main__':
    main()
