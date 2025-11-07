"""
Configuration module for image plotting settings.

This module loads and provides access to default figure settings from
the default_figure_settings.json configuration file. It handles global
matplotlib settings and makes them available to all image submodules.
"""
import matplotlib.pyplot as plt
from drp_template.default_params import read_package_config

# Load the package configuration file
_default_figure_settings = read_package_config('default_figure_settings.json')

# Access global settings from the nested structure
_global_settings = _default_figure_settings.get('global_settings', _default_figure_settings)

# Apply global matplotlib settings
plt.rcParams['font.size'] = _global_settings.get('font_size', 20)
plt.rcParams['font.family'] = _global_settings.get('font_family', 'Tahoma')


def get_global_settings():
    """
    Get the global figure settings dictionary.
    
    Returns
    -------
    dict
        Dictionary containing global settings like font_size, colormap, etc.
    
    Examples
    --------
    >>> settings = get_global_settings()
    >>> font_size = settings.get('font_size')
    >>> colormap = settings.get('colormap')
    """
    return _global_settings.copy()


def get_setting(key, default=None):
    """
    Get a specific global setting by key.
    
    Parameters
    ----------
    key : str
        The setting key to retrieve.
    default : any, optional
        Default value if key is not found.
    
    Returns
    -------
    any
        The setting value or default if not found.
    
    Examples
    --------
    >>> fig_width = get_setting('fig_width', 10)
    >>> colormap = get_setting('colormap', 'cm.batlow')
    """
    return _global_settings.get(key, default)


def get_layout_config(layout_type='arbitrary'):
    """
    Get layout configuration for ortho_views.
    
    Parameters
    ----------
    layout_type : str, optional
        Layout type ('rectangular' or 'arbitrary'). Default is 'arbitrary'.
    
    Returns
    -------
    dict
        Layout configuration dictionary with positions, spacing, etc.
    
    Examples
    --------
    >>> layout = get_layout_config('rectangular')
    >>> fig_width = layout.get('fig_width')
    >>> positions = layout.get('positions')
    """
    layout_settings = _default_figure_settings.get('ortho_views_layouts', {})
    layout_config = layout_settings.get(layout_type)
    
    # Fallback to arbitrary if specified layout doesn't exist
    if not layout_config:
        layout_config = layout_settings.get('arbitrary', {})
    
    return layout_config.copy()


def get_volume_rendering_config():
    """
    Get volume rendering configuration settings.
    
    Returns
    -------
    dict
        Volume rendering configuration with camera, lighting, window settings.
    
    Examples
    --------
    >>> config = get_volume_rendering_config()
    >>> window_size = config.get('window_size')
    >>> camera_zoom = config.get('camera_zoom')
    """
    return _default_figure_settings.get('volume_rendering', {}).copy()


# For backward compatibility, expose commonly used settings as module-level variables
im_left = get_setting('im_left', 0.25)
im_left_xz = get_setting('im_left_xz', 0.2)
im_right = get_setting('im_right', 1)
im_bottom = get_setting('im_bottom', 0.1)
im_width = get_setting('im_width', 0.6)
im_height = get_setting('im_height', 0.8)
cax_width = get_setting('cax_width', 0.04)
fig_width = get_setting('fig_width', 10)
fig_height = get_setting('fig_height', 10)
cax_space_left = get_setting('cax_space_left', 0.2)
cax_space_right = get_setting('cax_space_right', 0.02)
im_title = get_setting('im_title', 'Title')
