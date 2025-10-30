import glob
import os
import numpy as np
from drp_template.default_params import read_parameters_file, read_package_config, check_output_folder
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
from matplotlib.colors import ListedColormap
from matplotlib.ticker import FixedLocator, FixedFormatter
from cmcrameri import cm

__all__ = [
    'ortho_slice',
    'ortho_views',
    'add_slice_reference_lines',
    'save_figure',
    'histogram',
    'plot_effective_modulus',
    'get_figure_colors'
]

# S E T T I N G S
# Read the package configuration file (not from output folder, but from package directory)
default_figure_settings = read_package_config('default_figure_settings.json')

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

    # Helper function to check if a slice contains all unique values from the full data
    def slice_has_all_phases(data_slice, full_data_unique):
        slice_unique = np.unique(data_slice)
        return np.all(np.isin(full_data_unique, slice_unique))

    if plane == 'xy':
        if slice is None:
            nz = read_parameters_file(paramsfile=paramsfile, paramsvars='nz')
            slice = (nz // 2) - 1
            
            # Check if center slice has all phases
            unique_values = np.unique(data)
            if not slice_has_all_phases(data[:, :, slice], unique_values):
                # Import the function from tools
                from drp_template.tools import find_slice_with_all_values
                slice_dict = find_slice_with_all_values(data)
                if slice_dict['xy'] is not None:
                    slice = slice_dict['xy']

        data = data[:, :, slice]
    elif plane == 'yz':
        if slice is None:
            nx = read_parameters_file(paramsfile=paramsfile, paramsvars='nx')
            slice = (nx // 2) - 1
            
            # Check if center slice has all phases
            unique_values = np.unique(data)
            if not slice_has_all_phases(data[slice, :, :], unique_values):
                # Import the function from tools
                from drp_template.tools import find_slice_with_all_values
                slice_dict = find_slice_with_all_values(data)
                if slice_dict['yz'] is not None:
                    slice = slice_dict['yz']

        data = data[slice, :, :]
    elif plane == 'xz':
        if slice is None:
            ny = read_parameters_file(paramsfile=paramsfile, paramsvars='ny')
            slice = (ny // 2) - 1
            
            # Check if center slice has all phases
            unique_values = np.unique(data)
            if not slice_has_all_phases(data[:, slice, :], unique_values):
                # Import the function from tools
                from drp_template.tools import find_slice_with_all_values
                slice_dict = find_slice_with_all_values(data)
                if slice_dict['xz'] is not None:
                    slice = slice_dict['xz']

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


def _resolve_colormap(cmap_input):
    """
    Helper function to safely resolve colormap values to a Colormap object.
    
    Parameters:
    -----------
    cmap_input : str or Colormap
        Colormap name or object to resolve
        
    Returns:
    --------
    matplotlib.colors.Colormap
        Resolved colormap object
    """
    if cmap_input is None:
        return plt.colormaps['viridis']
    
    # Already a Colormap-like object
    if hasattr(cmap_input, 'N') or callable(cmap_input):
        return cmap_input
    
    if isinstance(cmap_input, str):
        # First try matplotlib colormaps (most common)
        try:
            return plt.colormaps.get_cmap(cmap_input)
        except Exception:
            # Then try cmcrameri (for specialized colormaps)
            try:
                return getattr(cm, cmap_input)
            except Exception:
                # Finally try cmcrameri with 'cm.' prefix
                if cmap_input.startswith('cm.'):
                    name = cmap_input.split('.', 1)[1]
                    try:
                        return getattr(cm, name)
                    except Exception:
                        try:
                            return plt.colormaps.get_cmap(name)
                        except Exception:
                            return plt.colormaps['viridis']
                else:
                    return plt.colormaps['viridis']
    
    return plt.colormaps['viridis']


def histogram(
    data,
    thresholds=None,
    paramsfile='parameters.json',
    dtype=None,
    cmap_set=None,
    title=None,
    log_scale='both',
    dark_mode=True,
    num_bins=None
):
    """
    Plot a histogram with optional threshold-based coloring.

    Parameters:
    -----------
    data : numpy.ndarray
        Input data array (will be flattened if multidimensional).
    thresholds : list of dict, optional (default=None)
        Threshold definitions for coloring histogram bars. Each threshold should be a dictionary with:
          - 'label': str, human-readable label for the threshold range
          - 'range': (min, max), numeric pair defining the inclusive range
        Example: [{'label':'Pores', 'range':[0, 13800]}, {'label':'Solid', 'range':[13801, 65535]}]
        Legacy dict format (label -> [min, max]) is also supported for backward compatibility.
        If None, plots a standard histogram without threshold coloring.
    paramsfile : str, optional (default='parameters.json')
        Path to JSON file containing plotting parameters.
    dtype : str, optional (default=None)
        Data type ('uint8' or 'uint16'). If None, read from paramsfile.
    cmap_set : str or matplotlib.colors.Colormap, optional (default=None)
        Colormap for histogram bars. Supports matplotlib colormap names ('viridis', 'berlin') 
        and cmcrameri colormaps ('batlow', 'oslo'). If None, uses default from global settings.
    title : str, optional (default=None)
        Plot title. If None, uses 'Threshold Histogram'.
    log_scale : str, optional (default='both')
        Axis scaling: 'x', 'y', 'both', or None for linear scaling.
    dark_mode : bool, optional (default=True)
        Use dark color scheme if True, light scheme if False.
    num_bins : int, optional (default=None)
        Number of histogram bins. If None, uses Freedman-Diaconis rule with fallback to 256.

    Returns:
    --------
    fig : matplotlib.figure.Figure
        The matplotlib figure object.
    ax : matplotlib.axes.Axes  
        The matplotlib axes object.

    Examples:
    ---------
    Basic histogram:
    >>> fig, ax = histogram(data, cmap_set='viridis')
    
    Threshold-based coloring:
    >>> thresholds = [
    ...     {'label': 'Pores', 'range': [0, 13800]},
    ...     {'label': 'Solid', 'range': [13801, 65535]}
    ... ]
    >>> fig, ax = histogram(data, thresholds=thresholds, cmap_set='berlin')

    Notes:
    ------
    - Function automatically handles zero counts in log-scale plots by replacing with small epsilon
    - Colormap resolution supports both matplotlib and cmcrameri colormaps
    - Threshold validation ensures proper format and data types
    - Uses global figure settings from default_figure_settings.json when available
    """
    # Flatten data if it's multidimensional
    data = data.flatten()
    
    # Set dtype based on the parameters file if not provided
    if dtype is None:
        dtype = read_parameters_file(paramsfile=paramsfile, paramsvars='dtype')

    # Determine gray_max based on dtype
    gray_max = 255 if dtype == 'uint8' else 65535

    # Set default colormap if not specified
    if cmap_set is None:
        # Get default colormap from global settings
        cmap_val = global_settings.get('colormap', 'cm.batlow')
        cmap_set = _resolve_colormap(cmap_val)
    else:
        # If user provided a string, resolve it to a Colormap object safely
        if isinstance(cmap_set, str):
            cmap_set = _resolve_colormap(cmap_set)

    # Set color scheme based on dark_mode
    if dark_mode:
        text_color, face_color, edge_color = 'white', 'black', 'white' 
    else:
        text_color, face_color, edge_color = 'black', 'white', 'black'

    # Calculate histogram bins
    if num_bins is not None:
        bins = np.linspace(0, gray_max, num_bins + 1)
    else:
        # Calculate histogram bins using Freedman-Diaconis rule with guards
        iqr = np.percentile(data, 75) - np.percentile(data, 25)
        if iqr <= 0 or np.isnan(iqr):
            # fallback to fixed bin count
            bins = np.linspace(0, gray_max, 256 + 1)
        else:
            bins_width = 2 * iqr / (len(data) ** (1 / 3))
            if not np.isfinite(bins_width) or bins_width <= 0:
                bins = np.linspace(0, gray_max, 256 + 1)
            else:
                bins = np.arange(0, gray_max + bins_width, bins_width)

    # Compute histogram of gray-scale intensities
    hist, bins = np.histogram(data, bins=bins, range=(0, gray_max))
    bin_centers = (bins[:-1] + bins[1:]) / 2
    bin_widths = bins[1:] - bins[:-1]

    # protect log-scale plotting from zero counts
    hist_plot = hist.copy()
    if log_scale in ('both', 'y'):
        eps = 1e-6
        hist_plot = np.where(hist_plot <= 0, eps, hist_plot)

    # Create the figure and axis
    fig, ax = plt.subplots(figsize=(fig_width, fig_height), facecolor=face_color, edgecolor=edge_color)
    
    # Normalize thresholds to canonical list-of-dicts format
    if isinstance(thresholds, dict):
        # Convert legacy dict format: {'label': [min, max]} -> [{'label': 'label', 'range': (min, max)}]
        thresholds = [{'label': k, 'range': tuple(v)} for k, v in thresholds.items()]

    # Validate canonical format
    if thresholds is not None:
        if not isinstance(thresholds, list):
            raise TypeError("'thresholds' must be a list of dicts with keys 'label' and 'range' or None")
        for t in thresholds:
            if not isinstance(t, dict):
                raise TypeError("Each threshold must be a dict with keys 'label' and 'range'")
            if 'label' not in t or 'range' not in t:
                raise KeyError("Each threshold dict must contain 'label' and 'range'")
            if not isinstance(t['label'], str):
                raise TypeError("threshold 'label' must be a string")
            if not (isinstance(t['range'], (list, tuple)) and len(t['range']) == 2):
                raise ValueError("threshold 'range' must be a sequence of two values (min,max)")
    
    # Plot histogram
    if thresholds is None:
        # Standard histogram with colormap gradient
        cmap = cmap_set if hasattr(cmap_set, 'N') else plt.colormaps.get_cmap(cmap_set)
        colors = cmap(np.linspace(0, 1, len(bins) - 1))
        ax.bar(bins[:-1], hist_plot, width=bin_widths, color=colors, linewidth=0.5, edgecolor=None)
    else:
        # Threshold-based coloring
        cmap = cmap_set if hasattr(cmap_set, 'N') else plt.colormaps.get_cmap(cmap_set)
        
        # Generate unique colors for each threshold
        n_thresholds = len(thresholds)
        threshold_colors = [cmap(i / (n_thresholds - 1)) if n_thresholds > 1 else cmap(0.5) 
                           for i in range(n_thresholds)]

        # Color bars based on threshold ranges
        default_color = 'gray' if dark_mode else 'lightgray'
        bar_colors = [default_color] * len(bin_centers)

        for i, t in enumerate(thresholds):
            min_val, max_val = t['range']
            in_range = (bin_centers >= min_val) & (bin_centers <= max_val)
            for idx, flag in enumerate(in_range):
                if flag:
                    bar_colors[idx] = threshold_colors[i]

        # Plot bars with individual colors
        for center, height, width, color in zip(bin_centers, hist_plot, bin_widths, bar_colors):
            ax.bar(center, height, width=width, color=color, edgecolor=None)
        
        # Add legend
        legend_elements = [plt.Rectangle((0, 0), 1, 1, color=threshold_colors[i], label=t['label'])
                          for i, t in enumerate(thresholds)]
        ax.legend(handles=legend_elements, loc='upper right', 
                 facecolor=face_color, edgecolor=edge_color, framealpha=0.7)

    # After plotting, set y-axis lower limit for log scale to avoid warnings
    if log_scale in ('both', 'y'):
        try:
            min_positive = np.min(hist[hist > 0])
            ax.set_ylim(bottom=max(eps, min_positive * 0.1))
        except Exception:
            ax.set_ylim(bottom=eps)

    # Configure log scaling
    if log_scale == 'both':
        ax.set_xscale('log')
        ax.set_yscale('log')
    elif log_scale == 'x':
        ax.set_xscale('log')
    elif log_scale == 'y':
        ax.set_yscale('log')
        ax.set_ylim(bottom=0.1)

    # Set labels and styling
    font_size = plt.rcParams['font.size']
    ax.set_xlabel('Gray-scale intensity', color=text_color, fontsize=font_size)
    ax.set_ylabel('Frequency', color=text_color, fontsize=font_size)
    
    title_text = 'Threshold Histogram' if title is None else title
    ax.set_title(title_text, color=text_color, fontsize=font_size)
    
    ax.tick_params(axis='both', which='both', direction='in', labelsize=font_size, colors=text_color)
    
    for spine in ax.spines.values():
        spine.set_edgecolor(edge_color)
    
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
    fraction, data, types='avg', marker='o', markersize=4, dark_mode=False, cmap_set=None, 
    xlabel_percent=False, grid=True, secondary_axis=True, secondary_label=None, linewidth=4, axes_colored=True,
    ylabel=None, xlabel=None, loc_legend='upper right', ylim_off=0.05, xlim_off=None, title=None
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
    markersize : int, optional (default=4)
        Size of the markers in the plot.
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
    loc_legend : str, optional (default='upper right')
        Location of the legend in the plot.
    ylim_off : float, optional (default=0.05)
        Offset for the y-axis limits. If None, no offset is applied.
    xlim_off : float, optional (default=0.05)
        Offset for the x-axis limits. If None, no offset is applied.
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

    fig, ax = plt.subplots(figsize=(12, 10), facecolor=face_color, edgecolor=edge_color)
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
                marker=marker, markersize=markersize, color=colors[i], linewidth=linewidth)

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
    
    legend = ax.legend(facecolor=face_color, edgecolor=edge_color, loc=loc_legend)
    
    for text in legend.get_texts():
        text.set_color(text_color)
        
    # Add grid
    if grid:
        plt.grid(True, linestyle='--', alpha=0.7)

    ax.tick_params(axis='y', colors=y_color, which='both')
    ax.tick_params(axis='x', colors=text_color, which='both')
    if xlabel_percent:
        ax.xaxis.set_major_formatter(mtick.PercentFormatter(1.00))  # convert x-axis into percent
    # Set the x-axis limits with a margin based on xlim_off
    # Ensure fraction is iterable (e.g., numpy array or list)
    if xlim_off is None:
        plt.xlim([0, 1])
    else:
        if isinstance(fraction, (float, int)):
            fraction = np.array([fraction])
        else:
            fraction = np.asarray(fraction).flatten()
        x_min = np.min(fraction)
        x_max = np.max(fraction)
        x_margin = xlim_off * (x_max - x_min) if x_max != x_min else xlim_off * x_max
        plt.xlim([x_min - x_margin, x_max + x_margin])
    
    # Find global min/max across all plotted data for consistent scaling
    all_values = []
    for mod_type in types:
        all_values.extend(data[mod_type])
    
    data_min = min(all_values) if all_values else 0
    data_max = max(all_values) if all_values else 1
    
    # Set the primary y-axis limits
    # Set the primary y-axis limits with a 5% margin
    y_margin = ylim_off * (data_max - data_min) if data_max != data_min else ylim_off * data_max
    ax.set_ylim([data_min - y_margin, data_max + y_margin])
    
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
        # Set the secondary y-axis limits with a 5% margin
        y_margin = ylim_off * (secondary_max - secondary_min) if secondary_max != secondary_min else ylim_off * secondary_max
        ax2.set_ylim([secondary_min - y_margin, secondary_max + y_margin])
        
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





    

def get_figure_colors(fig, num_colors=10, format='all', print_colors=True, data_only=True):
    """
    Extract colors used in a Matplotlib figure and convert them to RGB, CMYK, and HEX formats.
    
    Parameters:
    -----------
    fig : matplotlib.figure.Figure
        The Matplotlib figure object to extract colors from.
    num_colors : int, optional (default=10)
        Number of colors to sample from the colormap if colormap is used.
    format : str, optional (default='all')
        Output format: 'rgb', 'cmyk', 'hex', or 'all' for all formats.
    print_colors : bool, optional (default=True)
        If True, print the color values to console.
    data_only : bool, optional (default=True)
        If True, extract only data visualization colors (colormap colors).
        If False, include all figure colors (axes, text, background, etc.).
    
    Returns:
    --------
    dict
        Dictionary containing color information in requested formats.
        Keys: 'rgb', 'cmyk', 'hex' (depending on format parameter)
        Each key maps to a sub-dictionary with:
        - 'data_colors': Colors from data visualization (bars, lines, colormaps)
        - 'decoration_colors': Colors from figure decorations (if data_only=False)
    
    Examples:
    ---------
    ```python
    # Create a figure with histogram
    fig, ax = histogram(data, cmap_set='batlow')
    
    # Get only colormap/data colors (default)
    colors = get_figure_colors(fig, num_colors=5, data_only=True)
    
    # Get all colors including axes, text, etc.
    all_colors = get_figure_colors(fig, num_colors=5, data_only=False)
    
    # Get only HEX codes of data colors
    hex_colors = get_figure_colors(fig, format='hex', num_colors=8)
    
    # Access the colors
    data_hex = colors['hex']['data_colors']
    ```
    
    Notes:
    ------
    - RGB values are in range [0, 1]
    - CMYK values are in range [0, 100] (percentage)
    - HEX values are in format '#RRGGBB'
    - data_only=True focuses on colormap/visualization colors
    - data_only=False includes axis colors, text colors, backgrounds, etc.
    """
    
    def rgb_to_cmyk(rgb):
        """Convert RGB (0-1) to CMYK (0-100)"""
        r, g, b = rgb[:3]  # Take only RGB, ignore alpha
        
        if (r, g, b) == (0, 0, 0):
            return (0, 0, 0, 100)
        
        # RGB to CMY
        c = 1 - r
        m = 1 - g
        y = 1 - b
        
        # CMY to CMYK
        k = min(c, m, y)
        if k == 1:
            return (0, 0, 0, 100)
        
        c = ((c - k) / (1 - k)) * 100
        m = ((m - k) / (1 - k)) * 100
        y = ((y - k) / (1 - k)) * 100
        k = k * 100
        
        return (c, m, y, k)
    
    def rgb_to_hex(rgb):
        """Convert RGB (0-1) to HEX"""
        r, g, b = rgb[:3]  # Take only RGB, ignore alpha
        return '#{:02x}{:02x}{:02x}'.format(int(r*255), int(g*255), int(b*255))
    
    # Collect colors from the figure
    data_colors_rgba = set()
    decoration_colors_rgba = set()
    
    # Iterate through all axes in the figure
    for ax in fig.get_axes():
        # Extract DATA COLORS from plot elements (colormap/visualization)
        
        # From bar charts
        for patch in ax.patches:
            if hasattr(patch, 'get_facecolor'):
                data_colors_rgba.add(tuple(patch.get_facecolor()))
        
        # From line plots
        for line in ax.get_lines():
            if hasattr(line, 'get_color'):
                color = line.get_color()
                if isinstance(color, str):
                    # Convert named colors or hex to RGBA
                    from matplotlib.colors import to_rgba
                    data_colors_rgba.add(to_rgba(color))
                else:
                    data_colors_rgba.add(tuple(color))
        
        # From collections (pcolormesh, scatter, etc.)
        for collection in ax.collections:
            if hasattr(collection, 'get_facecolors'):
                face_colors = collection.get_facecolors()
                if len(face_colors) > 0:
                    # If many colors (colormap), sample evenly
                    if len(face_colors) > num_colors:
                        indices = np.linspace(0, len(face_colors)-1, num_colors, dtype=int)
                        for idx in indices:
                            data_colors_rgba.add(tuple(face_colors[idx]))
                    else:
                        for color in face_colors:
                            data_colors_rgba.add(tuple(color))
        
        if not data_only:
            # Extract DECORATION COLORS (axes, text, spines, etc.)
            from matplotlib.colors import to_rgba
            
            # Axis colors
            if hasattr(ax, 'get_facecolor'):
                decoration_colors_rgba.add(tuple(to_rgba(ax.get_facecolor())))
            
            # Spine colors
            for spine in ax.spines.values():
                if hasattr(spine, 'get_edgecolor'):
                    decoration_colors_rgba.add(tuple(to_rgba(spine.get_edgecolor())))
            
            # Text colors (labels, titles, ticks)
            if ax.xaxis.label:
                decoration_colors_rgba.add(tuple(to_rgba(ax.xaxis.label.get_color())))
            if ax.yaxis.label:
                decoration_colors_rgba.add(tuple(to_rgba(ax.yaxis.label.get_color())))
            if ax.title:
                decoration_colors_rgba.add(tuple(to_rgba(ax.title.get_color())))
            
            # Tick colors
            for tick in ax.xaxis.get_major_ticks():
                if tick.label1:
                    decoration_colors_rgba.add(tuple(to_rgba(tick.label1.get_color())))
            for tick in ax.yaxis.get_major_ticks():
                if tick.label1:
                    decoration_colors_rgba.add(tuple(to_rgba(tick.label1.get_color())))
    
    # Figure background color (if not data_only)
    if not data_only:
        from matplotlib.colors import to_rgba
        decoration_colors_rgba.add(tuple(to_rgba(fig.get_facecolor())))
    
    # Convert sets to sorted lists
    data_colors_rgba = sorted(list(data_colors_rgba))
    decoration_colors_rgba = sorted(list(decoration_colors_rgba))
    
    # If no data colors found, try to get from colormap
    if len(data_colors_rgba) < num_colors:
        # Try to extract colormap from first collection
        for ax in fig.get_axes():
            for collection in ax.collections:
                if hasattr(collection, 'get_cmap'):
                    cmap = collection.get_cmap()
                    if cmap is not None:
                        # Sample colors from colormap
                        sample_colors = cmap(np.linspace(0, 1, num_colors))
                        for color in sample_colors:
                            data_colors_rgba.add(tuple(color))
                        break
        data_colors_rgba = sorted(list(data_colors_rgba))
    
    # Limit to num_colors if we have too many data colors
    if len(data_colors_rgba) > num_colors:
        indices = np.linspace(0, len(data_colors_rgba)-1, num_colors, dtype=int)
        data_colors_rgba = [data_colors_rgba[i] for i in indices]
    
    # Convert to requested formats
    result = {}
    
    if format in ['rgb', 'all']:
        result['rgb'] = {
            'data_colors': data_colors_rgba,
            'decoration_colors': decoration_colors_rgba if not data_only else []
        }
    
    if format in ['cmyk', 'all']:
        result['cmyk'] = {
            'data_colors': [rgb_to_cmyk(rgb) for rgb in data_colors_rgba],
            'decoration_colors': [rgb_to_cmyk(rgb) for rgb in decoration_colors_rgba] if not data_only else []
        }
    
    if format in ['hex', 'all']:
        result['hex'] = {
            'data_colors': [rgb_to_hex(rgb) for rgb in data_colors_rgba],
            'decoration_colors': [rgb_to_hex(rgb) for rgb in decoration_colors_rgba] if not data_only else []
        }
    
    # Print colors if requested
    if print_colors:
        print(f"\n{'='*80}")
        print(f"DATA COLORS (Colormap/Visualization): {len(data_colors_rgba)} colors extracted")
        print("=" * 80)
        
        for i, rgb in enumerate(data_colors_rgba, 1):
            print(f"\nData Color {i}:")
            
            if 'rgb' in result:
                print(f"  RGB:  ({rgb[0]:.3f}, {rgb[1]:.3f}, {rgb[2]:.3f})")
            
            if 'cmyk' in result:
                c, m, y, k = result['cmyk']['data_colors'][i-1]
                print(f"  CMYK: (C:{c:.1f}%, M:{m:.1f}%, Y:{y:.1f}%, K:{k:.1f}%)")
            
            if 'hex' in result:
                print(f"  HEX:  {result['hex']['data_colors'][i-1]}")
        
        if not data_only and len(decoration_colors_rgba) > 0:
            print(f"\n{'='*80}")
            print(f"DECORATION COLORS (Axes/Text/Background): {len(decoration_colors_rgba)} colors extracted")
            print("=" * 80)
            
            for i, rgb in enumerate(decoration_colors_rgba, 1):
                print(f"\nDecoration Color {i}:")
                
                if 'rgb' in result:
                    print(f"  RGB:  ({rgb[0]:.3f}, {rgb[1]:.3f}, {rgb[2]:.3f})")
                
                if 'cmyk' in result:
                    c, m, y, k = result['cmyk']['decoration_colors'][i-1]
                    print(f"  CMYK: (C:{c:.1f}%, M:{m:.1f}%, Y:{y:.1f}%, K:{k:.1f}%)")
                
                if 'hex' in result:
                    print(f"  HEX:  {result['hex']['decoration_colors'][i-1]}")
        
        print("=" * 80)
    
    return result


def save_figure(figure, filename=None, format="png", dpi=300, log=True):
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