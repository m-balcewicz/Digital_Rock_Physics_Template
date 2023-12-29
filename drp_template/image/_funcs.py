import glob
import os
import numpy as np
import drp_template.bin.default_parameters as params
from drp_template.default_params import read_parameters_file, check_output_folder
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib.ticker import FixedLocator, FixedFormatter
from cmcrameri import cm

__all__ = [
    'plot_slice',
    'save_figure2',
    'plot_histogram',
    'plot_effective_modulus'
]

# S E T T I N G S
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



def plot_slice(data, paramsfile='parameters.json', cmap_set=None, slice=None, plane='xy', subvolume=None, labels=None,
               title=None, voxel_size=None, dark_mode=True):
    """
    Visualize 2D slice of 3D volumetric data using Matplotlib.

    Parameters:
    -----------
    data : 3D numpy array
        The volumetric data to be visualized.
    paramsfile : str, optional (default='parameters.json')
        Name of the JSON file containing plotting parameters.
    cmap_set : Matplotlib colormap, optional (default=None)
        The colormap to be used for the plot. If not specified, the default colormap (`batlow`) will be used.
    slice : int, optional (default=None)
        The index of the slice along the specified plane. If not provided, the default slice index is set to the middle slice.
    plane : str, optional (default='xy')
        The plane along which the slice will be visualized. Valid values are 'xy', 'yz', or 'xz'.
    subvolume : int or float, optional (default=None)
        Specifies a subvolume indicated in the figure.
    labels : list of str, optional (default=None)
        Labels for the colorbar. Can be a single string or a list.
    title : str, optional (default=None)
        The title of the plot.
    voxel_size : int of floats, optional (default=None)
        The size of the voxels along each dimension.
    dark_mode : bool, optional (default=True)
        If True, set a dark background; otherwise, set a light background.

    Returns:
    --------
    fig : Matplotlib Figure
        The Matplotlib figure object.
    ax : Matplotlib Axes
        The Matplotlib axes object.

    Examples:
    ---------
    ```python
    import numpy as np
    from plot_slice import plot_slice

    # Generate example data
    data = np.random.rand(50, 100, 200)

    # Plot XY plane slice
    fig, ax = plot_slice(data, cmap_set='viridis', slice=10, plane='xy', title='XY Plane slice')
    plt.show()
    ```

    Notes:
    ------
    - The function reads default plotting parameters from a JSON file. Make sure to provide a valid path to the JSON file or use the default if not specified.
    - The colormap (`cmap_set`) can be either a Matplotlib colormap or a string specifying the colormap name.
    - The `subvolume` parameter draws a rectangle around a specified subvolume if provided.
    - The `labels` parameter can be used to customize colorbar ticks.

    """
    # Get basic info about data
    dimensions = data.shape
    center = np.array([dimensions[0] / 2, dimensions[0] / 2])

    # Set color scheme based on dark_mode
    if dark_mode:
        text_color = 'white'
        face_color = 'black'
        edge_color = 'white'
    else:
        text_color = 'black'
        face_color = 'white'
        edge_color = 'black'

    if cmap_set is None:
        # Get the default colormap
        cmap_set = default_figure_settings.get('colormap')
        # Evaluate the string to get the actual colormap function
        cmap_set = eval(cmap_set)

    # Create a figure and axis with adjusted font family and size
    fig, ax = plt.subplots(figsize=(fig_width, fig_height), facecolor=face_color, edgecolor=edge_color)
    fig.set_facecolor(face_color)

    if plane == 'xy':
        if slice is None:
            nz = read_parameters_file(paramsfile=paramsfile, paramsvars='nz')
            slice = (nz // 2) - 1

        data = data[:, :, slice]
    elif plane == 'yz':
        if slice is None:
            nx = read_parameters_file(paramsfile=paramsfile, paramsvars='nx')
            slice = (nx // 2) - 1

        data = data[slice, :, :]
    elif plane == 'xz':
        if slice is None:
            ny = read_parameters_file(paramsfile=paramsfile, paramsvars='ny')
            slice = (ny // 2) - 1

        data = data[:, slice, :]
    else:
        raise ValueError("Invalid plane. Use 'xy', 'yz', or 'xz'.")

    # Transpose the slice to swap dimensions
    data = data.T

    pcm = ax.pcolormesh(data, cmap=cmap_set)

    plt.axis('tight')
    ax.set_aspect('equal', 'box')

    # Set labels and title
    if plane == 'xy':
        # Set labels and title with adjusted font size and family
        ax.set_xlabel('X-axis', color=text_color, fontsize=plt.rcParams['font.size'], fontfamily=plt.rcParams['font.family'])
        ax.set_ylabel('Y-axis', color=text_color, fontsize=plt.rcParams['font.size'], fontfamily=plt.rcParams['font.family'])

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
        cax_left = subplot_left - (subplot_left * cax_space_left)
        cax = fig.add_axes([cax_left, cax_bottom, cax_width, cax_height])  # left, bottom, width, height
        cbar = fig.colorbar(pcm, cax=cax, orientation='vertical')

        # Move the colorbar spines to the left
        cbar.ax.yaxis.set_ticks_position('left')
        cbar.ax.yaxis.set_label_position('left')
    elif plane == 'yz':
        ax.set_xlabel('Y-axis', color=text_color, fontsize=plt.rcParams['font.size'], fontfamily=plt.rcParams['font.family'])
        ax.set_ylabel('Z-axis', color=text_color, fontsize=plt.rcParams['font.size'], fontfamily=plt.rcParams['font.family'])

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
        cax_left = subplot_left - (subplot_left * cax_space_left)
        cax = fig.add_axes([cax_left, cax_bottom, cax_width, cax_height])  # left, bottom, width, height
        cbar = fig.colorbar(pcm, cax=cax, orientation='vertical')

        # Move the colorbar spines to the left
        cbar.ax.yaxis.set_ticks_position('left')
        cbar.ax.yaxis.set_label_position('left')
    elif plane == 'xz':
        ax.set_xlabel('X-axis', color=text_color, fontsize=plt.rcParams['font.size'], fontfamily=plt.rcParams['font.family'])
        ax.set_ylabel('Z-axis', color=text_color, fontsize=plt.rcParams['font.size'], fontfamily=plt.rcParams['font.family'])

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
        cax_right = subplot_right + (subplot_right * cax_space_right)
        cax = fig.add_axes([cax_right, cax_bottom, cax_width, cax_height])  # left, bottom, width, height
        cbar = fig.colorbar(pcm, cax=cax, orientation='vertical')

        # Move the colorbar spines to the right
        cbar.ax.yaxis.set_ticks_position('right')
        cbar.ax.yaxis.set_label_position('right')

    if title is None:
        title = ax.set_title(im_title, color=text_color, fontsize=plt.rcParams['font.size'], fontfamily=plt.rcParams['font.family'])
    else:
        title = ax.set_title(title, color=text_color, fontsize=plt.rcParams['font.size'], fontfamily=plt.rcParams['font.family'])
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

    # Add subvolume rectangle if given
    if subvolume is not None:
        rect = plt.Rectangle(center - subvolume / 2, subvolume, subvolume, fill=False, linewidth=2, edgecolor='r')
        ax.add_patch(rect)

    # Add slice number as text in the bottom right corner
    slice_text = f"slice: {slice}"
    text_box = ax.text(
        0.95,
        0.05,
        slice_text,
        transform=ax.transAxes,
        color='white',
        ha='right',
        va='bottom',
        fontsize=14,  # Adjust the fontsize as needed
        bbox=dict(facecolor='gray', alpha=0.5, pad=5)
    )

    return fig, ax


def plot_histogram(data, paramsfile='parameters.json', dtype=None, cmap_set=None, title=None, log_scale='both', dark_mode=True):
    """
    Plot a histogram of gray-scale intensities.

    Parameters:
    -----------
    data : numpy array
        1D array containing gray-scale intensities.
    dtype : str, optional (default=None)
        Data type of the input array. If not provided, it is read from the parameters file.
    cmap_set : Matplotlib colormap or str, optional (default=None)
        The colormap to be used for the plot. If not specified, the default colormap is used.
    title : str, optional (default=None)
        The title of the plot.
    log_scale : {'both', 'x', 'y'}, optional (default='both')
        Specifies whether to apply log scale to both axes ('both'), only the x-axis ('x'), or only the y-axis ('y').
    dark_mode : bool, optional (default=True)
        If True, set a dark background; otherwise, set a light background.
    paramsfile : str, optional (default='parameters.json')
        Name of the JSON file containing plotting parameters.

    Returns:
    --------
    fig : Matplotlib Figure
        The Matplotlib figure object.
    ax : Matplotlib Axes
        The Matplotlib axes object.

    Examples:
    ---------
    ```python
    import numpy as np
    from plot_histogram import plot_histogram

    # Generate example data
    data = np.random.randint(0, 255, 1000)

    # Plot histogram with default settings
    fig, ax = plot_histogram(data)
    plt.show()
    ```

    Notes:
    ------
    - If `dtype` is not provided, it is read from the parameters file.
    - The `cmap_set` parameter can be either a Matplotlib colormap or a string specifying the colormap name.
    - The `log_scale` parameter controls whether to apply log scale to the x-axis, y-axis, both, or neither.
    - The function reads default plotting parameters from a JSON file. Make sure to provide a valid path to the JSON file or use the default if not specified.
    - Adjust the `paramsfile` parameter based on your specific file path.

    """
    # Set dtype based on the parameters file if not provided
    if dtype is None:
        dtype = read_parameters_file(paramsfile=paramsfile, paramsvars='dtype')

    # Determine gray_max based on dtype
    gray_max = 255 if dtype == 'uint8' else 65535

    # Set default colormap if not specified
    if cmap_set is None:
        cmap_set = default_figure_settings.get('colormap')
        cmap_set = eval(cmap_set)

    # Set color scheme based on dark_mode
    if dark_mode:
        text_color, face_color, edge_color = 'white', 'black', 'white' 
    else:
        text_color, face_color, edge_color = 'black', 'white', 'black'

    # Calculate histogram bins using Freedman-Diaconis rule
    iqr = np.percentile(data, 75) - np.percentile(data, 25)
    bins_width = 2 * iqr / (len(data) ** (1 / 3))
    bins = np.arange(0, gray_max + bins_width, bins_width)

    # Compute histogram of gray-scale intensities
    hist, bins = np.histogram(data, bins=bins, range=(0, gray_max))

    # Create a color map for the histogram bars
    cmap = plt.cm.get_cmap(cmap_set)
    colors = cmap(np.linspace(0, 1, len(bins) - 1))

    # Plot histogram using colored bars
    fig, ax = plt.subplots(figsize=(fig_width, fig_height), facecolor=face_color, edgecolor=edge_color)
    ax.bar(bins[:-1], hist, width=bins_width, color=colors, linewidth=0.5, edgecolor=None) # no edgecolor for the bars

    # Apply log scale based on the log_scale parameter
    if log_scale == 'both':
        ax.set_xscale('log')
        ax.set_yscale('log')
    elif log_scale == 'x':
        ax.set_xscale('log')
    elif log_scale == 'y':
        ax.set_yscale('log')

    # Set labels and title with adjusted font size
    font_size = plt.rcParams['font.size']
    ax.set_xlabel('Gray-scale intensity', color=text_color, fontsize=font_size)
    ax.set_ylabel('Frequency', color=text_color, fontsize=font_size)

    # Set title with adjusted font size
    title_text = 'Histogram' if title is None else title
    ax.set_title(title_text, color=text_color, fontsize=font_size)

    # Set tick parameters with adjusted font size
    ax.tick_params(axis='both', which='both', direction='in', labelsize=font_size, colors=text_color)

    # Set spines edge color for the entire subplot
    for spine in ax.spines.values():
        spine.set_edgecolor(edge_color)

    # Set background color
    ax.set_facecolor(face_color)

    return fig, ax


# def compare_histograms(data_list, data_vars, dtype='uint16', cmap_set=None):
#     if dtype == 'uint8':
#         gray_max = 255
#     elif dtype == 'uint16':
#         gray_max = 65535
#
#     if cmap_set is None:
#         cmap_set = params.cmap
#     else:
#         cmap_set = cmap_set
#
#     params.default_figure()
#
#     # Calculate maximum number of data points for histogram
#     # max_data_points = max(len(np.unique(data)) for data in data_list)
#     # bins_guess = int(np.sqrt(max_data_points))
#     bins_guess = 255
#
#     # Create a color map for the line plot
#     colors = cmap_set(np.linspace(0, 1, len(data_list)))
#
#     fig = plt.figure(figsize=params.figsize)
#     ax = fig.add_axes(params.x_axes_right)  # left, bottom, width, height
#
#     for i, data in enumerate(data_list):
#         print(f'calculating bins . . . for {data_vars[i]}')
#         # Compute histogram of gray-scale intensities
#         hist, bins = np.histogram(data, bins=bins_guess, range=(0, gray_max))
#
#         # Plot histogram as a line plot
#         # color = plt.cm.get_cmap('hsv')(i / len(data_list))
#         ax.plot(bins[:-1], hist, color=colors[i], linewidth=params.linewidth, label=f'{data_vars[i]}')
#
#     ax.set_yscale('log')  # Set y-axis to logarithmic scale
#     ax.set_xlabel('Gray-scale intensity')
#     ax.set_ylabel('Frequency')
#
#     # create the legend and set its appearance
#     leg = plt.legend(loc='upper right', frameon=True)
#     for line in leg.get_lines():
#         line.set_linewidth(5.0)  # set the width of each legend line
#
#     return fig
#
#
# def shift_histogram(data_list, data_vars, data_ref, dtype='uint16', cmap_set=None, xlim=None, ylim=None, mask=None):
#     if dtype == 'uint8':
#         gray_max = 255
#     elif dtype == 'uint16':
#         gray_max = 65535
#
#     if cmap_set is None:
#         cmap_set = params.cmap
#     else:
#         cmap_set = cmap_set
#
#     params.default_figure()
#
#     # Calculate maximum number of data points for histogram
#     # max_data_points = max(len(np.unique(data)) for data in data_list)
#     # bins_guess = int(np.sqrt(max_data_points))
#     bins_guess = 255
#
#     # Create a color map for the line plot
#     colors = cmap_set(np.linspace(0, 1, len(data_list)))
#
#     fig = plt.figure(figsize=params.figsize)
#     ax = fig.add_axes(params.x_axes_right)  # left, bottom, width, height
#
#     for i, data in enumerate(data_list):
#         print(f'calculating bins . . . for {data_vars[i]}')
#         # Compute histogram of gray-scale intensities
#         hist, bins = np.histogram(data, bins=bins_guess, range=(0, gray_max))
#
#         # Plot histogram as a line plot
#         # color = plt.cm.get_cmap('hsv')(i / len(data_list))
#         ax.plot(bins[:-1], hist, color=colors[i], linewidth=params.linewidth, label=f'{data_vars[i]}')
#
#     ax.set_yscale('log')  # Set y-axis to logarithmic scale
#     ax.set_xlabel('Gray-scale intensity')
#     ax.set_ylabel('Frequency')
#
#     # create the legend and set its appearance
#     leg = plt.legend(loc='upper right', frameon=True)
#     for line in leg.get_lines():
#         line.set_linewidth(5.0)  # set the width of each legend line
#
#     if xlim is None and ylim is None:
#         plt.xlim([40000, 60000])
#         plt.ylim([10e3, 10e4])
#     elif isinstance(xlim, list) and len(xlim) == 2 and isinstance(xlim[0], (int, float)) and isinstance(xlim[1], (int, float)) and \
#             isinstance(ylim, list) and len(ylim) == 2 and isinstance(ylim[0], (int, float)) and isinstance(ylim[1], (int, float)):
#         plt.xlim(xlim)
#         plt.ylim(ylim)
#     else:
#         raise ValueError("xlim and ylim must be lists of two integers.")
#
#     if mask is None:
#         raise ValueError("Please provide a mask value")
#     elif isinstance(mask, list) and len(mask) == 2 and isinstance(mask[0], int) and isinstance(mask[1], int) and mask[0] < mask[1]:
#         # Find the minimum and maximum values within the specified mask
#         data_masked = np.ma.masked_where((data_ref < mask[0]) | (data_ref > mask[1]), data_list[0])
#         data_min = np.min(data_masked)
#         data_max = np.max(data_masked)
#
#         # Find the most common value within the masked data
#         data_flat = data_masked.flatten()
#         bincount = np.bincount(data_flat)
#         data_mode = np.argmax(bincount)
#
#         max = data_min + data_mode
#
#         print(f'data min in masked array: {data_min}')
#         print(f'data max in masked array: {data_max}')
#         print(f'data mode in masked array: {data_mode}')
#         print(f'max in masked array: {max}')
#
#         # Add vertical lines for the minimum and maximum values
#         plt.axvline(x=max, color='g')
#
#     else:
#         raise ValueError("Mask must be a list of two integers with the first value smaller than the second value.")
#
#     return fig


def plot_effective_modulus(phi, modulus, data, types='avg', dark_mode=False, fig_width=8, fig_height=6):
    """
    Plot effective modulus against porosity.

    Parameters:
    - phi (numpy.ndarray): Array of porosity values.
    - modulus (str): Modulus type, e.g., 'bulk' or 'shear'.
    - data (dict): Dictionary containing modulus data.
                   Example: {'voigt': voigt_data, 'reuss': reuss_data, 'hs_upper': hs_upper_data, 'hs_lower': hs_lower_data, 'avg': avg_data}
                   where voigt_data, reuss_data, hs_upper_data, hs_lower_data, and avg_data are arrays of modulus values.
    - types (str or list): Type or list of types of modulus to plot. Options: 'voigt', 'reuss', 'hs_upper', 'hs_lower', 'avg'.
                          You can also pass a list of types to plot multiple types.
                          If 'all' is passed, it will plot all available types.
    - dark_mode (bool): Use dark color scheme if True, else use light color scheme.
    - fig_width (float): Width of the figure.
    - fig_height (float): Height of the figure.
    
    Returns:
    - fig (matplotlib.figure.Figure): The matplotlib figure.
    - ax (matplotlib.axes._subplots.AxesSubplot): The matplotlib axes.
    """   
    if dark_mode:
        text_color, face_color, edge_color = 'white', 'black', 'white'
    else:
        text_color, face_color, edge_color = 'black', 'white', 'black'
    
    fig, ax = plt.subplots(figsize=(fig_width, fig_height), facecolor=face_color, edgecolor=edge_color)
    
    color1 = face_color
    color2 = 'tomato' if dark_mode else 'darkred'
    
    title = f"Effective {modulus.capitalize()} Modulus ($GPa$)"
    ax.set_title(title, color=text_color)
    
    if types == 'all':
        types = ['voigt', 'reuss', 'hs_upper', 'hs_lower', 'avg']
    elif isinstance(types, str):
        types = [types]

    for mod_type in types:
        modulus_values = np.array(data[mod_type])
        labels = {
            'voigt': 'Voigt Upper Bound',
            'reuss': 'Reuss Lower Bound',
            'hs_upper': 'Hashin–Shtrikman Upper Bound',
            'hs_lower': 'Hashin–Shtrikman Lower Bound',
            'avg': 'Voigt-Reuss-Hill Average',
        }
        
        marker_style = {'voigt': '-', 'reuss': '-', 'hs_upper': 'dashed', 'hs_lower': '-.', 'avg': '-'}
        
        ax.plot(phi, modulus_values, label=labels[mod_type], linestyle=marker_style[mod_type], marker='o', markersize=4, markerfacecolor=face_color, markeredgecolor=edge_color)

    ax.set_xlabel("Porosity", color=text_color)
    ax.set_ylabel(f"{modulus.capitalize()} Modulus", color=text_color)
    ax.legend()
    ax.tick_params(axis='y', colors=text_color)
    ax.xaxis.set_major_formatter(plt.PercentFormatter(1.00))  # convert x-axis into percent
    plt.xlim([0, 1])
    
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

    # Check output folder
    output_path = check_output_folder()

    if filename is None:
        # Find the highest existing index
        existing_files = glob.glob(os.path.join(output_path, "figure_*.png"))
        existing_indices = [int(os.path.basename(name).split("_")[1].split(".")[0]) for name in existing_files]
        highest_index = max(existing_indices, default=0)

        # Increment the index for the new file
        new_index = highest_index + 1

        # Format the index with leading zeros using %
        index_formatted = f"{new_index:03d}"

        # Use the index in the filename
        filename = os.path.join(output_path, f"figure_{index_formatted}")

    else:
        # Use the index in the filename
        filename = os.path.join(output_path, filename)

    # Save the figure
    full_path = f"{filename}.{format}"
    figure.savefig(full_path, dpi=dpi)

    if log:
        print(f"Figure saved at: {os.path.abspath(full_path)}")