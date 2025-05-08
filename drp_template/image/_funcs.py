import glob
import os
import numpy as np
import drp_template.bin.default_parameters as params
from drp_template.default_params import read_parameters_file, check_output_folder
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
from matplotlib.colors import ListedColormap
from matplotlib.ticker import FixedLocator, FixedFormatter
from cmcrameri import cm

__all__ = [
    'ortho_slice',
    'ortho_views',
    'add_slice_reference_lines',
    'save_figure2',
    'histogram',
    'plot_effective_modulus'
]

# S E T T I N G S
# Get the directory of the currently executing script (your module or package)
package_directory = os.path.dirname(os.path.abspath(__file__))
# Construct the relative path to the JSON file
relative_path = os.path.join('..','default_params','default_figure_settings.json')
# Combine the package directory and the relative path to get the absolute path
json_file_path = os.path.join(package_directory, relative_path)
default_figure_settings = read_parameters_file(paramsfile=json_file_path, paramsvars=None)

# Access global settings from the nested structure
global_settings = default_figure_settings.get('global_settings', default_figure_settings)

im_left = global_settings.get('im_left')
im_left_xz = global_settings.get('im_left_xz')
im_right = global_settings.get('im_right')
im_bottom = global_settings.get('im_bottom')
im_width = global_settings.get('im_width')
im_height = global_settings.get('im_height')
cax_width = global_settings.get('cax_width')
fig_width = global_settings.get('fig_width')
fig_height = global_settings.get('fig_height')
cax_space_left = global_settings.get('cax_space_left')
cax_space_right = global_settings.get('cax_space_right')
im_title = global_settings.get('im_title')
plt.rcParams['font.size'] = global_settings.get('font_size')
plt.rcParams['font.family'] = global_settings.get('font_family')



def ortho_slice(data, paramsfile='parameters.json', cmap_set=None, slice=None, plane='xy', subvolume=None, labels=None,
               title=None, voxel_size=None, dark_mode=True, cmap_intensity=1.0, ax=None, show_colorbar=True):
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
    show_colorbar : bool, optional (default=True)
        If True, display the colorbar; otherwise, suppress it.

    Returns:
    --------
    fig : Matplotlib Figure
        The Matplotlib figure object.
    ax : Matplotlib Axes
        The Matplotlib axes object.
    pcm : Matplotlib QuadMesh
        The QuadMesh object for the plot.

    Examples:
    ---------
    ```python
    import numpy as np
    from plot_slice import plot_slice

    # Generate example data
    data = np.random.rand(50, 100, 200)

    # Plot XY plane slice
    fig, ax, pcm = plot_slice(data, cmap_set='viridis', slice=10, plane='xy', title='XY Plane slice')
    plt.show()
    ```

    Notes:
    ------
    - The function reads default plotting parameters from a JSON file. Make sure to provide a valid path to the JSON file or use the default if not specified.
    - The colormap (`cmap_set`) can be either a Matplotlib colormap or a string specifying the colormap name.
    - The `subvolume` parameter draws a rectangle around a specified subvolume if provided.
    - The `labels` parameter can be used to customize colorbar ticks.

    """
    
    # Get the default colormap intensity if not in function parameters
    default_cmap_intensity = global_settings.get('cmap_intensity', 1.0)
    cmap_intensity = cmap_intensity or default_cmap_intensity
    
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
        cmap_set = global_settings.get('colormap')
        # Evaluate the string to get the actual colormap function
        cmap_set = eval(cmap_set)
        

    # Adjust colormap intensity if needed
    if cmap_intensity != 1.0:
        if isinstance(cmap_set, str):
            base_cmap = plt.cm.get_cmap(cmap_set)
        else:
            base_cmap = cmap_set
            
        # Create a modified colormap with adjusted intensity
        colors = base_cmap(np.linspace(0, 1, 256))
        
        # Adjust the RGB values (not alpha)
        # Values > 1.0 increase brightness, < 1.0 decrease brightness
        # Clamp values to valid range [0, 1]
        colors[:, :3] = np.clip(colors[:, :3] * cmap_intensity, 0, 1)
        
        # Create new colormap
        cmap_set = ListedColormap(colors)

    # Create a figure and axis with adjusted font family and size
    if ax is None:
        fig, ax = plt.subplots(figsize=(fig_width, fig_height), facecolor=face_color, edgecolor=edge_color)
        fig.set_facecolor(face_color)
    else:
        fig = ax.figure  # Use the figure from the provided axis

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
        cbar = None
        if show_colorbar:
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
        cbar = None
        if show_colorbar:
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
        cbar = None
        if show_colorbar:
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
    if cbar is not None:
        for label in cbar.ax.get_yticklabels():
            label.set_color(text_color)
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

        # Append the suffix "(voxel)" to the labels
        xlabel += ' (voxel)'
        ylabel += ' (voxel)'

        # Set the new X-axis and Y-axis labels
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)

    # UPDATE: 25.04.2025
    # Issue with labels which are not a dictionary
    if labels is not None and cbar is not None:
        # Convert the dictionary to sortable items
        if isinstance(labels, dict):
            # Convert string keys to integers for proper ordering
            label_items = []
            for k, v in labels.items():
                try:
                    # Try to convert key to integer for sorting
                    label_items.append((int(k), v))
                except ValueError:
                    # If key can't be converted to int, use it as is
                    label_items.append((k, v))
            
            # Sort by key
            label_items.sort()
            
            # Set the ticks and labels
            tick_positions = [k for k, v in label_items]
            tick_labels = [v for k, v in label_items]
            
            cbar.set_ticks(tick_positions)
            cbar.ax.set_yticklabels(tick_labels)
        else:
            # Handle case where labels is a list
            cbar.set_ticks(np.arange(len(labels)))
            cbar.ax.set_yticklabels(labels)

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

    return fig, ax, pcm


def ortho_views(data, paramsfile='parameters.json', cmap_set=None, slice_indices=None, subvolume=None, 
                labels=None, title=None, voxel_size=None, dark_mode=False, cmap_intensity=1.0, layout_type=None, add_slice_ref=True):
    """
    Visualize orthogonal views of 3D volumetric data.
    
    Parameters:
    -----------
    ...existing parameters...
    layout_type : str, optional (default=None)
        The layout configuration to use. Options are:
        - None: Use arbitrary layout (default)
        - 'rectangular': Layout optimized for rectangular data
        - 'arbitrary': Custom layout with manually specified positions (default)
    """
    import matplotlib.pyplot as plt

    nz, ny, nx = data.shape
    
    # Get layout settings from default_figure_settings.json
    layout_settings = default_figure_settings.get('ortho_views_layouts', {})
    
    # By default, use arbitrary layout
    if layout_type is None or layout_type not in ['rectangular']:
        layout_type = 'arbitrary'
        
    # Get layout config
    layout_config = layout_settings.get(layout_type)
    
    # If specified layout doesn't exist, fall back to arbitrary
    if not layout_config:
        layout_type = 'arbitrary'
        layout_config = layout_settings.get('arbitrary', {})

    def safe_index(idx, size):
        return min(max(idx, 0), size - 1)

    if slice_indices is None:
        slice_xy = safe_index(nz // 2, nz)
        slice_yz = safe_index(nx // 2, nx)
        slice_xz = safe_index(ny // 2, ny)
    else:
        if isinstance(slice_indices, dict):
            slice_xy = safe_index(slice_indices.get('slice_xy', nz // 2), nz)
            slice_yz = safe_index(slice_indices.get('slice_yz', nx // 2), nx)
            slice_xz = safe_index(slice_indices.get('slice_xz', ny // 2), ny)
        else:
            slice_xy = safe_index(slice_indices[0], nz)
            slice_yz = safe_index(slice_indices[1], nx)
            slice_xz = safe_index(slice_indices[2], ny)

    # Create figure based on layout settings from config
    fig_width = layout_config.get('fig_width')
    fig_height = layout_config.get('fig_height')
    fig = plt.figure(figsize=(fig_width, fig_height))
    fig.set_facecolor('black' if dark_mode else 'white')
    
    # Get spacing parameters from layout
    wspace = layout_config.get('wspace')
    title_pad = layout_config.get('title_pad')
    
    # Get positions from config - both layout types should have positions now
    positions = layout_config.get('positions')
    
    # Apply wspace adjustment if needed
    if wspace is not None and len(positions) == 3:
        # Calculate adjustment based on wspace
        spacing = wspace / 100.0  # Convert percentage to decimal
        
        # Apply spacing between subplots 
        new_positions = [
            positions[0],  # Keep first position as is
            [positions[0][0] + positions[0][2] + spacing, positions[1][1], positions[1][2], positions[1][3]],
            [positions[0][0] + positions[0][2] + positions[1][2] + 2*spacing, positions[2][1], positions[2][2], positions[2][3]]
        ]
        positions = new_positions
    
    # Create subplots using explicit positions
    axes = [fig.add_axes(pos) for pos in positions]
    
    # Calculate colorbar position
    cbar_left = positions[2][0] + positions[2][2] + 0.01
    cbar_width = layout_config.get('cbar_width')
    bottom = positions[0][1]
    height = positions[0][3]

    # Add the colorbar axes
    cbar_ax = fig.add_axes([cbar_left, bottom, cbar_width, height])
    # Set the text color of the colorbar depending on dark mode
    cbar_ax.tick_params(axis='both', colors='white' if dark_mode else 'black')

    planes = ['xy', 'yz', 'xz']
    slices = [slice_xy, slice_yz, slice_xz]
    titles = ['XY', 'YZ', 'XZ']

    pcms = []
    for i, (plane, slc, dir_title) in enumerate(zip(planes, slices, titles)):
        _, _, pcm = ortho_slice(
            data,
            paramsfile=paramsfile,
            cmap_set=cmap_set,
            slice=slc,
            plane=plane,
            subvolume=subvolume,
            labels=labels,
            title=None,  # Set title ourselves
            voxel_size=voxel_size,
            dark_mode=dark_mode,
            cmap_intensity=cmap_intensity,
            ax=axes[i],
            show_colorbar=False
        )
        pcms.append(pcm)
        axes[i].set_aspect('equal')
        axes[i].set_title(dir_title, fontsize=plt.rcParams['font.size'], 
                         color='white' if dark_mode else 'black', pad=title_pad)
        
        # Don't allow dev_ortho_slice to reposition our axes
        axes[i].set_position(positions[i])

    # Add the colorbar separately
    fig.colorbar(pcms[0], cax=cbar_ax, orientation='vertical')
    
    # Add reference lines to show slice positions across views
    if add_slice_ref is True:
        add_slice_reference_lines(axes, data.shape, [slice_xy, slice_yz, slice_xz], dark_mode, show_text=False)
    

    return fig, axes


def add_slice_reference_lines(axes, data_shape, slice_indices, dark_mode=False, show_text=True):
    """
    Add reference lines to orthogonal views to show the position of other slices.
    
    Parameters:
    -----------
    axes : list of matplotlib.axes.Axes
        List of the three axes objects (xy, yz, xz)
    data_shape : tuple
        Shape of the 3D data (nz, ny, nx)
    slice_indices : list
        List of slice indices [slice_xy, slice_yz, slice_xz]
    dark_mode : bool
        Whether dark mode is enabled
    """
    nz, ny, nx = data_shape
    slice_xy, slice_yz, slice_xz = slice_indices
    
    # Define line colors and styles
    line_color = 'red' if dark_mode else 'red'
    text_color = 'white' if dark_mode else 'black'
    line_style = '--'
    line_width = 1.5
    alpha = 0.8
    
    # XY view (axes[0]) - Show yz and xz slice positions
    # Vertical line for yz slice (x position)
    axes[0].axvline(x=slice_yz, color=line_color, linestyle=line_style, linewidth=line_width, alpha=alpha)
    if show_text:
        axes[0].text(slice_yz, ny*0.05, f"YZ (x={slice_yz})", color=text_color, 
                 rotation=90, va='bottom', ha='right', backgroundcolor='black' if dark_mode else 'white', alpha=0.7)
    
    axes[0].axhline(y=slice_xz, color=line_color, linestyle=line_style, linewidth=line_width, alpha=alpha)
    if show_text:
        axes[0].text(nx*0.05, slice_xz, f"XZ (y={slice_xz})", color=text_color, 
                 rotation=0, va='bottom', ha='right', backgroundcolor='black' if dark_mode else 'white', alpha=0.7)
    
    # YZ view (axes[1]) - Show xy and xz slice positions  
    # Horizontal line for xy slice (z position)
    axes[1].axhline(y=slice_xy, color=line_color, linestyle=line_style, linewidth=line_width, alpha=alpha)
    if show_text:
        axes[1].text(nx*0.05, slice_xy, f"XY (z={slice_xy})", color=text_color, 
                 rotation=0, va='bottom', ha='right', backgroundcolor='black' if dark_mode else 'white', alpha=0.7)
    
    # Vertical line for xz slice (y position)
    axes[1].axvline(x=slice_xz, color=line_color, linestyle=line_style, linewidth=line_width, alpha=alpha)
    if show_text:
        axes[1].text(slice_xz, ny*0.05, f"XZ (y={slice_xz})", color=text_color, 
                 rotation=90, va='bottom', ha='right', backgroundcolor='black' if dark_mode else 'white', alpha=0.7)
    
    # XZ view (axes[2]) - Show xy and yz slice positions
    # Horizontal line for xy slice (z position)
    axes[2].axhline(y=slice_xy, color=line_color, linestyle=line_style, linewidth=line_width, alpha=alpha)
    if show_text:
        axes[2].text(nx*0.05, slice_xy, f"XY (z={slice_xy})", color=text_color, 
                 rotation=0, va='bottom', ha='right', backgroundcolor='black' if dark_mode else 'white', alpha=0.7)
    
    # Vertical line for yz slice (x position)
    axes[2].axvline(x=slice_yz, color=line_color, linestyle=line_style, linewidth=line_width, alpha=alpha)
    if show_text:
        axes[2].text(slice_yz, ny*0.05, f"YZ (x={slice_yz})", color=text_color, 
                 rotation=90, va='bottom', ha='right', backgroundcolor='black' if dark_mode else 'white', alpha=0.7)

def histogram(data, paramsfile='parameters.json', dtype=None, cmap_set=None, title=None, log_scale='both', dark_mode=True):
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


def plot_effective_modulus(
    fraction, data, types='avg', marker='o', dark_mode=False, cmap_set=None, 
    xlabel_percent=False, grid=True, secondary_axis=True, secondary_label=None, linewidth=4, axes_colored=True,
    ylabel=None, xlabel=None, title=None
):
    """
    Plot effective modulus against porosity.

    Parameters:
    -----------
    fraction : numpy.ndarray
        Array of porosity values (x-axis).
    data : dict
        Dictionary containing modulus data for each type (e.g., 'voigt', 'reuss', 'hs_upper', 'hs_lower', 'avg').
    types : str or list, optional (default='avg')
        Type or list of types of modulus to plot. Valid options are 'voigt', 'reuss', 'hs_upper', 'hs_lower', 'avg', or 'all'.
    marker : str, optional (default='o')
        Marker style for the plot lines.
    dark_mode : bool, optional (default=False)
        If True, use a dark color scheme; otherwise, use a light color scheme.
    cmap_set : str or Colormap, optional (default=None)
        Colormap to use for the plot. If None, uses the default from global_settings.
    xlabel_percent : bool, optional (default=False)
        If True, format the x-axis as percentages.
    grid : bool, optional (default=True)
        If True, display a grid on the plot.
    secondary_axis : bool, optional (default=True)
        If True, display a secondary y-axis.
    secondary_label : str, optional (default=None)
        Custom label for the secondary y-axis. If None, uses the second element of `ylabel` if provided.
    linewidth : int, optional (default=4)
        Width of the plot lines.
    axes_colored : bool, optional (default=True)
        If True, color the axes for better contrast.
    ylabel : tuple or list, optional (default=None)
        Tuple or list of two strings: (primary y-axis label, secondary y-axis label).
    xlabel : str, optional (default=None)
        Custom label for the x-axis. If None, defaults to "Porosity".
    title : str, optional (default=None)
        Title of the plot. If None, no title is set.

    Returns:
    --------
    fig : matplotlib.figure.Figure
        The Matplotlib figure object.
    ax : matplotlib.axes.Axes
        The Matplotlib axes object.

    Examples:
    ---------
    ```python

    # Example data
    porosity = np.linspace(0, 1, 20)
    data = {
        'voigt': np.random.rand(20),
        'reuss': np.random.rand(20),
        'avg': np.random.rand(20),
        'hs_upper': np.random.rand(20),
        'hs_lower': np.random.rand(20),
    }

    fig, ax = plot_effective_modulus(porosity, data, types='all', dark_mode=True)
    plt.show()
    ```

    Notes:
    ------
    - The function supports plotting multiple modulus types simultaneously.
    - The `cmap_set` parameter can be a string (colormap name) or a Matplotlib/CMcrameri colormap object.
    - The `ylabel` parameter can be used to set both primary and secondary y-axis labels.
    - The secondary y-axis is enabled by default and can be customized with `secondary_label`.
    - Adjust `dark_mode`, `axes_colored`, and `grid` for preferred plot appearance.
    """
    if dark_mode:
        text_color, face_color, edge_color = 'white', 'black', 'white'
    else:
        text_color, face_color, edge_color = 'black', 'white', 'black'
    
    fig, ax = plt.subplots(figsize=(fig_width, fig_height), facecolor=face_color, edgecolor=edge_color)
    fig.set_facecolor(face_color)  # Set the face color of the entire figure   
    
    if axes_colored:
        ax.set_facecolor(face_color)
        for spine in ax.spines.values():
            spine.set_edgecolor('peru')
        y_color = 'peru'
    else:
        for spine in ax.spines.values():
            spine.set_edgecolor(edge_color)
        y_color = text_color

    color1 = face_color
    color2 = 'tomato' if dark_mode else 'darkred'
    
    # Title handling
    if title is not None:
        ax.set_title(title, color=text_color)
    
    if types == 'all':
        types = ['voigt', 'reuss', 'avg', 'hs_upper', 'hs_lower']
    elif isinstance(types, str):
        types = [types]

    # Handle colormap
    if cmap_set is None:
        # Get the default colormap from settings
        cmap_set = global_settings.get('colormap')
        # Evaluate the string to get the actual colormap function
        cmap_set = eval(cmap_set)
    elif isinstance(cmap_set, str):
        # If a string is provided, try to get it from matplotlib's colormaps
        try:
            cmap_set = plt.colormaps[cmap_set]  # Use the non-deprecated method
        except:
            # Fallback to a default colormap if the requested one doesn't exist
            print(f"Warning: Colormap '{cmap_set}' not found, using 'viridis' instead.")
            cmap_set = plt.colormaps['viridis']  # Use the non-deprecated method
    
    # Generate colors based on number of types
    n_types = len(types)
    colors = [cmap_set(i/(n_types-1) if n_types > 1 else 0.5) for i in range(n_types)]
    
    for i, mod_type in enumerate(types):
        modulus_values = np.array(data[mod_type])
        labels = {
            'voigt': 'Voigt Bound',
            'reuss': 'Reuss Bound',
            'hs_upper': 'Hashin–Shtrikman Upper Bound',
            'hs_lower': 'Hashin–Shtrikman Lower Bound',
            'avg': 'Voigt-Reuss-Hill Average',
        }
        
        _marker_style = {'voigt': '-', 'reuss': '--', 'hs_upper': 'dashed', 'hs_lower': '-.', 'avg': '-'}
        
        ax.plot(fraction, modulus_values, label=labels[mod_type], linestyle=_marker_style[mod_type], 
                marker=marker, markersize=4, color=colors[i], linewidth=linewidth)

    # y-axis label handling
    if ylabel is not None and isinstance(ylabel, (tuple, list)) and len(ylabel) == 2:
        y1_label, y2_label = ylabel
    else:
        y1_label = ""
        y2_label = ""

    # x-axis label handling
    if xlabel is None:
        x_label_str = "Porosity"
    else:
        x_label_str = xlabel

    ax.set_xlabel(x_label_str, color=text_color)
    ax.set_ylabel(y1_label, color=y_color)
    
    # Set the face and edge color of the axes (background within the plot)
    ax.set_facecolor(face_color)
    for spine in ax.spines.values():
        spine.set_edgecolor(edge_color)
    
    legend = ax.legend(facecolor=face_color, edgecolor=edge_color)
    
    for text in legend.get_texts():
        text.set_color(text_color)
        
    # Add grid
    if grid:
        plt.grid(True, linestyle='--', alpha=0.7)

    ax.tick_params(axis='y', colors=y_color, which='both')
    ax.tick_params(axis='x', colors=text_color, which='both')
    if xlabel_percent:
        ax.xaxis.set_major_formatter(mtick.PercentFormatter(1.00))  # convert x-axis into percent
    plt.xlim([0, 1])
    
    # Find global min/max across all plotted data for consistent scaling
    all_values = []
    for mod_type in types:
        all_values.extend(data[mod_type])
    
    data_min = min(all_values) if all_values else 0
    data_max = max(all_values) if all_values else 1
    
    # Set the primary y-axis limits
    ax.set_ylim([data_min, data_max])
    
    # Add secondary y-axis if requested
    if secondary_axis:
        # Create a twin of the primary axis
        ax2 = ax.twinx()
        ax2.set_facecolor(face_color)
        
        if axes_colored:
            for spine in ax2.spines.values():
                spine.set_edgecolor('tomato')
            y2_color = 'tomato'
        else:
            for spine in ax2.spines.values():
                spine.set_edgecolor(edge_color)
            y2_color = text_color
        
        # Set the secondary y-axis limits based on conversion factor
        secondary_min = data_min
        secondary_max = data_max
        ax2.set_ylim([secondary_min, secondary_max])
        
        # Set label for secondary axis
        if secondary_label:
            ax2.set_ylabel(secondary_label, color=y2_color)
        else:
            ax2.set_ylabel(y2_label, color=y2_color)
        
        # Style the secondary axis
        ax2.tick_params(axis='y', colors=y2_color)
        for spine in ax2.spines.values():
            spine.set_edgecolor(edge_color)
    
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