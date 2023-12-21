import glob
import os
import numpy as np
import barbara.default_parameters as params
from barbara.default_params import read_parameters_file
import matplotlib.pyplot as plt
from matplotlib.ticker import FixedLocator, FixedFormatter
from cmcrameri import cm


__all__ = [
    "plot_slice2",
    "save_figure2"
]


def plot_slice2(data, paramsfile='parameters.json', cmap_set=None, layer=None, plane='xy', subvolume=None, labels=None, title=None, voxel_size=None, dark_mode=True):
    """
    Visualize 2D slices of 3D volumetric data using Matplotlib.

    Parameters:
    -----------
    data : 3D numpy array
        The volumetric data to be visualized.
    paramsfile : str
        Name of the JSON file. Default is 'parameters.json'.
    cmap_set : Matplotlib colormap, optional (default=None)
        The colormap to be used for the plot. If not specified, the default colormap (`batlow`) will be used.
    slice : int, optional (default=None)
        The index of the slice along the specified plane. If not provided, the default slice index is set to 0.
    plane : str, optional (default='xy')
        The plane along which the slice will be visualized. Valid values are 'xy', 'yz', or 'xz'.
    subvolume : tuple of slices, optional (default=None)
        Specifies a subvolume of the data to visualize. It should be a tuple of slices along each dimension (e.g., `(slice(0, 10), slice(None), slice(20, 30))`).
    labels : list of str, optional (default=None)
        Labels for each axis. If provided, it should be a list containing three strings corresponding to the X, Y, and Z axes.
    title : str, optional (default=None)
        The title of the plot.
    voxel_size : tuple of floats, optional (default=None)
        The size of the voxels along each dimension. If provided, it should be a tuple of three floats.

    Returns:
    --------
    fig : Matplotlib Figure
        The Matplotlib figure object.
    ax : Matplotlib Axes
        The Matplotlib axes object.

    Usage Example:
    --------------
    ```python
    import numpy as np
    from plot_slice2 import plot_slice2

    # Generate example data
    data = np.random.rand(50, 100, 200)

    # Plot XY plane slice
    fig, ax = plot_slice2(data, cmap_set='viridis', slice=10, plane='xy', title='XY Plane Slice')
    plt.show()
    ```

    Adjust the parameters based on your specific use case.
    """
    
    # SETTINGS
    # Get the directory of the currently executing script (your module or package)
    package_directory = os.path.dirname(os.path.abspath(__file__))

    # Construct the relative path to the JSON file
    relative_path = os.path.join('..', 'default_params', 'default_figure_settings.json')

    # Combine the package directory and the relative path to get the absolute path
    json_file_path = os.path.join(package_directory, relative_path)

    default_figure_settings = read_parameters_file(paramsfile=json_file_path, paramsvars=None)
    im_left = default_figure_settings.get('im_left')
    im_left_xz = default_figure_settings.get('im_left_xz')
    im_right = default_figure_settings.get('im_right')
    im_bottom = default_figure_settings.get('im_bottom')
    im_width = default_figure_settings.get('im_width')
    im_height = default_figure_settings.get('im_height')
    cax_width = default_figure_settings.get('cax_width')
    fig_width = default_figure_settings.get('fig_width')
    fig_height = default_figure_settings.get('fig_height')
    cax_space_left = default_figure_settings.get('cax_space_left')
    cax_space_right = default_figure_settings.get('cax_space_right')
    im_title = default_figure_settings.get('im_title')
    plt.rcParams['font.size'] = default_figure_settings.get('font_size')
    plt.rcParams['font.family'] = default_figure_settings.get('font_family')

    if dark_mode:
        text_color = 'white'
        face_color = 'black'
    else:
        text_color = 'black'
        face_color = 'white'

    if cmap_set is None:
        # Get the default colormap
        cmap_set = default_figure_settings.get('colormap')
        # Evaluate the string to get the actual colormap function
        cmap_set = eval(cmap_set)

    # Create a figure and axis
    fig, ax = plt.subplots(figsize=(fig_width, fig_height))  # width, height

    # Set the background color
    fig.set_facecolor(face_color)

    if plane == 'xy':
        if layer is None:
            nz = read_parameters_file(paramsfile=paramsfile, paramsvars='nz')
            layer = (nz//2)-1

        data = data[:, :, layer]
    elif plane == 'yz':
        if layer is None:
            nx = read_parameters_file(paramsfile=paramsfile, paramsvars='nx')
            layer = (nx//2)-1

        data = data[layer, :, :]
    elif plane == 'xz':
        if layer is None:
            ny = read_parameters_file(paramsfile=paramsfile, paramsvars='ny')
            layer = (ny//2)-1
            
        data = data[:, layer, :]
    else:
        raise ValueError("Invalid plane. Use 'xy', 'yz', or 'xz'.")

    # Transpose the slice to swap dimensions
    data = data.T
    
    pcm = ax.pcolormesh(data, cmap=cmap_set)

    plt.axis('tight')
    ax.set_aspect('equal', 'box')

    # Set labels and title
    if plane == 'xy':
        ax.set_xlabel('X-axis', color=text_color)
        ax.set_ylabel('Y-axis', color=text_color)
        
        ax.yaxis.tick_right()
        ax.yaxis.set_label_position("right")
        ax.spines["right"].set_visible(True)

        # Move the y-axis to the right side
        ax.invert_xaxis()

        # Set the color of the tick values to white
        ax.tick_params(axis='both', colors=text_color)

        # Add a colorbar to the left of the plot
        # Get the position of the subplot area in figure coordinates
        subplot_position = ax.get_position()

        new_position = [im_left, im_bottom, im_width, im_height]  # left, bottom, width, height
        ax.set_position(new_position)

        # Get the positions of the subplot area
        subplot_height = ax.get_position().height
        subplot_bottom = ax.get_position().y0
        subplot_left = ax.get_position().x0
        
        # Set the colorbar position to match the subplot area
        cax_height = subplot_height
        cax_bottom = subplot_bottom
        cax_left = subplot_left - (subplot_left*cax_space_left)
        cax = fig.add_axes([cax_left, cax_bottom, cax_width, cax_height])  # left, bottom, width, height
        cbar = fig.colorbar(pcm, cax=cax, orientation='vertical')

        # Move the colorbar spines to the left
        cbar.ax.yaxis.set_ticks_position('left')
        cbar.ax.yaxis.set_label_position('left')
    elif plane == 'yz':
        ax.set_xlabel('Y-axis', color=text_color)
        ax.set_ylabel('Z-axis', color=text_color)
        
        ax.yaxis.tick_right()
        ax.yaxis.set_label_position("right")
        ax.spines["right"].set_visible(True)
        
        # Move the y-axis to the right side
        ax.invert_xaxis()  
        # Set the color of the tick values to white
        ax.tick_params(axis='both', colors=text_color)

        # Add a colorbar to the left of the plot
        # Get the position of the subplot area in figure coordinates
        subplot_position = ax.get_position()

        new_position = [im_left, im_bottom, im_width, im_height]  # left, bottom, width, height
        ax.set_position(new_position)

        # Get the positions of the subplot area
        subplot_height = ax.get_position().height
        subplot_bottom = ax.get_position().y0
        subplot_left = ax.get_position().x0
        
        # Set the colorbar position to match the subplot area
        cax_height = subplot_height
        cax_bottom = subplot_bottom
        cax_left = subplot_left - (subplot_left*cax_space_left)
        cax = fig.add_axes([cax_left, cax_bottom, cax_width, cax_height])  # left, bottom, width, height
        cbar = fig.colorbar(pcm, cax=cax, orientation='vertical')

        # Move the colorbar spines to the left
        cbar.ax.yaxis.set_ticks_position('left')
        cbar.ax.yaxis.set_label_position('left')              
    elif plane == 'xz':
        ax.set_xlabel('X-axis', color=text_color)
        ax.set_ylabel('Z-axis', color=text_color)

        ax.yaxis.tick_left()
        ax.yaxis.set_label_position("left")
        ax.spines["left"].set_visible(True)
        # Set the color of the tick values to white
        ax.tick_params(axis='both', colors=text_color)

        # Add a colorbar to the left of the plot
        # Get the position of the subplot area in figure coordinates
        subplot_position = ax.get_position()

        new_position = [im_left_xz, im_bottom, im_width, im_height]  # left, bottom, width, height
        ax.set_position(new_position)

        # Get the positions of the subplot area
        subplot_height = ax.get_position().height
        subplot_bottom = ax.get_position().y0
        subplot_left = ax.get_position().x0
        subplot_right = subplot_left + ax.get_position().width
        
        # Set the colorbar position to match the subplot area
        cax_height = subplot_height
        cax_bottom = subplot_bottom
        cax_right = subplot_right + (subplot_right*cax_space_right)
        cax = fig.add_axes([cax_right, cax_bottom, cax_width, cax_height])  # left, bottom, width, height
        cbar = fig.colorbar(pcm, cax=cax, orientation='vertical')

        # Move the colorbar spines to the right
        cbar.ax.yaxis.set_ticks_position('right')
        cbar.ax.yaxis.set_label_position('right')

    title = ax.set_title(im_title, color=text_color)
    title.set_position((0.5, 1.0))  # Set the position in axes coordinates

    # Set the text color of the colormap
    for label in cbar.ax.get_yticklabels():
        label.set_color(text_color)

    # Set the color of the colorbar ticks to white
    cbar.ax.tick_params(axis='y', colors=text_color)
    
    if voxel_size is not None:
        # Get the current tick locations
        xticks = ax.get_xticks()
        yticks = ax.get_yticks()

        # Calculate the new tick labels based on the resolution and desired number of ticks
        if isinstance(voxel_size, int):
            # resolution is an integer
            xticklabels = [f'{int(tick * voxel_size)}' for tick in np.linspace(xticks[0], xticks[-1], 5)]
            yticklabels = [f'{int(tick * voxel_size)}' for tick in np.linspace(yticks[0], yticks[-1], 5)]
            # Get the current X-axis and Y-axis labels
            xlabel = ax.get_xlabel()
            ylabel = ax.get_ylabel()

            # Append the suffix "(µm)" to the labels
            xlabel += ' (µm)'
            ylabel += ' (µm)'

            # Set the new X-axis and Y-axis labels
            ax.set_xlabel(xlabel)
            ax.set_ylabel(ylabel)
        else:
            # resolution is a float
            xticklabels = [f'{tick * voxel_size:.1f}' for tick in np.linspace(xticks[0], xticks[-1], 5)]
            yticklabels = [f'{tick * voxel_size:.1f}' for tick in np.linspace(yticks[0], yticks[-1], 5)]
            # Get the current X-axis and Y-axis labels
            xlabel = ax.get_xlabel()
            ylabel = ax.get_ylabel()

            # Append the suffix "(µm)" to the labels
            xlabel += ' (µm)'
            ylabel += ' (µm)'

            # Set the new X-axis and Y-axis labels
            ax.set_xlabel(xlabel)
            ax.set_ylabel(ylabel)

        # Set the new tick locations and labels
        ax.xaxis.set_major_locator(FixedLocator(np.linspace(xticks[0], xticks[-1], 5)))
        ax.xaxis.set_major_formatter(FixedFormatter(xticklabels))
        ax.yaxis.set_major_locator(FixedLocator(np.linspace(yticks[0], yticks[-1], 5)))
        ax.yaxis.set_major_formatter(FixedFormatter(yticklabels))
    else:
        # Set the x-axis and y-axis labels
            # Get the current X-axis and Y-axis labels
            xlabel = ax.get_xlabel()
            ylabel = ax.get_ylabel()

            # Append the suffix "(µm)" to the labels
            xlabel += ' (voxel)'
            ylabel += ' (voxel)'

            # Set the new X-axis and Y-axis labels
            ax.set_xlabel(xlabel)
            ax.set_ylabel(ylabel)
        
    if labels is not None:
        cbar.set_ticks(np.arange(len(labels)))
        # Use the label_dict to get the string corresponding to the numerical value
        cbar.ax.set_yticklabels([labels[tick] for tick in np.arange(len(labels))])
    

    return fig, ax



def save_figure2(figure, filename=None, format="png", dpi=300, log=True):
    """
    Save a Matplotlib figure.

    Parameters:
    -----------
    figure : matplotlib.figure.Figure
        The Matplotlib figure to be saved.
    filename : str, optional
        The base filename (without extension). If not provided, an incremental index will be used.
    format : str, optional
        The file format (e.g., "png", "pdf", "svg"). Default is "png".
    dpi : int, optional
        The dots per inch (resolution) of the saved figure. Default is 300.
    log : bool, optional
        If True, print the full path where the figure is saved. Default is True.
    """

    if filename is None:
        # Find the highest existing index
        existing_files = glob.glob("figure_*.png")
        existing_indices = [int(name.split("_")[1].split(".")[0]) for name in existing_files]
        highest_index = max(existing_indices, default=0)

        # Increment the index for the new file
        new_index = highest_index + 1

        # Format the index with leading zeros using %
        index_formatted = f"{new_index:03d}"

        # Use the index in the filename
        filename = f"figure_{index_formatted}"

    # Save the figure
    full_path = os.path.join(filename + "." + format)
    figure.savefig(full_path, dpi=dpi)

    if log:
            print(f"Figure saved at: {os.path.abspath(full_path)}")

