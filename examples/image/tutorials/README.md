# Image Tutorials & Volume Rendering Guide

This document unifies the tutorials overview and the complete Volume Rendering features guide.

## Tutorials Overview

Interactive, step-by-step notebooks teaching image workflows. Start from these:

- get_grayscale_histogram.ipynb — grayscale histogram exploration
- get_colored_histogram.ipynb — thresholded/colored histograms
- volume_rendering.ipynb — comprehensive volume rendering demo

Each tutorial aims to:
1. Load example data from `examples/data/`
2. Explain the goal and context
3. Show incremental code blocks
4. Summarize results with next steps

---

## Quick Start

```python
import drp_template.model as model
import drp_template.image as image

# Create sample data
data = model.create_binary_model_3d(nx=80, ny=80, nz=80, seed=42)
labels = {0: 'Pore Space', 1: 'Solid Matrix'}

# Basic 3D visualization
image.volume_rendering(data, mode='3d', labels=labels)
```

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

---

## Volume Rendering Features Guide

This section summarizes all features available in `volume_rendering` and `create_rotation_animation`.

### Table of Contents

1. [Slice Opacity Control](#1-slice-opacity-control)
2. [Edge Visualization](#2-edge-visualization)
3. [Custom Phase Colors](#3-custom-phase-colors)
4. [Lighting Presets](#4-lighting-presets)
5. [Rotation Animation](#5-rotation-animation)
6. [Window-Size Independent Camera Positioning](#6-window-size-independent-camera-positioning)

---

### 1. Slice Opacity Control

Feature: Independent control of slice plane opacity, separate from 3D mesh opacity.

Parameter:

```python
slice_opacity : float or None
    Opacity for slice planes (0.0-1.0). If None, uses default from settings (1.0).
```

Use cases:
- Make slices semi-transparent in `combined` mode so 3D meshes behind them are visible
- Create layered visualizations with varying transparency levels
- Focus attention on 3D structures while keeping spatial context

Examples:

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

### 2. Edge Visualization

Feature: Display mesh edges on 3D volumetric renderings for better structural understanding.

Parameters:

```python
show_3d_edges : bool, default False
edge_color : str or tuple, default 'black'
```

Use cases:
- Visualize mesh structure and resolution
- Better understand phase boundaries
- Create technical/wireframe-style visualizations
- Enhance contrast on dark or light backgrounds

Examples:

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

### 3. Custom Phase Colors

Feature: Override default colormap with custom RGB colors for each phase.

Parameter:

```python
phase_colors : dict or None
    # {phase_id: (R, G, B)} with RGB in [0,1]
```

Use cases:
- Apply domain-specific color schemes
- Match colors to publications or branding requirements
- Create high-contrast visualizations
- Highlight specific phases with distinctive colors

Examples:

```python
# Red pores, blue matrix
custom_colors = {
    0: (1.0, 0.0, 0.0),
    1: (0.0, 0.5, 1.0)
}
volume_rendering(data, mode='3d', phase_colors=custom_colors, labels={'0': 'Pores', '1': 'Matrix'})

# Grayscale with one highlighted phase
grayscale_with_highlight = {0: (1.0, 0.5, 0.0), 1: (0.5, 0.5, 0.5), 2: (0.3, 0.3, 0.3)}
volume_rendering(data, mode='3d', phase_colors=grayscale_with_highlight, phase_opacity={0: 1.0, 1: 0.3, 2: 0.3})
```

Notes:
- RGB values must be in range [0, 1]
- Missing phases will be filled with colormap colors
- Works with all rendering modes: 'slices', '3d', 'combined'

---

### 4. Lighting Presets

Feature: Pre-configured lighting setups for different visualization styles.

Function:

```python
get_lighting_preset(preset='default')
```

Available presets: `'bright'`, `'soft'`, `'dramatic'`, `'default'`, `'custom'`, `'none'`

Usage:

```python
# Direct
volume_rendering(data, mode='3d', lighting='dramatic', phase_opacity={0: 0.8})

# Modify a preset
cfg = get_lighting_preset('dramatic')
cfg['key_light']['intensity'] = 2.0
cfg['ambient_intensity'] = 0.05
volume_rendering(data, mode='3d', lighting=cfg)
```

---

### 5. Rotation Animation

Feature: Create rotating GIF/MP4 animations of volume renderings.

Function:

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

Examples:

```python
# Basic rotation
create_rotation_animation(data, save_path='output/rotation.gif', mode='3d', phase_opacity={0: 0.6}, n_frames=36, fps=12)

# High-quality MP4
create_rotation_animation(data, save_path='output/high_res.mp4', mode='3d', phase_opacity={0: 0.7, 1: 0.3}, n_frames=120, fps=30, window_size=[1920, 1080], lighting='dramatic')
```

---

### 6. Window-Size Independent Camera Positioning

Camera view shifts scale automatically with window size:

```json
"view_shift_x": 0.075,
"view_shift_y": -0.055
```

Benefits:
- Automatic scaling across resolutions
- Consistent composition
- Easy relative tuning

Examples:

```python
volume_rendering(data, window_size=[800, 600])
volume_rendering(data, window_size=[3200, 2400])
```

---

## Feature Summary

| Feature | Parameter | Values |
|---------|-----------|--------|
| Rendering Mode | `mode` | `'slices'`, `'3d'`, `'combined'` |
| Phase Opacity | `phase_opacity` | `{phase_id: opacity}` or list |
| Slice Opacity | `slice_opacity` | `0.0` to `1.0` |
| 3D Edges | `show_3d_edges` | `True`/`False` |
| Edge Color | `edge_color` | Color name or `(R,G,B)` |
| Custom Colors | `phase_colors` | `{phase_id: (R,G,B)}` |
| Lighting | `lighting` | `'bright'`, `'soft'`, `'dramatic'`, `'custom'`, `'default'`, `'none'` |
| Window Size | `window_size` | `[width, height]` pixels |

## Configuration Reference

Default settings are in `drp_template/default_params/default_figure_settings.json`:

```json
{
  "volume_rendering": {
    "view_shift_x": 0.075,
    "view_shift_y": -0.055,
    "camera_zoom": 0.85,
    "window_size": [2400, 1800],
    "lighting": "custom",
    "opacity_slice": 1.0
  }
}
```

## Tips & Tricks

1) Window-size independent rendering

```python
volume_rendering(data, window_size=[800, 600])
volume_rendering(data, window_size=[3200, 2400])
```

2) Transparent slices in combined mode

```python
volume_rendering(data, mode='combined', slice_opacity=0.2, phase_opacity={0: 0.8})
```

3) Structure analysis with edges

```python
volume_rendering(data, mode='3d', show_3d_edges=True, edge_color='white', dark_mode=True)
```

4) Custom color schemes

```python
volume_rendering(data, mode='3d', phase_colors={0: (1.0, 0.0, 0.0), 1: (0.0, 0.5, 1.0)})
```

5) Professional lighting

```python
volume_rendering(data, lighting='dramatic')
volume_rendering(data, lighting='soft')
```

## Common Workflows

Pore Network Visualization

```python
image.volume_rendering(
    data,
    mode='3d',
    phase_opacity={0: 0.8, 1: 0.2},
    lighting='dramatic',
    labels={0: 'Pore Network', 1: 'Rock Matrix'}
)
```

Multi-Scale Analysis

```python
image.volume_rendering(
    data,
    mode='combined',
    slice_indices=[40, 40, 40],
    slice_opacity=0.25,
    phase_opacity={0: 0.7},
    show_3d_edges=True
)
```

Publication Figure

```python
image.volume_rendering(
    data,
    mode='combined',
    window_size=[3200, 2400],
    slice_opacity=0.15,
    phase_opacity={0: 0.85},
    show_3d_edges=True,
    edge_color='yellow',
    lighting='bright'
)
```

Animation for Presentation

```python
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

- Python 3.8+
- PyVista >= 0.43.0
- trame >= 3.4 (for interactive notebooks)
- cmcrameri (for scientific colormaps)

## Support

For issues or questions:
1. Review this guide for detailed documentation
2. Explore the example notebooks
3. Check function docstrings: `help(image.volume_rendering)`

---

Last Updated: November 7, 2025
