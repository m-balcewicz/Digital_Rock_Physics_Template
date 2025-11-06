# Image Visualization Examples

This directory contains examples for the Digital Rock Physics image visualization functions.

## Quick Start

```python
import drp_template.tools as tools
import drp_template.image as image

# Create sample data
data = tools.create_binary_model_3d(nx=80, ny=80, nz=80, seed=42)
labels = {0: 'Pore Space', 1: 'Solid Matrix'}

# Basic 3D visualization
image.volume_rendering(data, mode='3d', labels=labels)
```

## Available Examples

### 📓 `volume_rendering.ipynb`
**Complete volume rendering feature demonstration**

Covers all volume rendering capabilities:
- ✅ Slice opacity control
- ✅ Edge visualization on 3D meshes
- ✅ Custom phase colors
- ✅ Lighting presets (bright, soft, dramatic, custom)
- ✅ Rotation animations (GIF/MP4/AVI)
- ✅ Combined mode (slices + 3D)
- ✅ Window-size independent positioning

**Start here** for a comprehensive overview of all features.

## Documentation

### 📄 `VOLUME_RENDERING_FEATURES.md`
Complete technical documentation including:
- Detailed parameter descriptions
- Use cases and best practices
- Performance considerations
- Troubleshooting guide
- Future enhancements

## Core Functions

### `volume_rendering()`
Main visualization function with three modes:

```python
# Orthogonal slices
image.volume_rendering(data, mode='slices')

# 3D volumetric rendering
image.volume_rendering(data, mode='3d', phase_opacity={0: 0.7})

# Combined: slices + selective 3D rendering
image.volume_rendering(data, mode='combined', 
                      slice_opacity=0.3,
                      phase_opacity={0: 0.8})
```

### `create_rotation_animation()`
Generate rotating animations:

```python
image.create_rotation_animation(
    data,
    save_path='output/rotation.gif',
    mode='3d',
    phase_opacity={0: 0.6},
    n_frames=60,
    fps=15,
    rotation_axis='z'
)
```

### `get_lighting_preset()`
Get pre-configured lighting:

```python
# Use preset directly
image.volume_rendering(data, mode='3d', lighting='dramatic')

# Or customize preset
lighting = image.get_lighting_preset('bright')
lighting['key_light']['intensity'] = 1.5
image.volume_rendering(data, mode='3d', lighting=lighting)
```

## Feature Summary

| Feature | Parameter | Values |
|---------|-----------|--------|
| **Rendering Mode** | `mode` | `'slices'`, `'3d'`, `'combined'` |
| **Phase Opacity** | `phase_opacity` | `{phase_id: opacity}` or `[opacity_list]` |
| **Slice Opacity** | `slice_opacity` | `0.0` to `1.0` |
| **3D Edges** | `show_3d_edges` | `True`/`False` |
| **Edge Color** | `edge_color` | Color name or `(R,G,B)` |
| **Custom Colors** | `phase_colors` | `{phase_id: (R,G,B)}` |
| **Lighting** | `lighting` | `'bright'`, `'soft'`, `'dramatic'`, `'custom'`, `'default'`, `'none'` |
| **Window Size** | `window_size` | `[width, height]` in pixels |

## Configuration

Default settings are in `drp_template/default_params/default_figure_settings.json`:

```json
{
  "volume_rendering": {
    "view_shift_x": 0.075,      // Relative to window width
    "view_shift_y": -0.055,     // Relative to window height
    "camera_zoom": 0.85,
    "window_size": [2400, 1800],
    "lighting": "custom",
    "opacity_slice": 1.0
  }
}
```

## Tips & Tricks

### 1. Window-Size Independent Rendering
Camera positioning scales automatically - same composition at any resolution:

```python
# Preview
volume_rendering(data, window_size=[800, 600])

# Publication quality
volume_rendering(data, window_size=[3200, 2400])
```

### 2. Transparent Slices in Combined Mode
Make slices provide context without obscuring 3D structures:

```python
volume_rendering(data, mode='combined',
                slice_opacity=0.2,
                phase_opacity={0: 0.8})
```

### 3. Structure Analysis with Edges
Visualize mesh topology for better understanding:

```python
volume_rendering(data, mode='3d',
                show_3d_edges=True,
                edge_color='white',
                dark_mode=True)
```

### 4. Custom Color Schemes
Override colormap for domain-specific coloring:

```python
volume_rendering(data, mode='3d',
                phase_colors={
                    0: (1.0, 0.0, 0.0),  # Red pores
                    1: (0.0, 0.5, 1.0)   # Blue matrix
                })
```

### 5. Professional Lighting
Use presets or customize for publication:

```python
# Dramatic lighting for striking visuals
volume_rendering(data, lighting='dramatic')

# Soft lighting for even illumination
volume_rendering(data, lighting='soft')
```

## Common Workflows

### Pore Network Visualization
```python
# Transparent matrix, highlighted pores
image.volume_rendering(
    data,
    mode='3d',
    phase_opacity={0: 0.8, 1: 0.2},
    lighting='dramatic',
    labels={0: 'Pore Network', 1: 'Rock Matrix'}
)
```

### Multi-Scale Analysis
```python
# Context slices + detailed 3D region
image.volume_rendering(
    data,
    mode='combined',
    slice_indices=[40, 40, 40],
    slice_opacity=0.25,
    phase_opacity={0: 0.7},
    show_3d_edges=True
)
```

### Publication Figure
```python
# High-resolution with all features
image.volume_rendering(
    data,
    mode='combined',
    window_size=[3200, 2400],
    slice_opacity=0.15,
    phase_opacity={0: 0.85},
    show_3d_edges=True,
    edge_color='yellow',
    lighting='bright',
    save_path='output/publication_figure.png'
)
```

### Animation for Presentation
```python
# Smooth rotation with custom styling
image.create_rotation_animation(
    data,
    save_path='output/presentation.mp4',
    mode='3d',
    phase_opacity={0: 0.6},
    lighting='soft',
    window_size=[1920, 1080],
    n_frames=120,
    fps=30,
    rotation_axis='z'
)
```

## Requirements

- Python 3.7+
- PyVista >= 0.43.0
- trame >= 3.4 (for interactive notebooks)
- cmcrameri (for scientific colormaps)

## Support

For issues or questions:
1. Check `VOLUME_RENDERING_FEATURES.md` for detailed documentation
2. Review example notebooks
3. Check function docstrings: `help(image.volume_rendering)`

---

**Last Updated**: November 6, 2025
