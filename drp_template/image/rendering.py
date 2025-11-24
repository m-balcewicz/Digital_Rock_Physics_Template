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
from drp_template.image.colormaps import get_phase_color_resources

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
    full_cmap=False,
    show_legend=True,
    show_axes=True,
    show_bounds=True,
    off_screen=None,
    colorbar_position=(0.15, 0.1),
    colorbar_size=(0.06, 0.8),
    colorbar_title='Amplitude',
    colorbar_title_offset=(-0.04, 0.38),
    colorbar_title_font_size=None,
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
    full_cmap : bool, optional
        If True, render the full (continuous) colormap across the scalar
        range of `data` using PyVista's volume rendering (no discrete phase
        thresholding). Useful to display all shades of `cmap_set` instead of
        showing separate phase meshes.
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
    # Colorbar handles
    pos_x, pos_y = colorbar_position
    width, height = colorbar_size
    tx_off, ty_off = colorbar_title_offset
    tx = pos_x + tx_off
    ty = pos_y + ty_off
    # Title font size (explicit param overrides settings)
    if colorbar_title_font_size is None:
        colorbar_title_font_size = title_font_size
    # Track whether we added a PyVista scalar bar so we don't remove it later
    _pyvista_scalar_bar_added = False
    # Track whether VTK scalar bar or text was added so we don't duplicate
    _vtk_scalar_bar_used = False
    _vtk_text_added = False

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

    # Unified phase color resources (shared with 2D views)
    cmap_name = None
    if isinstance(cmap_set, str):
        cmap_name = cmap_set.split('.', 1)[1] if cmap_set.startswith('cm.') else cmap_set
    elif cmap_set is None:
        cmap_name = 'batlow'
    else:
        # Non-string cmap provided; use default name for sampling purposes
        cmap_name = 'batlow'
    color_res = get_phase_color_resources(data, cmap_name=cmap_name, brightness=1.0)
    unique_vals = list(map(int, color_res.get('unique_ids', [])))
    final_phase_colors = dict(color_res.get('mapping', {}))
    # Allow user overrides per phase id
    if phase_colors is not None and isinstance(phase_colors, (dict,)):
        for pid, color in phase_colors.items():
            if isinstance(color, (list, tuple)) and len(color) == 3:
                final_phase_colors[int(pid)] = tuple(color)
    # Fallback if mapping empty (e.g., non-integer data): sample evenly for a guessed range
    if not final_phase_colors:
        # Guess phases from labels or data max
        n_guess = max(int(data.max()) + 1, len(labels))
        base = _resolve_colormap(cmap_set) if cmap_set is not None else cm.batlow
        if n_guess <= 1:
            final_phase_colors[0] = tuple(base(0.5)[:3])
            unique_vals = [0]
        else:
            for i in range(n_guess):
                t = i / (n_guess - 1)
                final_phase_colors[i] = tuple(base(t)[:3])
            unique_vals = list(range(n_guess))

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

    # Clamp slice indices to valid integer ranges and compute a cell-centered origin
    try:
        sx = int(max(0, min(nx - 1, int(sx))))
        sy = int(max(0, min(ny - 1, int(sy))))
        sz = int(max(0, min(nz - 1, int(sz))))
    except Exception:
        sx, sy, sz = nx // 2, ny // 2, nz // 2

    # Compute a cell-centered origin but clamp it away from the outermost
    # boundary so slicing doesn't fall outside the grid (which can produce
    # empty/transparent results). This keeps slices inside the volume.
    def _cell_center_clamp(idx, dim):
        if dim <= 1:
            return 0.0
        min_c = 0.5
        max_c = max(min_c, (dim - 1) - 0.5)  # dim-1-0.5 == dim-1.5
        return float(min(max(min_c, idx + 0.5), max_c))

    origin_coords = [
        _cell_center_clamp(sx, nx),
        _cell_center_clamp(sy, ny),
        _cell_center_clamp(sz, nz),
    ]

    grid = pv.ImageData()
    grid.dimensions = (nx, ny, nz)
    # Keep original 'phase' key for discrete rendering compatibility,
    # and also store numeric values under 'values' for continuous colormap
    grid.point_data["phase"] = data.flatten(order="F")
    try:
        grid.point_data["values"] = data.astype(float).flatten(order="F")
    except Exception:
        # Fallback: if casting fails, keep original array as-is
        grid.point_data["values"] = data.flatten(order="F")

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
    # Render full continuous colormap if requested (no discrete phase meshes)
    if full_cmap:
        # Resolve colormap: prefer provided cmap_set, otherwise use default
        # Resolve a CMas Crameri colormap when possible (prefer cmcrameri 'cm').
        cmap_obj = None
        if isinstance(cmap_set, str):
            # Allow 'cm.name' or just 'name'
            name = cmap_set.split('.', 1)[1] if cmap_set.startswith('cm.') else cmap_set
            # Prefer cm.<name> from cmcrameri if available
            if hasattr(cm, name):
                cmap_obj = getattr(cm, name)
            else:
                try:
                    cmap_obj = _resolve_colormap(cmap_set)
                except Exception:
                    cmap_obj = None
        elif cmap_set is None:
            # Default to a CMas Crameri map
            cmap_obj = cm.batlow
        else:
            # Non-string cmap: try resolving, else fall back to CMas default
            try:
                cmap_obj = _resolve_colormap(cmap_set)
            except Exception:
                cmap_obj = cm.batlow

        if cmap_obj is None:
            cmap_obj = cm.batlow

        # Determine scalar range and a simple opacity transfer function
        scalar_min = float(np.nanmin(data))
        scalar_max = float(np.nanmax(data))
        clim = (scalar_min, scalar_max)
        # Create a smooth opacity transfer (low -> mostly transparent, high -> opaque)
        # Ensure a small minimum alpha so the whole volume isn't invisible.
        min_alpha = 0.02
        opacity_tf = (min_alpha + (1.0 - min_alpha) * np.linspace(0.0, 1.0, 256)).tolist()

        # Add continuous volume rendering
        try:
            # Add volume without automatic scalar bar so we can enforce the scalar range
            # Use the 'values' scalar for continuous numeric rendering so the
            # colorbar reflects the true data range and not normalized labels.
            vol_actor = plotter.add_volume(
                grid,
                scalars='values',
                cmap=cmap_obj,
                opacity=opacity_tf,
                clim=clim,
                shade=True,
                scalar_bar_args=None
            )
            # Ensure the mapper (if available) uses the exact scalar range so the
            # scalar bar shows the real data values instead of a normalized 0-1 range.
            try:
                vol_actor.mapper.scalar_range = clim
            except Exception:
                # Some PyVista versions/actors may not expose mapper; ignore if so.
                pass

            # Add a scalar bar and set its range explicitly (only if requested)
            if show_legend:                
                try:
                    # Some PyVista backends don't pick up the LUT from a volume
                    # actor when drawing the scalar bar. As a robust fallback we
                    # create a tiny invisible plane with a linear scalar ramp and
                    # attach the scalar bar to that mesh so the colorbar colors
                    # exactly match the chosen colormap. The plane is translated
                    # far away so it won't be visible in the scene.
                    try:
                        # Create a vtkLookupTable from the chosen colormap and
                        # attach a vtkScalarBarActor directly to the renderer.
                        # This places the colorbar as a 2D actor and does not
                        # introduce any 3D geometry that could interfere with
                        # slicing or scene bounds.
                        try:
                            import vtk
                            n_colors = 256
                            lut = vtk.vtkLookupTable()
                            lut.SetNumberOfTableValues(n_colors)
                            lut.Build()
                            for ii in range(n_colors):
                                t = ii / float(n_colors - 1)
                                rgba = cmap_obj(t)
                                # cmap_obj may return RGBA with values 0..1
                                lut.SetTableValue(ii, float(rgba[0]), float(rgba[1]), float(rgba[2]), 1.0)

                            # Ensure the lookup table maps to the actual data range
                            try:
                                lut.SetRange(scalar_min, scalar_max)
                            except Exception:
                                pass

                            scalar_bar = vtk.vtkScalarBarActor()
                            scalar_bar.SetLookupTable(lut)
                            scalar_bar.SetTitle(colorbar_title)
                            # Move title to the left, center vertically, rotate 90º CCW
                            try:
                                scalar_bar.SetTitleSideToLeft()
                            except Exception:
                                pass
                            try:
                                scalar_bar.SetVerticalTitle(True)
                            except Exception:
                                pass
                            try:
                                tprop = scalar_bar.GetTitleTextProperty()
                                tprop.SetOrientation(90)  # 90º CCW
                                tprop.SetJustificationToCentered()
                                tprop.SetVerticalJustificationToCentered()
                            except Exception:
                                pass
                            # Position and size (normalized viewport coordinates)
                            try:
                                scalar_bar.SetPosition(pos_x, pos_y)
                                scalar_bar.SetWidth(width)
                                scalar_bar.SetHeight(height)
                            except Exception:
                                try:
                                    coord = scalar_bar.GetPositionCoordinate()
                                    coord.SetValue(pos_x, pos_y, 0)
                                except Exception:
                                    pass
                            # Use a fixed number of labels matching the plotted ticks
                            n_labels = 5
                            try:
                                scalar_bar.SetNumberOfLabels(n_labels)
                            except Exception:
                                # Older/newer VTK may not support SetNumberOfLabels
                                pass
                            # Remove tick labels by setting label format to empty
                            try:
                                scalar_bar.SetLabelFormat('')
                            except Exception:
                                pass
                            # Ensure the scalar bar text (title and labels) is
                            # drawn in black so it's readable on light backgrounds.
                            try:
                                tprop = scalar_bar.GetTitleTextProperty()
                                lprop = scalar_bar.GetLabelTextProperty()
                                tprop.SetColor(0.0, 0.0, 0.0)
                                lprop.SetColor(0.0, 0.0, 0.0)
                                # Set readable font sizes for title and labels
                                try:
                                    tprop.SetFontSize(12)
                                except Exception:
                                    pass
                                try:
                                    lprop.SetFontSize(20)
                                except Exception:
                                    pass
                            except Exception:
                                pass
                            # Remove the scalar_bar internal title - we'll draw a
                            # separate 2D text actor so its placement is independent
                            try:
                                scalar_bar.SetTitle('')
                            except Exception:
                                pass
                            # Add a separate 2D text actor for the colorbar title
                            try:
                                tx_off, ty_off = colorbar_title_offset
                                tx = pos_x + tx_off
                                ty = pos_y + ty_off
                                try:
                                    # Create a vtkTextActor placed in normalized viewport
                                    txt = vtk.vtkTextActor()
                                    txt.SetInput(colorbar_title)
                                    tprop2 = txt.GetTextProperty()
                                    tprop2.SetFontSize(int(colorbar_title_font_size))
                                    tprop2.SetColor(0.0, 0.0, 0.0)
                                    tprop2.SetOrientation(90)
                                    tprop2.SetJustificationToCentered()
                                    tprop2.SetVerticalJustificationToCentered()
                                    # Use normalized viewport coordinates
                                    try:
                                        pc = txt.GetPositionCoordinate()
                                        pc.SetCoordinateSystemToNormalizedViewport()
                                        pc.SetValue(tx, ty, 0)
                                    except Exception:
                                        try:
                                            txt.SetPosition(tx, ty)
                                        except Exception:
                                            pass
                                    plotter.renderer.AddActor2D(txt)
                                    _vtk_text_added = True
                                except Exception:
                                    # Fallback to PyVista text
                                    try:
                                        plotter.add_text(colorbar_title, position=(tx, ty), font_size=colorbar_title_font_size, color='black', rotation=90)
                                        _vtk_text_added = True
                                    except Exception:
                                        try:
                                            plotter.add_text(colorbar_title, position=(tx, ty), font_size=colorbar_title_font_size, color='black')
                                            _vtk_text_added = True
                                        except Exception:
                                            pass
                            except Exception:
                                pass
                            # Ensure the scalar bar orientation is vertical for a
                            # narrow left-side placement and that the lookup table
                            # range matches the data values used for tick generation.
                            try:
                                scalar_bar.SetOrientationToVertical()
                            except Exception:
                                pass
                            # Add as a 2D actor so it doesn't affect 3D bounds
                            try:
                                plotter.renderer.AddActor2D(scalar_bar)
                                _vtk_scalar_bar_used = True
                            except Exception:
                                plotter.renderer.AddActor(scalar_bar)
                                _vtk_scalar_bar_used = True
                        except Exception:
                            # Fallback to PyVista scalar bar if vtk is unavailable
                            try:
                                plotter.add_scalar_bar(
                                    title='',
                                    n_labels=0,  # Hide tick labels
                                    position_x=pos_x,
                                    position_y=pos_y,
                                    width=width,
                                    height=height,
                                    color='black',
                                    title_font_size=colorbar_title_font_size,
                                    label_font_size=1,  # Minimize font size
                                    label_format='',   # Remove tick labels
                                    vertical=True,     # Title vertical
                                    title_side='left', # Title on left
                                    title_orientation=90, # 90º CCW
                                    title_justify='center',
                                )
                                _pyvista_scalar_bar_added = True
                            except Exception:
                                # Last-resort fallback with default placement
                                        try:
                                            plotter.add_scalar_bar(title='', n_labels=0, color='black', title_font_size=colorbar_title_font_size, label_font_size=1, label_format='', vertical=True, title_side='left', title_orientation=90, title_justify='center', position_x=pos_x, position_y=pos_y, width=width, height=height)
                                        except Exception:
                                            try:
                                                plotter.add_scalar_bar(title='', n_labels=0, color='black', title_font_size=12, label_font_size=1, label_format='', vertical=True, title_side='left', title_orientation=90, title_justify='center', position_x=pos_x, position_y=pos_y, width=width, height=height)
                                            except Exception:
                                                plotter.add_scalar_bar(title='', n_labels=0, color='black')
                        # Ensure the scalar bar range matches the data
                        try:
                            plotter.update_scalar_bar_range(clim)
                        except Exception:
                            pass
                        # If VTK didn't add a text actor, add a separate
                        # PyVista text label for the colorbar title so its
                        # position is independent from the bar itself.
                        if not _vtk_text_added:
                            try:
                                try:
                                    # Try adding rotated text first
                                    plotter.add_text(colorbar_title, position=(tx, ty), font_size=colorbar_title_font_size, color='black', rotation=90)
                                except Exception:
                                    plotter.add_text(colorbar_title, position=(tx, ty), font_size=colorbar_title_font_size, color='black')
                            except Exception:
                                pass
                        # Force label/title font size on any scalar bar actor
                        # that may have been added (covers both our VTK actor
                        # and PyVista-managed scalar bars which also appear as
                        # vtkScalarBarActor in the renderer).
                        try:
                            import vtk
                            ren = plotter.renderer
                            # Try 2D actors first
                            try:
                                actors2d = ren.GetActors2D()
                                actors2d.InitTraversal()
                                while True:
                                    a = actors2d.GetNextActor()
                                    if a is None:
                                        break
                                    try:
                                        if a.IsA('vtkScalarBarActor'):
                                            try:
                                                tp = a.GetTitleTextProperty()
                                                lp = a.GetLabelTextProperty()
                                                tp.SetFontSize(12)
                                                lp.SetFontSize(20)
                                            except Exception:
                                                pass
                                    except Exception:
                                        pass
                            except Exception:
                                # Fallback: iterate view props
                                try:
                                    props = ren.GetViewProps()
                                    props.InitTraversal()
                                    while True:
                                        p = props.GetNextProp()
                                        if p is None:
                                            break
                                        try:
                                            if p.IsA('vtkScalarBarActor'):
                                                try:
                                                    tp = p.GetTitleTextProperty()
                                                    lp = p.GetLabelTextProperty()
                                                    tp.SetFontSize(12)
                                                    lp.SetFontSize(20)
                                                except Exception:
                                                    pass
                                        except Exception:
                                            pass
                                except Exception:
                                    pass
                        except Exception:
                            # If VTK not available, nothing to force here
                            pass
                    except Exception:
                        # If scalar bar helpers are unavailable, ignore and rely on defaults
                        pass
                except Exception:
                    # If scalar bar helpers are unavailable, ignore and rely on defaults
                    pass
            # If user requested slices in combination with full_cmap, add colored
            # slice planes using the numeric 'values' scalar so they match the
            # continuous colormap (this mirrors the 'combined' mode behavior).
            try:
                if mode in ('slices', 'combined'):
                    origin = origin_coords
                    slice_xy = grid.slice(normal=[0, 0, 1], origin=origin)
                    slice_xz = grid.slice(normal=[0, 1, 0], origin=origin)
                    slice_yz = grid.slice(normal=[1, 0, 0], origin=origin)
                    slice_planes = [slice_xy, slice_xz, slice_yz]
                    for i, plane in enumerate(slice_planes):
                        if plane.n_cells > 0:
                            plotter.add_mesh(
                                plane,
                                scalars='values',
                                cmap=cmap_obj,
                                opacity=slice_opacity_value,
                                show_edges=False,
                                label=None if i > 0 else 'Slice',
                                show_scalar_bar=False,
                            )
            except Exception:
                # If slicing fails (older pyvista), ignore and continue
                pass
        except Exception:
            # Fallback: if add_volume not available or fails, raise informative error
            raise RuntimeError('Continuous colormap volume rendering failed. Ensure PyVista supports add_volume and the data are finite numeric scalars.')

        # Continue to the shared post-rendering steps (bounds, legend/scalar bar, axes, title, camera)
    # Force camera and bounds to the grid (model) so added invisible helpers
    # do not change the displayed extents/ticks. Prefer resetting to the
    # ImageData grid itself when possible.
    # Defensive cleanup: if the user requested no legend, remove any
    # scalar-bar actors that may have been added by fallbacks (VTK actor
    # or PyVista scalar bar). This handles cases where a scalar bar was
    # created despite `show_legend=False`.
    if not show_legend:
        try:
            try:
                import vtk
                ren = plotter.renderer
                # Try to remove 2D scalar bar actors (VTK ScalarBarActor)
                try:
                    actors2d = ren.GetActors2D()
                    # different VTK versions expose traversal methods
                    try:
                        actors2d.InitTraversal()
                        while True:
                            a = actors2d.GetNextActor()
                            if a is None:
                                break
                            try:
                                if a.IsA('vtkScalarBarActor'):
                                    ren.RemoveActor2D(a)
                            except Exception:
                                pass
                    except Exception:
                        # Fallback traversal API
                        try:
                            n = actors2d.GetNumberOfItems()
                            for _ in range(n):
                                a = actors2d.GetNextItem()
                                try:
                                    if a.IsA('vtkScalarBarActor'):
                                        ren.RemoveActor2D(a)
                                except Exception:
                                    pass
                        except Exception:
                            pass
                except Exception:
                    # Try removing any view props matching scalar bar type
                    try:
                        props = ren.GetViewProps()
                        try:
                            props.InitTraversal()
                            while True:
                                p = props.GetNextProp()
                                if p is None:
                                    break
                                try:
                                    if p.IsA('vtkScalarBarActor'):
                                        ren.RemoveActor(p)
                                except Exception:
                                    pass
                        except Exception:
                            pass
                    except Exception:
                        pass
            except Exception:
                # If VTK isn't available, ignore and try PyVista removal below
                pass
            # Try to remove any PyVista scalar bar if present
            try:
                # remove_scalar_bar exists in some PyVista versions
                if hasattr(plotter, 'remove_scalar_bar'):
                    plotter.remove_scalar_bar()
            except Exception:
                pass
        except Exception:
            pass
    try:
        # Call reset_camera without positional args to avoid PyVista deprecation
        # warning about positional 'render' argument. Resetting without args
        # recenters the camera to the scene (including the volume and slices).
        plotter.reset_camera()
    except Exception:
        try:
            plotter.reset_camera()
        except Exception:
            pass
    # Render phases/slices (skip when full_cmap is True)
    if (not full_cmap) and mode == '3d':
        phase_opacity_map = {}
        if isinstance(phase_opacity, dict):
            # Respect provided mapping; otherwise default later
            phase_opacity_map = {int(k): float(v) for k, v in phase_opacity.items()}
        elif isinstance(phase_opacity, (list, tuple)):
            for pid, opacity_val in zip(unique_vals, phase_opacity):
                phase_opacity_map[int(pid)] = float(opacity_val)
        else:
            for pid in unique_vals:
                phase_opacity_map[int(pid)] = slice_opacity_value
        for pid, opacity_val in phase_opacity_map.items():
            if opacity_val <= 0.0:
                continue
            opacity_val = max(0.0, min(1.0, opacity_val))
            pname = labels.get(int(pid), f"Phase {int(pid)}") if isinstance(labels, dict) else f"Phase {int(pid)}"
            phase_mesh = grid.threshold(value=[int(pid) - 0.1, int(pid) + 0.1], scalars='phase')
            if phase_mesh.n_cells > 0:
                plotter.add_mesh(
                    phase_mesh,
                    color=final_phase_colors.get(int(pid), (1.0, 1.0, 1.0)),
                    opacity=opacity_val,
                    show_edges=show_3d_edges,
                    edge_color=edge_color,
                    label=pname,
                    smooth_shading=True
                )
    elif (not full_cmap) and mode in ('slices', 'combined'):
        origin = origin_coords
        slice_xy = grid.slice(normal=[0, 0, 1], origin=origin)
        slice_xz = grid.slice(normal=[0, 1, 0], origin=origin)
        slice_yz = grid.slice(normal=[1, 0, 0], origin=origin)
        slice_planes = [slice_xy, slice_xz, slice_yz]
        for pid in unique_vals:
            pname = labels.get(int(pid), f"Phase {int(pid)}") if isinstance(labels, dict) else f"Phase {int(pid)}"
            for i, plane in enumerate(slice_planes):
                p_slice = plane.threshold(value=[int(pid) - 0.1, int(pid) + 0.1], scalars='phase')
                if p_slice.n_cells > 0:
                    plotter.add_mesh(
                        p_slice,
                        color=final_phase_colors.get(int(pid), (1.0, 1.0, 1.0)),
                        opacity=slice_opacity_value,
                        show_edges=False,
                        label=pname if i == 0 else None,
                        show_scalar_bar=False,
                    )
        if mode == 'combined' and phase_opacity is not None:
            phase_opacity_map = {}
            if isinstance(phase_opacity, dict):
                phase_opacity_map = {int(k): float(v) for k, v in phase_opacity.items()}
            elif isinstance(phase_opacity, (list, tuple)):
                for pid, opacity_val in zip(unique_vals, phase_opacity):
                    phase_opacity_map[int(pid)] = float(opacity_val)
            for pid, opacity_val in phase_opacity_map.items():
                if opacity_val <= 0.0:
                    continue
                opacity_val = max(0.0, min(1.0, opacity_val))
                pname = labels.get(int(pid), f"Phase {int(pid)}") if isinstance(labels, dict) else f"Phase {int(pid)}"
                phase_mesh = grid.threshold(value=[int(pid) - 0.1, int(pid) + 0.1], scalars='phase')
                if phase_mesh.n_cells > 0:
                    plotter.add_mesh(
                        phase_mesh,
                        color=final_phase_colors.get(int(pid), (1.0, 1.0, 1.0)),
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
        # Only add the discrete legend when NOT using the continuous colormap.
        # The continuous path (`full_cmap=True`) already adds and configures
        # a scalar bar earlier, so adding another here creates duplicate bars
        # with conflicting ranges/ticks.
        if not full_cmap:
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

    # Remove any PyVista-managed scalar bar (often added as a horizontal bar at
    # the bottom) to avoid duplicate/wrong colorbars. We keep VTK scalar bar
    # actors we added directly (those live in the renderer as vtkScalarBarActor
    # and are not removed by plotter.remove_scalar_bar()).
    try:
        # Only remove PyVista-managed scalar bars if we didn't add one ourselves
        if hasattr(plotter, 'remove_scalar_bar') and (not _pyvista_scalar_bar_added):
            try:
                plotter.remove_scalar_bar()
            except Exception:
                # Some versions may raise if no scalar bar present; ignore
                pass
    except Exception:
        pass

    plotter.camera_position = 'iso'
    plotter.camera.zoom(camera_zoom if camera_zoom is not None else default_camera_zoom)
    win_size = window_size or win_size_default
    view_shift_x = view_shift_x_rel * win_size[0]
    view_shift_y = view_shift_y_rel * win_size[1]
    fp = plotter.camera.focal_point
    plotter.camera.focal_point = (fp[0] + view_shift_x, fp[1] + view_shift_y, fp[2])

    try:
        n_phases_print = len(unique_vals)
    except Exception:
        n_phases_print = int(data.max()) + 1
    print(f"3D volume rendering with {n_phases_print} phases")
    
    # In interactive mode (notebooks), show the plot and return the image
    # In off-screen mode (scripts), just return the plotter for saving
    if not off_screen:
        return plotter.show()
    else:
        return plotter
