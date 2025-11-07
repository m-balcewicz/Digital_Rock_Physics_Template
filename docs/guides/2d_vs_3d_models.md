# Binary Model Creation: 2D vs 3D Guide

## Overview

The `drp_template` package now provides explicit functions for binary model creation (generic `create_binary_model` removed):

1. **`create_binary_model_2d()`** - Dedicated 2D function (creates nx × ny × 1 volume)
2. **`create_binary_model_3d()`** - Dedicated 3D function

## Architecture & Maintainability

### Design Principles

**Single Responsibility**: Each function has a clear, focused purpose
- `create_binary_model_2d()` handles all 2D logic
- `create_binary_model_3d()` handles all 3D logic (wraps original)
- Helper functions (`_make_ellipse_mask_2d`, `_make_ellipsoid_mask`) are private

**Easy to Maintain**:
- 2D and 3D logic are separated
- Changes to 2D don't affect 3D and vice versa
- Original `create_binary_model()` preserved for backward compatibility

**Clear Intent**:
```python
# Explicit and clear what you're creating
data_2d = create_binary_model_2d(200, 200, ...)
data_3d = create_binary_model_3d(150, 150, 150, ...)
```

## Quick Reference

### When to Use Which Function

| Scenario | Function | Why |
|----------|----------|-----|
| 2D microstructure | `create_binary_model_2d()` | Clearer intent, enforces 2D |
| 3D pore network | `create_binary_model_3d()` | Clearer intent, full 3D control |
| Legacy code | `create_binary_model()` | Backward compatible |
| Not sure | `create_binary_model_3d()` | More general, can do everything |

### Function Comparison

#### `create_binary_model_2d(nx, ny, ...)`

**Purpose**: Create 2D binary models (thin sections, single slices)

**Output Shape**: `(nx, ny, 1)` - third dimension always 1

**Inclusions**: Ellipses/circles in XY plane

**Positions Format**: `(N, 2)` array `[[x, y], ...]`

**Rotation**: In-plane only (around Z-axis)

**Parameters**:
- No `nz` parameter (always 1)
- No `orientation` parameter (always XY)
- `random_orientation` rotates in 2D plane

**Example**:
```python
data_2d = create_binary_model_2d(
    nx=200, ny=200,
    num_inclusions=15,
    inclusion_radius=12,
    inclusion_aspect_ratio=1.5,  # Ellipses
    random_orientation=True,      # 2D rotation only
    seed=42
)
# Shape: (200, 200, 1)
```

#### `create_binary_model_3d(nx, ny, nz, ...)`

**Purpose**: Create 3D binary models (full volumes)

**Output Shape**: `(nx, ny, nz)` - true 3D volume

**Inclusions**: Ellipsoids/spheres in 3D space

**Positions Format**: `(N, 3)` array `[[x, y, z], ...]`

**Rotation**: Full 3D rotation with Euler angles

**Parameters**:
- Requires `nx, ny, nz` dimensions
- `orientation` parameter ('xy', 'zx', 'zy')
- `random_orientation` uses true 3D rotation

**Example**:
```python
data_3d = create_binary_model_3d(
    nx=150, ny=150, nz=150,
    num_inclusions=20,
    inclusion_radius=12,
    inclusion_aspect_ratio=1.5,  # Ellipsoids
    orientation='xy',             # Elongated in Z
    random_orientation=True,      # Full 3D rotation!
    seed=42
)
# Shape: (150, 150, 150)
```

## Use Cases

### 2D Models (`create_binary_model_2d`)

**Best for**:
- Thin section analysis
- 2D image segmentation validation
- Fast parameter studies (computationally cheaper)
- Teaching/demonstrations
- Image-based microstructure modeling

**Advantages**:
- ✓ Faster to compute
- ✓ Easier to visualize (single image)
- ✓ Less memory usage
- ✓ Matches 2D imaging workflows

**Limitations**:
- ✗ No 3D connectivity analysis
- ✗ No permeability calculation
- ✗ Limited to planar structures

### 3D Models (`create_binary_model_3d`)

**Best for**:
- Digital rock physics simulations
- Permeability/connectivity analysis
- 3D pore network modeling
- Realistic geological structures
- Multi-phase flow simulations

**Advantages**:
- ✓ True 3D spatial relationships
- ✓ Realistic pore connectivity
- ✓ Full orientation control (Euler angles)
- ✓ Representative of real rocks

**Limitations**:
- ✗ More computationally expensive
- ✗ Larger memory footprint
- ✗ More complex visualization

## Technical Details

### Aspect Ratio Behavior

**2D (`create_binary_model_2d`)**:
- `aspect_ratio = 1.0` → Circle
- `aspect_ratio < 1.0` → Vertically flattened ellipse
- `aspect_ratio > 1.0` → Vertically elongated ellipse

**3D (`create_binary_model_3d`)** with `orientation='xy'`:
- `aspect_ratio = 1.0` → Sphere
- `aspect_ratio < 1.0` → Oblate ellipsoid (disk-like, flat in Z)
- `aspect_ratio > 1.0` → Prolate ellipsoid (cigar-like, long in Z)

### Random Orientation

**2D**: Rotates ellipse in XY plane (single angle, 0-2π)
```python
# Simple 2D rotation matrix
angle = random(0, 2π)
R = [[cos(θ), -sin(θ)],
     [sin(θ),  cos(θ)]]
```

**3D**: Full 3D rotation using Euler angles (α, β, γ)
```python
# ZYX Euler angle composition
R = Rz(α) @ Ry(β) @ Rx(γ)
# Each ellipsoid can point in any direction!
```

### Position Specification

**2D**:
```python
positions = np.array([
    [100, 50],    # x, y
    [150, 100],
    [75, 150]
])
data_2d = create_binary_model_2d(200, 200, positions=positions, num_inclusions=3)
```

**3D**:
```python
positions = np.array([
    [100, 50, 75],     # x, y, z
    [150, 100, 100],
    [75, 150, 125]
])
data_3d = create_binary_model_3d(200, 200, 200, positions=positions, num_inclusions=3)
```

## Migration Guide

### From `create_binary_model()` to Specialized Functions

**Old code** (ambiguous):
```python
# Is this 2D or 3D? Not clear!
data = create_binary_model(200, 200, 1, num_inclusions=10)
```

**New code** (explicit):
```python
# Crystal clear: this is 2D
data_2d = create_binary_model_2d(200, 200, num_inclusions=10)

# Or for 3D:
data_3d = create_binary_model_3d(200, 200, 200, num_inclusions=10)
```

### Removal of Generic Function

The previous generic `create_binary_model()` has been removed. Use explicit 2D or 3D creation for clarity.

## Code Examples

### Example 1: 2D Thin Section

```python
from drp_template.model import create_binary_model_2d
from drp_template.input_output import export_model
import matplotlib.pyplot as plt

# Create 2D model
data_2d = create_binary_model_2d(
    nx=300, ny=300,
    num_inclusions=25,
    inclusion_radius=15,
    inclusion_aspect_ratio=1.2,
    random_orientation=True,
    background_value=1,
    inclusion_value=0,
    seed=42
)

# Visualize
plt.imshow(data_2d[:, :, 0].T, cmap='gray')
plt.title('2D Thin Section Model')
plt.show()

# Export
export_model('thin_section_2d', data_2d, voxel_size=1.0, labels={0: 'Pore', 1: 'Solid'})
```

### Example 2: 3D Pore Network

```python
from drp_template.model import create_binary_model_3d
from drp_template.image import ortho_views

# Create 3D model with randomly oriented prolate ellipsoids
data_3d = create_binary_model_3d(
    nx=150, ny=150, nz=150,
    num_inclusions=30,
    inclusion_radius=12,
    inclusion_aspect_ratio=2.0,  # Very elongated
    random_orientation=True,      # True 3D random!
    background_value=1,
    inclusion_value=0,
    seed=123
)

# Visualize all three views
fig, axes = ortho_views(data_3d, labels={0: 'Pore', 1: 'Rock Matrix'})
plt.show()

# Export
export_model('pore_network_3d', data_3d, voxel_size=5.0)
```

### Example 3: Explicit Positioning

```python
import numpy as np

# 2D: Create grid of circles
positions_2d = []
for i in range(5):
    for j in range(5):
        positions_2d.append([40 + i*40, 40 + j*40])
positions_2d = np.array(positions_2d)

data_2d = create_binary_model_2d(
    nx=250, ny=250,
    num_inclusions=25,
    inclusion_radius=15,
    positions=positions_2d
)

# 3D: Create cubic lattice of spheres
positions_3d = []
for i in range(4):
    for j in range(4):
        for k in range(4):
            positions_3d.append([30 + i*30, 30 + j*30, 30 + k*30])
positions_3d = np.array(positions_3d)

data_3d = create_binary_model_3d(
    nx=150, ny=150, nz=150,
    num_inclusions=64,
    inclusion_radius=10,
    positions=positions_3d
)
```

## Best Practices

### 1. Use Explicit Functions

✅ **DO THIS**:
```python
data_2d = create_binary_model_2d(200, 200, num_inclusions=10)
data_3d = create_binary_model_3d(200, 200, 200, num_inclusions=10)
```

❌ **AVOID THIS** (legacy pattern removed):
```python
# data = create_binary_model(200, 200, 1, num_inclusions=10)
```

### 2. Choose Right Dimensions

For 2D models, match your image/sample dimensions:
```python
# 2000×2000 pixel thin section image, 1 μm/pixel
data_2d = create_binary_model_2d(2000, 2000, inclusion_radius=50)
```

For 3D models, consider computational resources:
```python
# 500³ voxels = 125M voxels (manageable)
data_3d = create_binary_model_3d(500, 500, 500, inclusion_radius=25)

# 1000³ voxels = 1B voxels (requires significant RAM!)
```

### 3. Use Random Orientation Wisely

For **2D models**: Random orientation adds variety but limited effect
```python
# 2D rotation mostly affects visualization
data_2d = create_binary_model_2d(..., random_orientation=True)
```

For **3D models**: Random orientation critical for realistic structures
```python
# 3D rotation essential for realistic pore networks
data_3d = create_binary_model_3d(..., random_orientation=True)
```

### 4. Set Appropriate Seeds

For reproducible research:
```python
# Same seed = same model
data1 = create_binary_model_3d(..., seed=42)
data2 = create_binary_model_3d(..., seed=42)
assert np.array_equal(data1, data2)  # True!
```

## Performance Considerations

### Memory Usage

- **2D (200×200×1)**: ~40 KB (uint8)
- **3D (200×200×200)**: ~8 MB (uint8)
- **3D (500×500×500)**: ~125 MB (uint8)

### Computation Time (approximate, single inclusion)

- **2D**: ~1-2 ms
- **3D (no rotation)**: ~10-20 ms
- **3D (with rotation)**: ~50-100 ms

### Recommendations

For parameter studies with many iterations:
- Use 2D when possible (much faster)
- Use smaller 3D volumes (100³ vs 500³)
- Limit `num_inclusions` in 3D models

## Troubleshooting

### Issue: 2D model appears 3D

**Problem**: Using `create_binary_model()` with nz=1
```python
data = create_binary_model(200, 200, 1, ...)  # Creates 3D array
```

**Solution**: Use dedicated 2D function
```python
data_2d = create_binary_model_2d(200, 200, ...)  # Clearer intent
```

### Issue: 3D random orientation not working

**Problem**: Ellipsoids all aligned the same way

**Solution**: Ensure `random_orientation=True` and check seed
```python
data_3d = create_binary_model_3d(
    ...,
    random_orientation=True,  # Must be True!
    seed=None  # Different result each time
)
```

### Issue: Positions validation error

**Problem**: Wrong position array shape for 2D vs 3D

**Solution**: Match dimensions
```python
# 2D: (N, 2)
positions_2d = np.array([[50, 50], [100, 100]])  # Only x, y
data_2d = create_binary_model_2d(..., positions=positions_2d)

# 3D: (N, 3)
positions_3d = np.array([[50, 50, 50], [100, 100, 100]])  # x, y, z
data_3d = create_binary_model_3d(..., positions=positions_3d)
```

## Periodic Boundary Conditions

### Overview

Both 2D and 3D functions support **periodic boundary conditions (PBC)** via the `periodic` parameter. When enabled, inclusions that extend beyond domain boundaries are automatically wrapped to the opposite side, creating seamless, tileable volumes.

### Applications

- **Representative Volume Elements (RVE)** for computational homogenization
- **Periodic unit cells** for material property calculations
- **Seamless texture generation** without edge artifacts
- **Finite element simulations** requiring periodic BCs

### How It Works

**Without PBC** (`periodic=False`, default):
- Inclusions are cut off at boundaries
- Non-tileable volumes
- Edge effects in statistics

**With PBC** (`periodic=True`):
- Inclusions wrap to opposite boundaries
- Seamlessly tileable in all directions
- No edge effects

### Implementation Details

**2D Periodic Boundaries**:
- Checks 4 edges: left, right, top, bottom
- Checks 4 corners: diagonal wrapping
- Up to **9 copies** per inclusion (1 original + 8 periodic images)

**3D Periodic Boundaries**:
- Checks 6 faces: ±X, ±Y, ±Z
- Checks 12 edges: combinations of 2 faces
- Checks 8 corners: combinations of 3 faces
- Up to **27 copies** per inclusion (1 original + 26 periodic images)

### Usage Examples

#### 2D Periodic RVE

```python
from drp_template.model import create_binary_model_2d

# Create 2D RVE with periodic boundaries
data_rve_2d = create_binary_model_2d(
    nx=200, ny=200,
    num_inclusions=15,
    inclusion_radius=25,
    inclusion_aspect_ratio=1.5,
    random_orientation=True,
    periodic=True,  # Enable periodic boundaries
    seed=42
)

# Verify seamless tiling
import numpy as np
tiled = np.block([
    [data_rve_2d[:, :, 0], data_rve_2d[:, :, 0]],
    [data_rve_2d[:, :, 0], data_rve_2d[:, :, 0]]
])
# No visible seams at tile boundaries!
```

#### 3D Periodic RVE

```python
from drp_template.model import create_binary_model_3d

# Create 3D RVE with periodic boundaries
data_rve_3d = create_binary_model_3d(
    nx=100, ny=100, nz=100,
    num_inclusions=10,
    inclusion_radius=18,
    inclusion_aspect_ratio=1.2,
    random_orientation=True,
    periodic=True,  # Enable periodic boundaries
    seed=123
)

# This volume can be seamlessly tiled in all three dimensions
```

#### Demonstrating the Effect

```python
# Compare: Without vs With PBC
import matplotlib.pyplot as plt

# Near-boundary inclusion
position = np.array([[10, 10]])

# Without PBC
data_no_pbc = create_binary_model_2d(
    100, 100,
    num_inclusions=1,
    inclusion_radius=30,
    positions=position,
    periodic=False
)

# With PBC
data_pbc = create_binary_model_2d(
    100, 100,
    num_inclusions=1,
    inclusion_radius=30,
    positions=position,
    periodic=True
)

# Visualize
fig, axes = plt.subplots(1, 2, figsize=(12, 5))
axes[0].imshow(data_no_pbc[:, :, 0].T, cmap='gray')
axes[0].set_title('Without PBC (cut off)')
axes[1].imshow(data_pbc[:, :, 0].T, cmap='gray')
axes[1].set_title('With PBC (wrapped)')
plt.show()
```

### When to Use Periodic Boundaries

✅ **Use `periodic=True` when:**
- Creating RVEs for homogenization
- Generating periodic unit cells
- Need seamless tiling
- Avoiding boundary artifacts in analysis
- Simulating infinite/repeating structures

❌ **Don't use `periodic=True` when:**
- Modeling finite domains (real rock samples)
- Boundary conditions matter for your application
- Inclusions should be cut off at edges
- Not concerned with tiling

### Performance Note

Enabling periodic boundaries may create up to 9 (2D) or 27 (3D) copies of inclusions near boundaries. For most applications, this has minimal performance impact, but be aware when creating many inclusions in small volumes.

## Summary

| Feature | 2D | 3D |
|---------|-----|-----|
| **Function** | `create_binary_model_2d()` | `create_binary_model_3d()` |
| **Output Shape** | (nx, ny, 1) | (nx, ny, nz) |
| **Inclusions** | Ellipses | Ellipsoids |
| **Position Format** | (N, 2) | (N, 3) |
| **Rotation** | Single angle | Euler angles (α, β, γ) |
| **Periodic BC** | Up to 9 copies | Up to 27 copies |
| **Speed** | Fast | Moderate |
| **Memory** | Low | Higher |
| **Best For** | Thin sections, images | Rock physics, 3D networks |

**Recommendation**: Always use the explicit function (`_2d` or `_3d`) that matches your intent for clearer, more maintainable code.

### New Features (v0.1.0+)

- ✅ **Dedicated 2D function** (`create_binary_model_2d`)
- ✅ **True 3D rotation** with Euler angles (α, β, γ)
- ✅ **Periodic boundary conditions** for RVE applications
- ✅ **Improved architecture** with single responsibility principle
- ✅ **Backward compatibility** maintained
