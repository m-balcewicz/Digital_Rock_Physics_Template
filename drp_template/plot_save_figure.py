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
    This is some text.

    Parameters:
    -----------
    data :
        is a numpy array in which each cell will be visualized as a voxel.
    type :
        Data type can be 'raw' or 'binary'
    cmap_set :
        can be any matplotlib colormap that is available.
    slice :
        some text
    plane :
        some text
    subvolume :
        some text
    labels :
        some text
    title :
        some text
    voxel_size :
        some text
    """

    dimensions = data.shape
    center = np.array([dimensions[0] / 2, dimensions[0] / 2])

    # # set the font size and typeface for all text in the plot
    # plt.rcParams.update({'font.size': 14, 'font.family': 'Arial'})
    #
    if type == 'raw' and cmap_set is None:
        cmap_set = 'gray'
    elif type == 'binary' and cmap_set is None:
        cmap_set = 'viridis'
    elif cmap_set is not None:
        cmap_set = cmap_set
    else:
        print('## ERROR: Please define type = 1 (for RAW CT images) or type = 2 (for segmented CT images)')
        fig = 'NaN'

    # get the minimum and maximum values of the data
    vmin = np.amin(data)
    vmax = np.amax(data)

    if slice is not None:
        slice = slice
    else:
        slice = int(dimensions[0] / 2)

    if plane == 'yz':
        # set the font size and typeface for all text in the plot
        plt.rcParams.update({'font.size': 18, 'font.family': 'Arial'})

        fig = plt.figure(figsize=(8, 6))
        ax = fig.add_axes([0.15, 0.1, 0.75, 0.8])  # left, bottom, width, height

        im = ax.pcolormesh(data[:, :, slice], cmap=cmap_set, vmin=vmin, vmax=vmax)
        ax.set_aspect('equal', 'box')

        # Add a colorbar to the left of the plot
        cax = fig.add_axes([0.18, 0.1, 0.03, 0.8])  # left, bottom, width, height
        cbar = fig.colorbar(im, cax=cax, orientation='vertical')
        cbar.ax.yaxis.tick_left()

        if labels is not None and type == 'binary':
            cbar.ax.yaxis.set_label_position("right")
            cbar.ax.yaxis.tick_right()
            cbar.set_ticks(np.arange(len(labels)))
            cbar.ax.set_yticklabels([label.replace('_', '\n') for label in labels])
        else:
            cbar = fig.colorbar(im, cax=cax, orientation='vertical')

        cbar.ax.yaxis.tick_left()

        plt.axis('tight')

        # Invert the Y-axis
        ax.invert_xaxis()

        # Move the y-axis to the right side
        ax.yaxis.tick_right()
        ax.yaxis.set_label_position("right")
        ax.spines["left"].set_visible(False)
        ax.spines["right"].set_visible(True)

        if voxel_size is not None:
            # Get the current tick locations
            xticks = ax.get_xticks()
            yticks = ax.get_yticks()

            # Calculate the new tick labels based on the resolution
            # Check if resolution is an integer
            if isinstance(voxel_size, int):
                # resolution is an integer
                xticklabels = [f'{int(tick * voxel_size)}' for tick in xticks]
                yticklabels = [f'{int(tick * voxel_size)}' for tick in yticks]
                ax.set_xlabel('Y-axis (µm)')
                ax.set_ylabel('Z-axis (µm)')
            else:
                # resolution is a float
                xticklabels = [f'{tick * voxel_size:.1f}' for tick in xticks]
                yticklabels = [f'{tick * voxel_size:.1f}' for tick in yticks]
                ax.set_xlabel('Y-axis (µm)')
                ax.set_ylabel('Z-axis (µm)')

            # Set the new tick locations and labels
            ax.xaxis.set_major_locator(FixedLocator(xticks))
            ax.xaxis.set_major_formatter(FixedFormatter(xticklabels))
            ax.yaxis.set_major_locator(FixedLocator(yticks))
            ax.yaxis.set_major_formatter(FixedFormatter(yticklabels))
        else:
            # Set the x-axis and y-axis titles
            ax.set_xlabel('Y-axis (voxel)')
            ax.set_ylabel('Z-axis (voxel)')

        # Add a title if given
        if title is not None:
            plt.title(f'{title}', fontsize=20, fontweight='bold', y=1.01, x=10.5, ha='center')

    elif plane == 'xz':
        # set the font size and typeface for all text in the plot
        plt.rcParams.update({'font.size': 18, 'font.family': 'Arial'})

        fig = plt.figure(figsize=(8, 6))
        ax = fig.add_axes([0.15, 0.1, 0.75, 0.8])  # left, bottom, width, height

        im = ax.pcolormesh(data[:, slice, :], cmap=cmap_set, vmin=vmin, vmax=vmax)
        ax.set_aspect('equal', 'box')

        # Add a colorbar to the right of the plot
        cax = fig.add_axes([0.84, 0.1, 0.03, 0.8])  # left, bottom, width, height
        cbar = fig.colorbar(im, cax=cax, orientation='vertical')
        cbar.ax.yaxis.tick_right()

        if labels is not None and type == 'binary':
            cbar.ax.yaxis.set_label_position("left")
            cbar.ax.yaxis.tick_left()
            cbar.set_ticks(np.arange(len(labels)))
            cbar.ax.set_yticklabels([label.replace('_', '\n') for label in labels])
        else:
            cbar = fig.colorbar(im, cax=cax, orientation='vertical')

        cbar.ax.yaxis.tick_right()

        plt.axis('tight')

        # # Invert the Y-axis
        # ax.invert_xaxis()

        # Move the y-axis to the left side
        ax.yaxis.tick_left()
        ax.yaxis.set_label_position("left")
        ax.spines["right"].set_visible(False)
        ax.spines["left"].set_visible(True)

        if voxel_size is not None:
            # Get the current tick locations
            xticks = ax.get_xticks()
            yticks = ax.get_yticks()

            # Calculate the new tick labels based on the resolution
            # Check if resolution is an integer
            if isinstance(voxel_size, int):
                # resolution is an integer
                xticklabels = [f'{int(tick * voxel_size)}' for tick in xticks]
                yticklabels = [f'{int(tick * voxel_size)}' for tick in yticks]
                ax.set_xlabel('X-axis (µm)')
                ax.set_ylabel('Z-axis (µm)')
            else:
                # resolution is a float
                xticklabels = [f'{tick * voxel_size:.1f}' for tick in xticks]
                yticklabels = [f'{tick * voxel_size:.1f}' for tick in yticks]
                ax.set_xlabel('X-axis (µm)')
                ax.set_ylabel('Z-axis (µm)')

            # Set the new tick locations and labels
            ax.xaxis.set_major_locator(FixedLocator(xticks))
            ax.xaxis.set_major_formatter(FixedFormatter(xticklabels))
            ax.yaxis.set_major_locator(FixedLocator(yticks))
            ax.yaxis.set_major_formatter(FixedFormatter(yticklabels))
        else:
            # Set the x-axis and y-axis titles
            ax.set_xlabel('X-axis (voxel)')
            ax.set_ylabel('Z-axis (voxel)')

        # Add a title if given
        if title is not None:
            plt.title(f'{title}', fontsize=20, fontweight='bold', y=1.01, x=-10.5, ha='center')

    elif plane == 'xy':
        # set the font size and typeface for all text in the plot
        plt.rcParams.update({'font.size': 18, 'font.family': 'Arial'})

        fig = plt.figure(figsize=(8, 6))
        ax = fig.add_axes([0.15, 0.1, 0.75, 0.8])  # left, bottom, width, height

        im = ax.pcolormesh(data[slice, :, :], cmap=cmap_set, vmin=vmin, vmax=vmax)
        ax.set_aspect('equal', 'box')


        # Add a colorbar to the left of the plot
        cax = fig.add_axes([0.17, 0.1, 0.03, 0.8])  # left, bottom, width, height
        cbar = fig.colorbar(im, cax=cax, orientation='vertical')
        cbar.ax.yaxis.tick_left()

        if labels is not None and type == 'binary':
            cbar.ax.yaxis.set_label_position("right")
            cbar.ax.yaxis.tick_right()
            cbar.set_ticks(np.arange(len(labels)))
            cbar.ax.set_yticklabels([label.replace('_', '\n') for label in labels])
        else:
            cbar = fig.colorbar(im, cax=cax, orientation='vertical')

        cbar.ax.yaxis.tick_left()


        plt.axis('tight')

        ax.invert_xaxis()

        # Move the y-axis to the right side
        ax.yaxis.tick_right()
        ax.yaxis.set_label_position("right")
        ax.spines["left"].set_visible(False)
        ax.spines["right"].set_visible(True)

        if voxel_size is not None:
            # Get the current tick locations
            xticks = ax.get_xticks()
            yticks = ax.get_yticks()

            # # Calculate the new tick labels based on the resolution
            # # Check if resolution is an integer
            # if isinstance(voxel_size, int):
            #     # resolution is an integer
            #     xticklabels = [f'{int(tick * voxel_size)}' for tick in xticks]
            #     yticklabels = [f'{int(tick * voxel_size)}' for tick in yticks]
            #     ax.set_xlabel('X-axis (µm)')
            #     ax.set_ylabel('Y-axis (µm)')
            # else:
            #     # resolution is a float
            #     xticklabels = [f'{tick * voxel_size:.1f}' for tick in xticks]
            #     yticklabels = [f'{tick * voxel_size:.1f}' for tick in yticks]
            #     ax.set_xlabel('X-axis (µm)')
            #     ax.set_ylabel('Y-axis (µm)')
            #
            # # Set the new tick locations and labels
            # ax.xaxis.set_major_locator(FixedLocator(xticks))
            # ax.xaxis.set_major_formatter(FixedFormatter(xticklabels))
            # ax.yaxis.set_major_locator(FixedLocator(yticks))
            # ax.yaxis.set_major_formatter(FixedFormatter(yticklabels))

            # Calculate the new tick labels based on the resolution and desired number of ticks
            if isinstance(voxel_size, int):
                # resolution is an integer
                xticklabels = [f'{int(tick * voxel_size)}' for tick in np.linspace(xticks[0], xticks[-1], 4)]
                yticklabels = [f'{int(tick * voxel_size)}' for tick in np.linspace(yticks[0], yticks[-1], 4)]
                ax.set_xlabel('X-axis (µm)')
                ax.set_ylabel('Y-axis (µm)')
            else:
                # resolution is a float
                xticklabels = [f'{tick * voxel_size:.1f}' for tick in np.linspace(xticks[0], xticks[-1], 4)]
                yticklabels = [f'{tick * voxel_size:.1f}' for tick in np.linspace(yticks[0], yticks[-1], 4)]
                ax.set_xlabel('X-axis (µm)')
                ax.set_ylabel('Y-axis (µm)')

            # Set the new tick locations and labels
            ax.xaxis.set_major_locator(FixedLocator(np.linspace(xticks[0], xticks[-1], 4)))
            ax.xaxis.set_major_formatter(FixedFormatter(xticklabels))
            ax.yaxis.set_major_locator(FixedLocator(np.linspace(yticks[0], yticks[-1], 4)))
            ax.yaxis.set_major_formatter(FixedFormatter(yticklabels))

        else:
            # Set the x-axis and y-axis titles
            ax.set_xlabel('X-axis (voxel)')
            ax.set_ylabel('Y-axis (voxel)')

        # Add a title if given
        if title is not None:
            plt.title(f'{title}', fontsize=20, fontweight='bold', y=1.01, x=10.5, ha='center')

    # Add subvolume rectangle if given
    if subvolume is not None:
        rect = plt.Rectangle(center - subvolume / 2, subvolume, subvolume, fill=False, linewidth=2, edgecolor='r')
        ax.add_patch(rect)

    return fig


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
