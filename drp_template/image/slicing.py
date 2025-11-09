
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from matplotlib.ticker import FixedLocator, FixedFormatter
from drp_template.default_params import read_parameters_file
from drp_template.image import _config


__all__ = [
    'ortho_slice',
    'ortho_views',
    'add_slice_reference_lines'
]

# Get settings from config module
global_settings = _config.get_global_settings()
fig_width = _config.fig_width
fig_height = _config.fig_height
im_left = _config.im_left
im_left_xz = _config.im_left_xz
im_bottom = _config.im_bottom
im_width = _config.im_width
im_height = _config.im_height
cax_width = _config.cax_width
cax_space_left = _config.cax_space_left
cax_space_right = _config.cax_space_right
im_title = _config.im_title

def ortho_slice(data, paramsfile='parameters.json', cmap_set=None, slice=None, plane='xy', subvolume=None, labels=None, title=None, voxel_size=None, dark_mode=True, cmap_intensity=1.0, ax=None, show_colorbar=True):
    """
    Visualize 2D slice of 3D volumetric data using Matplotlib.

    Parameters
    ----------
    data : 3D numpy array
        The volumetric data to be visualized.
    paramsfile : str, optional
        Name of the JSON file containing plotting parameters (default: 'parameters.json').
    cmap_set : Matplotlib colormap, optional
        The colormap to be used for the plot. If not specified, the default colormap ('batlow') will be used.
    slice : int, optional
        The index of the slice along the specified plane. If not provided, the default slice index is set to the middle slice.
    plane : str, optional
        The plane along which the slice will be visualized. Valid values are 'xy', 'yz', or 'xz'.
    subvolume : int or float, optional
        Specifies a subvolume indicated in the figure.
    labels : list of str, optional
        Labels for the colorbar. Can be a single string or a list.
    title : str, optional
        The title of the plot.
    voxel_size : int or float, optional
        The size of the voxels along each dimension.
    dark_mode : bool, optional
        If True, set a dark background; otherwise, set a light background (default: True).
    show_colorbar : bool, optional
        If True, display the colorbar; otherwise, suppress it (default: True).

    Returns
    -------
    fig : Matplotlib Figure
        The Matplotlib figure object.
    ax : Matplotlib Axes
        The Matplotlib axes object.
    pcm : Matplotlib QuadMesh
        The QuadMesh object for the plot.

    Example:
        import numpy as np
        from drp_template.image.slicing import ortho_slice
        data = np.random.rand(50, 100, 200)
        fig, ax, pcm = ortho_slice(data, cmap_set='viridis', slice=10, plane='xy', title='XY Plane slice')
        plt.show()

    Notes:
        The function reads default plotting parameters from a JSON file. Make sure to provide a valid path to the JSON file or use the default if not specified. The colormap cmap_set can be either a Matplotlib colormap or a string specifying the colormap name. The subvolume parameter draws a rectangle around a specified subvolume if provided. The labels parameter can be used to customize colorbar ticks.
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


def ortho_views(data, 
                paramsfile='parameters.json', 
                cmap_set=None, 
                slice_indices=None, 
                subvolume=None, 
                labels=None, 
                title=None, 
                voxel_size=None, 
                dark_mode=False, 
                cmap_intensity=1.0, 
                layout_type=None, 
                add_slice_ref=True):
    """
    Visualize orthogonal views of 3D volumetric data.
    
    Parameters:
    -----------
    data : 3D numpy array
        The volumetric data to be visualized.
    paramsfile : str, optional (default='parameters.json')
        Name of the JSON file containing plotting parameters.
    cmap_set : Matplotlib colormap, optional (default=None)
        The colormap to be used for the plot. If not specified, uses default from settings.
    slice_indices : dict or list, optional (default=None)
        Slice indices for each view. Can be a dict with keys 'slice_xy', 'slice_yz', 'slice_xz'
        or a list [slice_xy, slice_yz, slice_xz]. If None, uses middle slices.
    subvolume : int or float, optional (default=None)
        Specifies a subvolume indicated in the figure.
    labels : dict or list, optional (default=None)
        Labels for the colorbar ticks. Can be a dict mapping values to labels (e.g., {0: 'Pore', 1: 'Solid'})
        or a list of label strings. Used to annotate discrete phases or categories.
    title : str, optional (default=None)
        Overall title for the figure (currently not used, individual subplot titles are set).
    voxel_size : int or float, optional (default=None)
        The size of the voxels for axis scaling. If provided, axes will show physical units.
    dark_mode : bool, optional (default=False)
        If True, use dark background and light text; otherwise use light background.
    cmap_intensity : float, optional (default=1.0)
        Multiplier for colormap brightness. Values > 1.0 increase brightness, < 1.0 decrease it.
    layout_type : str, optional (default=None)
        The layout configuration to use. Options are:
        - None: Use arbitrary layout (default)
        - 'rectangular': Layout optimized for rectangular data
        - 'arbitrary': Custom layout with manually specified positions (default)
    add_slice_ref : bool, optional (default=True)
        If True, add reference lines showing slice positions across different views.
    
    Returns:
    --------
    fig : Matplotlib Figure
        The Matplotlib figure object.
    axes : list of Matplotlib Axes
        List of three axes objects [ax_xy, ax_yz, ax_xz].
    
    Examples:
    ---------
    ```python
    import numpy as np
    from drp_template.image import ortho_views
    
    # Create sample binary data
    data = np.random.randint(0, 2, (100, 100, 100), dtype=np.uint8)
    
    # Visualize with labels
    labels = {0: 'Pore', 1: 'Solid'}
    fig, axes = ortho_views(data, labels=labels, dark_mode=True)
    
    # Specify custom slice positions
    slice_indices = {'slice_xy': 50, 'slice_yz': 40, 'slice_xz': 60}
    fig, axes = ortho_views(data, slice_indices=slice_indices, labels=labels)
    ```
    """
    import matplotlib.pyplot as plt

    nz, ny, nx = data.shape
    
    # Get layout config using _config helper (handles fallback internally)
    layout_config = _config.get_layout_config(layout_type or 'arbitrary')

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
    cbar_spacing = layout_config.get('cbar_spacing', 0.01)  # Default to 0.01 if not specified
    cbar_left = positions[2][0] + positions[2][2] + cbar_spacing
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
    cbar = fig.colorbar(pcms[0], cax=cbar_ax, orientation='vertical')
    
    # Apply labels to colorbar if provided
    if labels is not None:
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


