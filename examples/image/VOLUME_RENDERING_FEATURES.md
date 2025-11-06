# Volume Rendering Features Guide

This document describes all the features implemented in the `volume_rendering` function and the `create_rotation_animation` utility.

## Table of Contents

1. [Slice Opacity Control](#1-slice-opacity-control)
2. [Edge Visualization](#2-edge-visualization)
3. [Custom Phase Colors](#3-custom-phase-colors)
4. [Lighting Presets](#4-lighting-presets)
5. [Rotation Animation](#5-rotation-animation)
6. [Window-Size Independent Camera Positioning](#6-window-size-independent-camera-positioning)

---

## 1. Slice Opacity Control

**Feature**: Independent control of slice plane opacity, separate from 3D mesh opacity.

### Parameter
```python
slice_opacity : float or None
    Opacity for slice planes (0.0-1.0). If None, uses default from settings (1.0).
```

### Use Cases
- Make slices semi-transparent in `combined` mode so 3D meshes behind them are visible
- Create layered visualizations with varying transparency levels
- Focus attention on 3D structures while keeping spatial context

### Examples

```python
# Semi-transparent slices (30%) with solid 3D pores
volume_rendering(
    data,
    mode='combined',
    slice_opacity=0.3,
    phase_opacity={0: 1.0},
    labels=labels
)

# Very faint slices for context only
volume_rendering(
    data,
    mode='combined',
    slice_opacity=0.1,
    phase_opacity={0: 0.8}
)
```

---

## 2. Edge Visualization

**Feature**: Display mesh edges on 3D volumetric renderings for better structural understanding.

### Parameters
```python
show_3d_edges : bool, default False
    If True, show edges on 3D volumetric meshes.

edge_color : str or tuple, default 'black'
    Color for edges. Can be color name ('white', 'black', 'red') or RGB tuple (R, G, B).
```

### Use Cases
- Visualize mesh structure and resolution
- Better understand phase boundaries
- Create technical/wireframe-style visualizations
- Enhance contrast on dark or light backgrounds

### Examples

```python
# White edges on dark background
volume_rendering(
    data,
    mode='3d',
    show_3d_edges=True,
    edge_color='white',
    dark_mode=True
)

# Custom color edges
volume_rendering(
    data,
    mode='3d',
    show_3d_edges=True,
    edge_color=(1.0, 1.0, 0.0),  # Yellow edges
    phase_opacity={0: 0.7}
)

# Edges in combined mode
volume_rendering(
    data,
    mode='combined',
    show_3d_edges=True,
    edge_color='red',
    phase_opacity={0: 0.5}
)
```

---

## 3. Custom Phase Colors

**Feature**: Override default colormap with custom RGB colors for each phase.

### Parameter
```python
phase_colors : dict or None
    Override default phase colors. Dict mapping {phase_id: (R, G, B)} with RGB in [0,1].
    If None, colors are generated from cmap_set.
    Example: {0: (1.0, 0.0, 0.0), 1: (0.0, 0.0, 1.0)}
```

### Use Cases
- Apply domain-specific color schemes (e.g., blue for water, brown for minerals)
- Match colors to publications or branding requirements
- Create high-contrast visualizations
- Highlight specific phases with distinctive colors

### Examples

```python
# Red pores, blue matrix
custom_colors = {
    0: (1.0, 0.0, 0.0),  # Bright red
    1: (0.0, 0.5, 1.0)   # Light blue
}

volume_rendering(
    data,
    mode='3d',
    phase_colors=custom_colors,
    labels={'0': 'Pores', '1': 'Matrix'}
)

# Grayscale with one highlighted phase
grayscale_with_highlight = {
    0: (1.0, 0.5, 0.0),  # Orange pores (highlighted)
    1: (0.5, 0.5, 0.5),  # Gray matrix
    2: (0.3, 0.3, 0.3)   # Dark gray minerals
}

volume_rendering(
    data,
    mode='3d',
    phase_colors=grayscale_with_highlight,
    phase_opacity={0: 1.0, 1: 0.3, 2: 0.3}
)
```

### Notes
- RGB values must be in range [0, 1]
- Missing phases will be filled in with colormap colors
- Works with all rendering modes: 'slices', '3d', 'combined'

---

## 4. Lighting Presets

**Feature**: Pre-configured lighting setups for different visualization styles.

### Function
```python
get_lighting_preset(preset='default')
```

### Available Presets

| Preset | Description | Key Light Intensity | Ambient Intensity | Use Case |
|--------|-------------|-------------------|------------------|----------|
| `'bright'` | High intensity, strong ambient | 1.2 | 0.5 | Clear, well-lit scenes |
| `'soft'` | Moderate light, high ambient | 0.7 | 0.6 | Soft shadows, gentle look |
| `'dramatic'` | Strong directional, minimal ambient | 1.5 | 0.1 | High contrast, dramatic effect |
| `'default'` | PyVista's default lighting | - | - | Standard rendering |
| `'custom'` | Returns None for manual config | - | - | Full control |
| `'none'` | No lighting | 0 | 0 | Flat shading |

### Usage

**Direct preset application:**
```python
# Use preset directly
volume_rendering(
    data,
    mode='3d',
    lighting='dramatic',
    phase_opacity={0: 0.8}
)
```

**Get and modify preset:**
```python
# Get preset configuration
lighting_config = get_lighting_preset('dramatic')

# Customize
lighting_config['key_light']['intensity'] = 2.0
lighting_config['ambient_intensity'] = 0.05

# Apply customized lighting
volume_rendering(
    data,
    mode='3d',
    lighting=lighting_config
)
```

### Preset Details

**Bright:**
- Position: (400, 400, 500)
- Key intensity: 1.2
- Ambient: 0.5
- Best for: Educational materials, presentations

**Soft:**
- Position: (300, 300, 350)
- Key intensity: 0.7
- Ambient: 0.6
- Best for: Publications, reports

**Dramatic:**
- Position: (500, 200, 600)
- Key intensity: 1.5
- Ambient: 0.1
- Best for: Hero shots, marketing materials

---

## 5. Rotation Animation

**Feature**: Create rotating GIF or MP4 animations of volume renderings.

### Function
```python
create_rotation_animation(
    data,
    save_path,
    mode='3d',
    n_frames=60,
    fps=15,
    rotation_axis='z',
    **volume_rendering_kwargs
)
```

### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `data` | np.ndarray | required | 3D labeled array |
| `save_path` | str | required | Output path (.gif, .mp4, .avi) |
| `n_frames` | int | 60 | Number of frames |
| `fps` | int | 15 | Frames per second |
| `rotation_axis` | str | 'z' | Rotation axis: 'x', 'y', or 'z' |
| `mode` | str | '3d' | 'slices', '3d', or 'combined' |
| `phase_opacity` | dict/list | None | Phase opacity control |
| `lighting` | str/dict | 'custom' | Lighting preset or config |
| All other parameters from `volume_rendering` |

### Use Cases
- Present dynamic 3D structures
- Explore complex geometries from all angles
- Create supplementary materials for publications
- Social media content
- Presentations and conferences

### Examples

**Basic rotation:**
```python
create_rotation_animation(
    data,
    save_path='output/rotation.gif',
    mode='3d',
    phase_opacity={0: 0.6},
    n_frames=36,
    fps=12
)
```

**High-quality MP4:**
```python
create_rotation_animation(
    data,
    save_path='output/high_res.mp4',
    mode='3d',
    phase_opacity={0: 0.7, 1: 0.3},
    n_frames=120,  # Smooth rotation
    fps=30,        # Film-quality
    window_size=[1920, 1080],  # Full HD
    lighting='dramatic'
)
```

**Combined mode animation:**
```python
create_rotation_animation(
    data,
    save_path='output/combined.gif',
    mode='combined',
    slice_indices=[40, 40, 40],
    slice_opacity=0.3,
    phase_opacity={0: 0.8},
    n_frames=60,
    fps=15,
    rotation_axis='z',
    show_3d_edges=True,
    edge_color='white',
    dark_mode=True
)
```

**Custom colors and lighting:**
```python
create_rotation_animation(
    data,
    save_path='output/custom_rotation.gif',
    mode='3d',
    phase_colors={0: (1.0, 0.3, 0.0), 1: (0.2, 0.2, 0.8)},
    phase_opacity={0: 0.7},
    lighting='bright',
    n_frames=72,
    fps=18,
    title="Pore Network Rotation"
)
```

### Tips
- **Frame count**: 36 frames = fast, 60 frames = smooth, 120+ frames = very smooth
- **FPS**: 12 fps = standard GIF, 15 fps = smooth, 24-30 fps = film quality
- **File format**: Use .gif for web/presentations, .mp4 for high quality, .avi for uncompressed
- **Rotation axis**: 'z' for vertical rotation, 'y' for horizontal tumbling, 'x' for sideways roll
- **File size**: More frames + higher FPS + larger window = larger file size

### Output Formats
- **GIF**: Widely compatible, good for web, limited colors
- **MP4**: High quality, smaller file size, good compression
- **AVI**: Uncompressed, highest quality, large file size

---

## 6. Window-Size Independent Camera Positioning

**Feature**: Camera view shifts that scale automatically with window size.

### Configuration
The camera positioning uses relative values in `default_figure_settings.json`:

```json
"view_shift_x": 0.075,   // 7.5% of window width
"view_shift_y": -0.055   // -5.5% of window height
```

### Benefits
- **Automatic Scaling**: Camera positioning adapts to any window size
- **Consistent Composition**: Same visual layout whether using `[800, 600]` or `[2400, 1800]`
- **Easy Adjustment**: Percentage-based values are more intuitive than absolute pixels

### Use Cases
- Maintain consistent visualization appearance across different output sizes
- Create publication-ready images at different resolutions
- Generate animations at various sizes without repositioning

### Example
```python
# Small preview - camera positioning scales automatically
volume_rendering(data, window_size=[800, 600])

# High-resolution output - same visual composition
volume_rendering(data, window_size=[3200, 2400])
```

### Manual Override
You can still provide absolute view shift values if needed:

```python
volume_rendering(
    data,
    view_shift=(100, -50)  # Absolute pixel shifts
)
```

---

## Complete Feature Summary

| Feature | Parameter | Type | Default | Modes |
|---------|-----------|------|---------|-------|
| **Slice Opacity** | `slice_opacity` | float | None | slices, combined |
| **3D Edges** | `show_3d_edges` | bool | False | 3d, combined |
| **Edge Color** | `edge_color` | str/tuple | 'white' | 3d, combined |
| **Custom Colors** | `phase_colors` | dict | None | all modes |
| **Lighting Preset** | `lighting` | str/dict | 'custom' | all modes |
| **Animation** | `create_rotation_animation()` | function | - | all modes |
| **View Shift** | `view_shift_x/y` | float | 0.075/-0.055 | all modes |

---

## Example: Using All Features Together

```python
from drp_template.image import volume_rendering, create_rotation_animation

# Define custom colors
colors = {
    0: (0.0, 0.8, 1.0),  # Cyan pores
    1: (0.8, 0.8, 0.8)   # Gray matrix
}

# Static combined rendering with all features
volume_rendering(
    data,
    mode='combined',
    slice_indices=[40, 40, 40],
    slice_opacity=0.2,
    phase_opacity={0: 0.8},
    show_3d_edges=True,
    edge_color='yellow',
    phase_colors=colors,
    lighting='bright',
    labels=labels,
    title="Complete Feature Showcase",
    dark_mode=True,
    window_size=[1400, 900],
    save_path='output/showcase.png'
)

# Animated version
create_rotation_animation(
    data,
    save_path='output/showcase_animation.gif',
    mode='combined',
    slice_indices=[40, 40, 40],
    slice_opacity=0.2,
    phase_opacity={0: 0.8},
    show_3d_edges=True,
    edge_color='yellow',
    phase_colors=colors,
    lighting='bright',
    labels=labels,
    title="Rotating Showcase",
    dark_mode=True,
    n_frames=60,
    fps=15,
    window_size=[1200, 900]
)
```

---

## Migration Guide

### From Basic to Advanced

**Before (basic usage):**
```python
volume_rendering(data, mode='combined', phase_opacity={0: 0.5})
```

**After (with new features):**
```python
volume_rendering(
    data,
    mode='combined',
    phase_opacity={0: 0.5},
    slice_opacity=0.3,           # NEW: Control slice transparency
    show_3d_edges=True,          # NEW: Show mesh structure
    edge_color='white',          # NEW: Edge color
    phase_colors={0: (1,0,0)},   # NEW: Custom red color for pores
    lighting='dramatic'          # NEW: Preset lighting
)
```

### Backward Compatibility

All new features are **optional** and **backward compatible**:
- Existing code will continue to work without changes
- Default values maintain previous behavior
- New parameters are opt-in

---

## Best Practices

### 1. Slice Opacity in Combined Mode
- Use `slice_opacity=0.2-0.4` for subtle context
- Use `slice_opacity=0.6-0.8` for balanced visualization
- Use `slice_opacity=1.0` (default) for traditional slices

### 2. Edge Visualization
- Use white edges on dark backgrounds
- Use black/dark edges on light backgrounds
- Reduce 3D mesh opacity when showing edges for clarity

### 3. Custom Colors
- Maintain sufficient contrast between phases
- Use colorblind-friendly palettes when possible
- Test colors in both light and dark modes

### 4. Lighting
- Use 'bright' for educational/presentation materials
- Use 'soft' for publications and reports
- Use 'dramatic' for hero shots and marketing
- Customize presets for specific needs

### 5. Animations
- 36-60 frames for web/presentations
- 120+ frames for smooth professional animations
- Use 12-15 fps for GIFs, 24-30 fps for MP4s
- Compress large animations for sharing

---

## Performance Considerations

- **Edge visualization**: Adds minimal overhead
- **Custom colors**: No performance impact
- **Lighting presets**: Same as custom lighting
- **Animations**: Scales linearly with frame count
- **Slice opacity**: No performance impact

---

## Troubleshooting

### Issue: Edges too thick/thin
**Solution**: Adjust with PyVista settings (future enhancement)

### Issue: Animation file too large
**Solution**: 
- Reduce `n_frames`
- Reduce `window_size`
- Use .mp4 instead of .gif
- Compress output file

### Issue: Custom colors not showing
**Solution**: Ensure RGB values are in [0, 1] range, not [0, 255]

### Issue: Lighting too dark/bright
**Solution**: Get preset, modify intensity values, then apply

---

## Future Enhancements

1. Multiple slice positions per direction
2. Adjustable edge line width
3. More lighting presets (studio, outdoor, etc.)
4. Camera path animations (not just rotation)
5. Interactive widgets for Jupyter notebooks
6. Batch processing for parameter studies

---

## Implementation Status

### ✅ Completed Features
- Slice opacity control
- Edge visualization on 3D meshes
- Custom phase colors
- Lighting presets (6 presets available)
- Rotation animation
- Window-size independent camera positioning

### 🔄 Planned Features
- Multiple slice positions per direction
- Adjustable edge line width
- Additional lighting presets
- Complex camera path animations
- Interactive Jupyter widgets

---

## References

- PyVista Documentation: https://docs.pyvista.org
- CMCrameri Colormaps: https://www.fabiocrameri.ch/colourmaps/
- Example Notebook: `volume_rendering.ipynb`

---

**Last Updated**: November 6, 2025
**Author**: Digital Rock Physics Template Team

