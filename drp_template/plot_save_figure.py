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
import drp_template.default_parameters as params


def main():
    print('-------------------------------------------------------------------------------------------------')
    print('-------------------------------------------------------------------------------------------------')
    print('Welcome CT visualizer')
    print('developed 01/2023 by Martin Balcewicz (mail: martin.balcewicz@rockphysics.org)')
    print('-------------------------------------------------------------------------------------------------')
    print('-------------------------------------------------------------------------------------------------')
    print(' ')


def plot_slice(data, cmap_set=None, slice=None, plane='xy', subvolume=None, labels=None, title=None, voxel_size=None):
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

    if cmap_set is None:
        cmap_set = params.cmap
    else:
        cmap_set = cmap_set

    params.default_figure()

    # get the minimum and maximum values of the data
    vmin = np.amin(data)
    vmax = np.amax(data)

    if slice is not None:
        slice = slice
    else:
        slice = int(dimensions[0] / 2)

    if plane == 'yz':
        # create a new figure and axes using the default parameters
        fig = plt.figure(figsize=params.figsize)
        ax = fig.add_axes(params.x_axes_right)  # left, bottom, width, height

        im = ax.pcolormesh(data[:, :, slice], cmap=cmap_set, vmin=vmin, vmax=vmax)
        ax.set_aspect('equal', 'box')

        # Add a colorbar to the left of the plot
        cax = fig.add_axes(params.l_axes)  # left, bottom, width, height
        cbar = fig.colorbar(im, cax=cax, orientation='vertical')

        if labels is not None:
            cbar.ax.yaxis.set_label_position("right")
            cbar.set_ticks(np.arange(len(labels)))
            cbar.ax.set_yticklabels([labels[tick] for tick in np.arange(len(labels))])
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

            # Calculate the new tick labels based on the resolution and desired number of ticks
            if isinstance(voxel_size, int):
                # resolution is an integer
                xticklabels = [f'{int(tick * voxel_size)}' for tick in np.linspace(xticks[0], xticks[-1], 5)]
                yticklabels = [f'{int(tick * voxel_size)}' for tick in np.linspace(yticks[0], yticks[-1], 5)]
                ax.set_xlabel('Y-axis (µm)')
                ax.set_ylabel('Z-axis (µm)')
            else:
                # resolution is a float
                xticklabels = [f'{tick * voxel_size:.1f}' for tick in np.linspace(xticks[0], xticks[-1], 5)]
                yticklabels = [f'{tick * voxel_size:.1f}' for tick in np.linspace(yticks[0], yticks[-1], 5)]
                ax.set_xlabel('Y-axis (µm)')
                ax.set_ylabel('Z-axis (µm)')

            # Set the new tick locations and labels
            ax.xaxis.set_major_locator(FixedLocator(np.linspace(xticks[0], xticks[-1], 5)))
            ax.xaxis.set_major_formatter(FixedFormatter(xticklabels))
            ax.yaxis.set_major_locator(FixedLocator(np.linspace(yticks[0], yticks[-1], 5)))
            ax.yaxis.set_major_formatter(FixedFormatter(yticklabels))
        else:
            # Set the x-axis and y-axis titles
            ax.set_xlabel('Y-axis (voxel)')
            ax.set_ylabel('Z-axis (voxel)')

        # Add a title if given
        if title is not None:
            plt.title(f'{title}', fontsize=20, fontweight='bold', y=1.01, x=10.5, ha='center')

    elif plane == 'xz':
        # create a new figure and axes using the default parameters
        fig = plt.figure(figsize=params.figsize)
        ax = fig.add_axes(params.x_axes_left)  # left, bottom, width, height

        im = ax.pcolormesh(data[:, slice, :], cmap=cmap_set, vmin=vmin, vmax=vmax)
        ax.set_aspect('equal', 'box')

        # Add a colorbar to the right of the plot
        cax = fig.add_axes(params.r_axes)  # left, bottom, width, height
        cbar = fig.colorbar(im, cax=cax, orientation='vertical')

        if labels is not None:
            cbar.set_ticks(np.arange(len(labels)))
            # Use the label_dict to get the string corresponding to the numerical value
            cbar.ax.set_yticklabels([labels[tick] for tick in np.arange(len(labels))])
        else:
            cbar = fig.colorbar(im, cax=cax, orientation='vertical')
        cbar.ax.yaxis.tick_right()

        plt.axis('tight')

        # Move the y-axis to the left side
        ax.yaxis.tick_left()
        ax.yaxis.set_label_position("left")
        ax.spines["right"].set_visible(False)
        ax.spines["left"].set_visible(True)

        if voxel_size is not None:
            # Get the current tick locations
            xticks = ax.get_xticks()
            yticks = ax.get_yticks()

            # Calculate the new tick labels based on the resolution and desired number of ticks
            if isinstance(voxel_size, int):
                # resolution is an integer
                xticklabels = [f'{int(tick * voxel_size)}' for tick in np.linspace(xticks[0], xticks[-1], 5)]
                yticklabels = [f'{int(tick * voxel_size)}' for tick in np.linspace(yticks[0], yticks[-1], 5)]
                ax.set_xlabel('X-axis (µm)')
                ax.set_ylabel('Y-axis (µm)')
            else:
                # resolution is a float
                xticklabels = [f'{tick * voxel_size:.1f}' for tick in np.linspace(xticks[0], xticks[-1], 5)]
                yticklabels = [f'{tick * voxel_size:.1f}' for tick in np.linspace(yticks[0], yticks[-1], 5)]
                ax.set_xlabel('X-axis (µm)')
                ax.set_ylabel('Y-axis (µm)')

            # Set the new tick locations and labels
            ax.xaxis.set_major_locator(FixedLocator(np.linspace(xticks[0], xticks[-1], 5)))
            ax.xaxis.set_major_formatter(FixedFormatter(xticklabels))
            ax.yaxis.set_major_locator(FixedLocator(np.linspace(yticks[0], yticks[-1], 5)))
            ax.yaxis.set_major_formatter(FixedFormatter(yticklabels))
        else:
            # Set the x-axis and y-axis titles
            ax.set_xlabel('X-axis (voxel)')
            ax.set_ylabel('Z-axis (voxel)')

        # Add a title if given
        if title is not None:
            plt.title(f'{title}', fontsize=20, fontweight='bold', y=1.01, x=-10.5, ha='center')

    elif plane == 'xy':
        # create a new figure and axes using the default parameters
        fig = plt.figure(figsize=params.figsize)
        ax = fig.add_axes(params.x_axes_right)

        im = ax.pcolormesh(data[slice, :, :], cmap=cmap_set, vmin=vmin, vmax=vmax)
        ax.set_aspect('equal', 'box')

        # Add a colorbar to the left of the plot
        cax = fig.add_axes(params.l_axes)  # left, bottom, width, height
        cbar = fig.colorbar(im, cax=cax, orientation='vertical')

        # # Set the ticks on the colorbar
        # cbar.set_ticks(np.linspace(vmin, vmax, num=6))
        #
        # # Set the tick labels to the corresponding values
        # tick_labels = [vmin] + [f"{v:.2f}" for v in np.linspace(vmin, vmax, num=4)] + [vmax]
        # cbar.ax.set_yticklabels(tick_labels)

        if labels is not None:
            cbar.set_ticks(np.arange(len(labels)))
            # Use the label_dict to get the string corresponding to the numerical value
            cbar.ax.set_yticklabels([labels[tick] for tick in np.arange(len(labels))])
        else:
            pass

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

            # Calculate the new tick labels based on the resolution and desired number of ticks
            if isinstance(voxel_size, int):
                # resolution is an integer
                xticklabels = [f'{int(tick * voxel_size)}' for tick in np.linspace(xticks[0], xticks[-1], 5)]
                yticklabels = [f'{int(tick * voxel_size)}' for tick in np.linspace(yticks[0], yticks[-1], 5)]
                ax.set_xlabel('X-axis (µm)')
                ax.set_ylabel('Y-axis (µm)')
            else:
                # resolution is a float
                xticklabels = [f'{tick * voxel_size:.1f}' for tick in np.linspace(xticks[0], xticks[-1], 5)]
                yticklabels = [f'{tick * voxel_size:.1f}' for tick in np.linspace(yticks[0], yticks[-1], 5)]
                ax.set_xlabel('X-axis (µm)')
                ax.set_ylabel('Y-axis (µm)')

            # Set the new tick locations and labels
            ax.xaxis.set_major_locator(FixedLocator(np.linspace(xticks[0], xticks[-1], 5)))
            ax.xaxis.set_major_formatter(FixedFormatter(xticklabels))
            ax.yaxis.set_major_locator(FixedLocator(np.linspace(yticks[0], yticks[-1], 5)))
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








def save_figure(figure, name, format=None, dpi=None):
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
