import os
import numpy as np
from cmcrameri import cm

try:
    import pyvista as pv
    # Configure PyVista for Jupyter notebooks if available
    try:
        from IPython import get_ipython
        get_ipython()
        # We're in a Jupyter environment, set up interactive backend
        if not hasattr(pv, '_jupyter_backend_set'):
            try:
                pv.set_jupyter_backend('trame')  # Interactive 3D viewer
            except Exception:
                # Trame not installed, fall back to panel or ipyvtklink
                try:
                    pv.set_jupyter_backend('ipyvtklink')
                except Exception:
                    pv.set_jupyter_backend('static')  # Last resort
            pv._jupyter_backend_set = True
    except NameError:
        # Not in Jupyter, no need to set backend
        pass
except Exception:
    pv = None

from drp_template.default_params import read_parameters_file
from drp_template.image._config import get_volume_rendering_config
from drp_template.image.plotting import _resolve_colormap

__all__ = [
    'get_lighting_preset',
    'volume_rendering'
]


def get_lighting_preset(preset='default'):
    """Return predefined lighting configurations for PyVista volume rendering."""
    presets = {
        'bright': {
            'mode': 'custom',
            'key_light': {
                'position': (400, 400, 500),
                'focal_point': (0, 0, 0),
                'intensity': 1.2
            },
            'ambient_intensity': 0.5
        },
        'soft': {
            'mode': 'custom',
            'key_light': {
                'position': (300, 300, 350),
                'focal_point': (0, 0, 0),
                'intensity': 0.7
            },
            'ambient_intensity': 0.6
        },
        'dramatic': {
            'mode': 'custom',
            'key_light': {
                'position': (500, 200, 600),
                'focal_point': (0, 0, 0),
                'intensity': 1.5
            },
            'ambient_intensity': 0.1
        },
        'default': None,
        'custom': None,
        'none': {'mode': 'none'}
    }
    if preset not in presets:
        raise ValueError(f"Unknown preset '{preset}'. Choose from: {list(presets.keys())}")
    return presets[preset]


def volume_rendering(
    data,
    paramsfile='parameters.json',
    cmap_set=None,
    slice_indices=None,
    labels=None,
    title=None,
    dark_mode=False,
    window_size=None,
    mode='3d',
    phase_opacity=None,
    slice_opacity=None,
    show_3d_edges=False,
    edge_color='white',
    phase_colors=None,
    camera_zoom=None,
    lighting='custom',
    show_legend=True,
    show_axes=True,
    show_bounds=True,
    off_screen=None
):
    """Render a 3D labeled volume with optional slices and lighting using PyVista.
    
    Parameters
    ----------
    data : np.ndarray
        3D array containing phase labels.
    paramsfile : str, optional
        Path to parameters JSON file for loading labels and metadata.
    cmap_set : str or Colormap, optional
        Colormap to use for phase colors.
    slice_indices : list, tuple, or dict, optional
        Slice positions [x, y, z] or {'x': val, 'y': val, 'z': val}.
    labels : dict, optional
        Phase labels mapping {phase_id: 'Phase Name'}.
    title : str, optional
        Plot title.
    dark_mode : bool, optional
        Use dark background if True.
    window_size : list, optional
        Window size [width, height] in pixels.
    mode : str, optional
        Rendering mode: '3d', 'slices', or 'combined'. Default '3d'.
    phase_opacity : dict or list, optional
        Opacity values for 3D meshes {phase_id: opacity} or [opacity1, opacity2, ...].
    slice_opacity : float, optional
        Opacity for slice planes (0.0 to 1.0).
    show_3d_edges : bool, optional
        Show mesh edges on 3D objects.
    edge_color : str or tuple, optional
        Color for mesh edges.
    phase_colors : dict, optional
        Custom RGB colors {phase_id: (R, G, B)}.
    camera_zoom : float, optional
        Camera zoom factor.
    lighting : str or dict, optional
        Lighting preset ('bright', 'soft', 'dramatic', 'default', 'none', 'custom') 
        or custom lighting configuration dict.
    show_legend : bool, optional
        Display legend with phase labels.
    show_axes : bool, optional
        Display XYZ axes.
    show_bounds : bool, optional
        Display bounding box.
    off_screen : bool or None, optional
        If True, render off-screen (for saving images). If False, render interactively.
        If None (default), auto-detect: False in Jupyter notebooks, True otherwise.
    
    Returns
    -------
    image or pv.Plotter
        When off_screen=False (notebooks): displays visualization and returns image array.
        When off_screen=True (scripts): returns PyVista plotter for .screenshot() or further customization.
    """
    if pv is None:
        raise ImportError("PyVista is required for volume_rendering.")

    if not isinstance(data, np.ndarray) or data.ndim != 3:
        raise ValueError("'data' must be a 3D numpy array.")

    # Auto-detect off_screen mode if not specified
    if off_screen is None:
        try:
            # Check if running in Jupyter/IPython environment
            from IPython import get_ipython
            get_ipython()
            off_screen = False  # Interactive mode in notebooks
        except Exception:
            off_screen = True  # Off-screen mode in scripts

    vr_settings = get_volume_rendering_config()
    def _vr(key, default):
        return vr_settings.get(key, default)

    view_shift_x_rel = _vr('view_shift_x', 0.075)
    view_shift_y_rel = _vr('view_shift_y', -0.055)
    default_camera_zoom = _vr('camera_zoom', 0.85)
    legend_size = tuple(_vr('legend_size', [0.2, 0.5]))
    legend_position = _vr('legend_position', 'center left')
    win_size_default = _vr('window_size', [2400, 1800])
    title_font_size = _vr('title_font_size', 30)
    axes_line_width = _vr('axes_line_width', 2)
    background_color = 'black' if dark_mode else _vr('background_color', 'white')
    light_position_default = tuple(_vr('light_position', [350, 350, 400]))
    light_focal_point = tuple(_vr('light_focal_point', [0, 0, 0]))
    light_intensity_default = _vr('light_intensity', 0.95)
    ambient_intensity_default = _vr('ambient_intensity', 0.3)
    opacity_slice = _vr('opacity_slice', 1.0)

    # Load labels from params file if not provided
    if labels is None:
        try:
            params = read_parameters_file(paramsfile=paramsfile)
            labels = params.get('labels', None)
        except Exception:
            pass
    if labels is None:
        n_phases_guess = int(data.max()) + 1
        labels = {i: f"Phase {i}" for i in range(n_phases_guess)}

    # Resolve colormap
    if cmap_set is None:
        cmap = cm.batlow
    else:
        try:
            cmap = _resolve_colormap(cmap_set)
        except Exception:
            cmap = cm.batlow

    n_phases = max(int(data.max()) + 1, len(labels))
    computed_phase_colors = {}
    if n_phases <= 1:
        computed_phase_colors[0] = tuple(cmap(0.5)[:3])
    else:
        for i in range(n_phases):
            t = i / (n_phases - 1)
            rgba = cmap(t)
            computed_phase_colors[i] = tuple(rgba[:3])
    if phase_colors is not None:
        for pid, color in phase_colors.items():
            if isinstance(color, (list, tuple)) and len(color) == 3:
                computed_phase_colors[pid] = tuple(color)
    final_phase_colors = computed_phase_colors

    if slice_opacity is None:
        slice_opacity_value = opacity_slice
    else:
        slice_opacity_value = max(0.0, min(1.0, float(slice_opacity)))

    nx, ny, nz = data.shape
    if slice_indices is None:
        sx, sy, sz = nx // 2, ny // 2, nz // 2
    elif isinstance(slice_indices, dict):
        sx = slice_indices.get('x', nx // 2)
        sy = slice_indices.get('y', ny // 2)
        sz = slice_indices.get('z', nz // 2)
    elif isinstance(slice_indices, (list, tuple)) and len(slice_indices) == 3:
        sx, sy, sz = slice_indices
    else:
        sx, sy, sz = nx // 2, ny // 2, nz // 2

    grid = pv.ImageData()
    grid.dimensions = (nx, ny, nz)
    grid.point_data["phase"] = data.flatten(order="F")

    win_size = window_size or win_size_default

    # Lighting handling
    if isinstance(lighting, dict):
        mode_key = lighting.get('mode', 'custom')
        if mode_key == 'custom':
            use_custom_light = True
            lighting_mode = 'none'
        elif mode_key in ('none', 'default'):
            use_custom_light = False
            lighting_mode = mode_key
        else:
            use_custom_light = True
            lighting_mode = 'none'
    elif isinstance(lighting, str):
        if lighting == 'custom':
            use_custom_light = True
            lighting_mode = 'none'
        else:
            preset = get_lighting_preset(lighting)
            if preset is None or preset.get('mode') == 'default':
                use_custom_light = False
                lighting_mode = 'default'
            elif preset.get('mode') == 'none':
                use_custom_light = False
                lighting_mode = 'none'
            else:
                use_custom_light = True
                lighting_mode = 'none'
                lighting = preset
    else:
        use_custom_light = True
        lighting_mode = 'none'

    plotter = pv.Plotter(off_screen=off_screen, window_size=win_size, lighting=lighting_mode)
    plotter.set_background(background_color)

    if use_custom_light:
        if isinstance(lighting, dict):
            key_cfg = lighting.get('key_light', {})
            Lpos = key_cfg.get('position', light_position_default)
            Lfoc = key_cfg.get('focal_point', light_focal_point)
            Lint = key_cfg.get('intensity', light_intensity_default)
            Aint = lighting.get('ambient_intensity', ambient_intensity_default)
        else:
            Lpos = light_position_default
            Lfoc = light_focal_point
            Lint = light_intensity_default
            Aint = ambient_intensity_default
        key_light = pv.Light()
        key_light.position = Lpos
        key_light.focal_point = Lfoc
        key_light.intensity = Lint
        plotter.add_light(key_light)
        amb = pv.Light(light_type='headlight')
        amb.intensity = Aint
        plotter.add_light(amb)

    # Render phases/slices
    if mode == '3d':
        phase_opacity_map = {}
        if phase_opacity is None:
            for pid in range(n_phases):
                phase_opacity_map[pid] = slice_opacity_value
        elif isinstance(phase_opacity, dict):
            phase_opacity_map = phase_opacity.copy()
        elif isinstance(phase_opacity, (list, tuple)):
            for pid, opacity_val in enumerate(phase_opacity):
                if pid < n_phases:
                    phase_opacity_map[pid] = opacity_val
        for pid, opacity_val in phase_opacity_map.items():
            if opacity_val <= 0.0:
                continue
            opacity_val = max(0.0, min(1.0, opacity_val))
            pname = labels.get(pid, f"Phase {pid}") if isinstance(labels, dict) else f"Phase {pid}"
            phase_mesh = grid.threshold(value=[pid - 0.1, pid + 0.1], scalars='phase')
            if phase_mesh.n_cells > 0:
                plotter.add_mesh(
                    phase_mesh,
                    color=final_phase_colors.get(pid, (1.0, 1.0, 1.0)),
                    opacity=opacity_val,
                    show_edges=show_3d_edges,
                    edge_color=edge_color,
                    label=pname,
                    smooth_shading=True
                )
    elif mode in ('slices', 'combined'):
        origin = [sx, sy, sz]
        slice_xy = grid.slice(normal=[0, 0, 1], origin=origin)
        slice_xz = grid.slice(normal=[0, 1, 0], origin=origin)
        slice_yz = grid.slice(normal=[1, 0, 0], origin=origin)
        slice_planes = [slice_xy, slice_xz, slice_yz]
        for pid in range(n_phases):
            pname = labels.get(pid, f"Phase {pid}") if isinstance(labels, dict) else f"Phase {pid}"
            for i, plane in enumerate(slice_planes):
                p_slice = plane.threshold(value=[pid - 0.1, pid + 0.1], scalars='phase')
                if p_slice.n_cells > 0:
                    plotter.add_mesh(
                        p_slice,
                        color=final_phase_colors.get(pid, (1.0, 1.0, 1.0)),
                        opacity=slice_opacity_value,
                        show_edges=False,
                        label=pname if i == 0 else None,
                        show_scalar_bar=False,
                    )
        if mode == 'combined' and phase_opacity is not None:
            phase_opacity_map = {}
            if isinstance(phase_opacity, dict):
                phase_opacity_map = phase_opacity.copy()
            elif isinstance(phase_opacity, (list, tuple)):
                for pid, opacity_val in enumerate(phase_opacity):
                    if pid < n_phases:
                        phase_opacity_map[pid] = opacity_val
            for pid, opacity_val in phase_opacity_map.items():
                if opacity_val <= 0.0:
                    continue
                opacity_val = max(0.0, min(1.0, opacity_val))
                pname = labels.get(pid, f"Phase {pid}") if isinstance(labels, dict) else f"Phase {pid}"
                phase_mesh = grid.threshold(value=[pid - 0.1, pid + 0.1], scalars='phase')
                if phase_mesh.n_cells > 0:
                    plotter.add_mesh(
                        phase_mesh,
                        color=final_phase_colors.get(pid, (1.0, 1.0, 1.0)),
                        opacity=opacity_val,
                        show_edges=show_3d_edges,
                        edge_color=edge_color,
                        label=None,
                        smooth_shading=True
                    )

    if show_bounds:
        plotter.add_mesh(grid.outline(), color='black', line_width=2)
        plotter.show_bounds(location='outer', all_edges=True, color='gray')

    if show_legend:
        plotter.add_legend(
            size=legend_size,
            loc=legend_position,
            face='rectangle',
            bcolor='white',
            border=True
        )

    if show_axes:
        plotter.add_axes(xlabel='X', ylabel='Y', zlabel='Z', line_width=axes_line_width, labels_off=False)

    if title:
        plotter.add_title(title, font_size=title_font_size, color=('white' if dark_mode else 'black'))

    plotter.camera_position = 'iso'
    plotter.camera.zoom(camera_zoom if camera_zoom is not None else default_camera_zoom)
    win_size = window_size or win_size_default
    view_shift_x = view_shift_x_rel * win_size[0]
    view_shift_y = view_shift_y_rel * win_size[1]
    fp = plotter.camera.focal_point
    plotter.camera.focal_point = (fp[0] + view_shift_x, fp[1] + view_shift_y, fp[2])

    print(f"3D volume rendering with {n_phases} phases")
    
    # In interactive mode (notebooks), show the plot and return the image
    # In off-screen mode (scripts), just return the plotter for saving
    if not off_screen:
        return plotter.show()
    else:
        return plotter
