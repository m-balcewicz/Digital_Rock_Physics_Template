# Release Notes – 0.1.0b1 Beta (2025-11-07)

This beta release consolidates a broad architectural refactor plus the new binary model API introduced earlier. The focus is on a cleaner package structure, explicit public functions, SI unit consistency, and streamlined export/visualization tooling.

---

## 🧱 Package Structure (New Modular Layout)

The library is now intentionally decomposed into focused subpackages. Each namespace exposes a small, explicit set of functions.

| Package | Purpose | Key Public Functions / Objects |
|---------|---------|--------------------------------|
| `drp_template.model` | Synthetic binary model generation | `binary_2d`, `binary_3d` |
| `drp_template.image` | Visualization helpers (orthos, histograms, rendering, animation) | `ortho_slice`, `ortho_views`, `histogram`, `volume_rendering`, `create_rotation_animation` |
| `drp_template.tools.validation` | Data validation & statistics | `check_binary`, `classify_data_type`, `get_value_statistics` |
| `drp_template.tools.labeling` | Connected component labeling & relabeling | `label_binary`, `reorder_labels` |
| `drp_template.tools.file_utils` | Model metadata & file helpers | `get_model_properties`, `infer_dtype_from_filesize` |
| `drp_template.io.writers` | Export functions (raw, VTK) | `export_model`, `export_vti` |
| `drp_template.io.utils` | IO utilities | `open_in_paraview`, `reorient_volume`, `resolve_params_filename` |
| `drp_template.compute` | Rock physics / math utilities | `ct_geometry`, wavelength-related functions, length conversions (`m2mm`, etc.) |

### Why This Matters
* Explicit boundaries: Easier discovery, less hidden coupling.
* Future stability: Clear migration path; deprecated legacy monoliths now isolated.
* Testability: Fine-grained units facilitate targeted tests.

---

## 🧪 Binary Model API (Recap & Integration)

The earlier alpha update introduced the simplified, explicit binary model API. In beta, that API is fully integrated with the new structure and documentation paths.

```python
from drp_template.model import binary_2d, binary_3d

data2d = binary_2d(200, 200, num_inclusions=12, periodic=True)
data3d = binary_3d(150, 150, 150, num_inclusions=20, random_orientation=True)
```

Highlights:
* Short names (`binary_2d`, `binary_3d`) replace verbose legacy names.
* True 3D Euler rotations for inclusions (`random_orientation=True`).
* Periodic boundary generation (2D: up to 9 copies; 3D: up to 27).
* Fixed ellipsoid axis aspect-ratio mapping (geometry correctness guaranteed).

---

## 🌍 SI Unit Standardization

All geometry-related functions (e.g. `ct_geometry`) use SI units (meters) internally. Helper conversions shipped in `compute`:

```python
from drp_template.compute import m2mm, mm2m, m2um, um2m
```

Benefits: Consistent downstream physics, unambiguous metadata, simplified multi-tool integration.

---

## 📤 Export & Visualization Tooling

### Unified VTK Export
`export_vti` (in `io.writers`) writes VTK ImageData (`.vti`) plus a JSON sidecar with SI metadata:

```python
from drp_template.io import export_vti
export_vti(array_xyz, path="output/model.vti", spacing=(0.001, 0.001, 0.001))
```

Rules:
* Enforces array order = xyz (no silent permutation) for clarity.
* Sidecar JSON: spacing, origin, dtype, shape.

### ParaView Launcher
`open_in_paraview("output/model.vti")` attempts OS-aware executable discovery, opening the exported file directly if ParaView is installed.

### Deprecation Shim
Former `io.vtk` heavy implementation now a lightweight shim re-exporting `export_vti` and `open_in_paraview` with a `DeprecationWarning`.

---

## 🧩 Deprecated Legacy Modules

Monolithic `_funcs` modules in `image` and `tools` are replaced by stubs guiding users to new submodules. They remain temporarily for backward compatibility and will be removed in a future minor release.

Migration is intentionally frictionless: import paths simply change; function semantics preserved or improved.

---

## 🧪 Testing & Scripts
* `test_io_export_model.py` validates raw export + metadata.
* Standalone VTI export script demonstrates `export_vti` with a synthetic sphere volume.
* Additional granular tests (image slicing, labeling, stats, IO readers) planned for the next iteration.

---

## 📚 Documentation & Generation
* Docs generator relocated to `docs/scripts/generate_docs.py`.
* Examples reorganized (ongoing) under `examples/<module>/reference` & `examples/<module>/tutorials`.
* Release notes emphasize discoverability and explicit API boundaries.

---

## ➕ Optional Dependencies (Extras)

Install minimal core:
```bash
pip install drp_template==0.1.0b1
```

Add visualization stack:
```bash
pip install drp_template[viz]
```

Add VTK export support:
```bash
pip install drp_template[vtk]
```

Combination:
```bash
pip install drp_template[viz,vtk]
```

---

## 🔧 Migration Guide (Beta Focus)

| Legacy | Replacement | Notes |
|--------|-------------|-------|
| `tools.create_binary_model_2d` | `model.binary_2d` | Shorter & explicit dimensionality |
| `tools.create_binary_model_3d` | `model.binary_3d` | Full Euler rotations |
| `image._funcs.histogram` | `image.histogram` | Same behavior, moved |
| `tools._funcs.get_model_properties` | `tools.file_utils.get_model_properties` | Extended metadata |
| `io.vtk.export_vti` (old) | `io.writers.export_vti` | xyz-only enforcement |

Action Items for Users:
1. Update imports to new package paths.
2. Remove reliance on implicit array reordering (prepare xyz layout upstream).
3. Adopt SI spacing/origin when exporting or computing geometry.

---

## 🗺️ Roadmap (Post-Beta)
* Remove deprecated stubs (`_funcs`, shim in `io.vtk`).
* Expand test coverage (image, labeling, IO readers).
* Notebook consolidation under examples structure.
* Performance profiling for large model generation and VTI export.

---

## ✅ Summary
The 0.1.0b1 beta crystallizes a modular architecture, explicit binary model APIs, SI unit normalization, and transparent export tooling. It sets a stable foundation for adding physics features and expanding test coverage without future large-scale breaking reorganizations.

---

# Historical Note – Binary Model Creation Update (2025-01-05)

The earlier alpha introduced the streamlined binary model API. Core details retained below for completeness.

## 🚀 Quick Start

**New Clean API**:
```python
from drp_template.model import binary_2d, binary_3d

# Create 2D model
data_2d = binary_2d(200, 200, num_inclusions=10, periodic=True)

# Create 3D model  
data_3d = binary_3d(100, 100, 100, num_inclusions=15, random_orientation=True)
```

**What Changed**:
- ✅ **Shorter names**: `binary_2d()` and `binary_3d()` (60% shorter!)
- ✅ **New location**: `drp_template.model` (dedicated package)
- ⚠️ **Breaking**: Old verbose names removed

---

## 🎉 Major Features

### 1. New Simplified API with Dedicated 2D and 3D Functions

**Clean, Concise Function Names**:
- `binary_2d(nx, ny, ...)` - Create 2D binary models
- `binary_3d(nx, ny, nz, ...)` - Create 3D binary models

**New Location**:
```python
from drp_template.model import binary_2d, binary_3d
```

**Benefits**:
- ✅ Shorter, cleaner names
- ✅ Clear intent (explicit 2D vs 3D)
- ✅ Works beautifully with module prefix: `model.binary_2d()`
- ✅ Better maintainability (Single Responsibility Principle)
- ⚠️ **Breaking Change**: Generic `create_binary_model()` removed

### 2. Periodic Boundary Conditions 🔄

**New `periodic` parameter** for both 2D and 3D functions:

```python
# 2D with periodic boundaries
data_2d = binary_2d(
    200, 200,
    num_inclusions=15,
    periodic=True  # ← NEW!
)

# 3D with periodic boundaries
data_3d = binary_3d(
    100, 100, 100,
    num_inclusions=10,
    periodic=True  # ← NEW!
)
```

**How it works**:
- Inclusions near boundaries wrap to opposite side
- Creates seamless, tileable volumes
- Perfect for Representative Volume Elements (RVE)

**Implementation**:
- **2D**: Up to 9 periodic copies (1 original + 4 edges + 4 corners)
- **3D**: Up to 27 periodic copies (1 original + 6 faces + 12 edges + 8 corners)

### 3. True 3D Rotation with Euler Angles

**Fixed and Enhanced**:
- ✅ **Before**: Only 2D in-plane rotation
- ✅ **Now**: Full 3D rotation using Euler angles (α, β, γ)
- ✅ Rotation matrix: `R = Rz(α) @ Ry(β) @ Rx(γ)`

```python
data = binary_3d(
    100, 100, 100,
    num_inclusions=10,
    random_orientation=True  # Now produces TRUE 3D rotation!
)
```

**Result**: Ellipsoids now orient along all three axes (X, Y, Z)

## 🐛 Critical Bug Fixes

### Ellipsoid Geometry Fix

**Problem**: Aspect ratio was applied to wrong axis

**Before** (INCORRECT):
- `orientation='xy'`: Aspect applied to Y-axis ❌
- `orientation='zx'`: Aspect applied to X-axis ❌  
- `orientation='zy'`: Aspect applied to Y-axis ❌

**Now** (CORRECT):
- `orientation='xy'`: Aspect applied to Z-axis ✅ (perpendicular to XY plane)
- `orientation='zx'`: Aspect applied to Y-axis ✅ (perpendicular to ZX plane)
- `orientation='zy'`: Aspect applied to X-axis ✅ (perpendicular to ZY plane)

This was a **fundamental geometry error** affecting all ellipsoidal inclusions!

## 📚 Documentation Updates

### New Guides
 `binary_2d(nx, ny, ...)` - Dedicated 2D function (formerly `create_binary_model_2d`)
 `binary_3d(nx, ny, nz, ...)` - Dedicated 3D function (formerly `create_binary_model_3d`)
  - Periodic boundaries explained
 `binary_3d(nx, ny, nz, ...)`
 **Example: 2D Model with PBC**
 ```python
 from drp_template.model import binary_2d
 # Create 2D RVE
 data_rve = binary_2d(
     nx=200, ny=200,
     num_inclusions=15,
     inclusion_radius=12,
     periodic=True,
     seed=42
 )
  - Added Example 5: Periodic Boundary Conditions
 `binary_3d(nx, ny, nz, ...)`
 ```python
 from drp_template.model import binary_3d
 # Create 3D model with random orientations
 data_3d = binary_3d(
     nx=100, ny=100, nz=100,
     num_inclusions=10,
     inclusion_radius=15,
     inclusion_aspect_ratio=1.5,
     random_orientation=True,
     seed=123
 )
    - `binary_2d()` function
    - `binary_3d()` function  
 ✅ Explicit 2D/3D APIs (`binary_2d`, `binary_3d`)
 The previous generic `create_binary_model()` has been removed to enforce explicit 2D vs 3D intent. Use:
 ```python
 from drp_template.model import binary_2d, binary_3d
 # 2D
 data2d = binary_2d(...)
 # 3D
 data3d = binary_3d(...)
 ```
|---------|-----|-----|
| **Function** | `binary_2d()` | `binary_3d()` |
| **Output Shape** | (nx, ny, 1) | (nx, ny, nz) |
| **Inclusions** | Ellipses | Ellipsoids |
| **Position Format** | (N, 2) | (N, 3) |
| **Rotation** | Single angle | Euler angles (α, β, γ) |
| **Periodic BC** | Up to 9 copies | Up to 27 copies |
| **Speed** | ⚡ Fast | Moderate |
| **Best For** | Thin sections, images | Rock physics, 3D volumes |

## 🚀 Usage Examples

### Example 1: 2D RVE with Periodic Boundaries

```python
from drp_template.model import binary_2d
import numpy as np

# Create 2D RVE
data_rve = binary_2d(
    nx=200, ny=200,
    num_inclusions=15,
    inclusion_radius=25,
    inclusion_aspect_ratio=1.5,
    random_orientation=True,
    periodic=True,  # Seamless tiling
    seed=42
)

# Verify seamless tiling
tiled = np.block([
    [data_rve[:, :, 0], data_rve[:, :, 0]],
    [data_rve[:, :, 0], data_rve[:, :, 0]]
])
# No visible seams! ✅
```

### Example 2: 3D Model with Full 3D Rotation

```python
from drp_template.model import binary_3d

# Create 3D model with random orientations
data_3d = binary_3d(

### Example 3: Demonstrating PBC Effect

```python
import matplotlib.pyplot as plt

# Without periodic boundaries
data_no_pbc = binary_2d(
    100, 100,
    num_inclusions=1,
    inclusion_radius=30,
    positions=np.array([[10, 10]]),  # Near corner
    periodic=False
)

# With periodic boundaries
data_pbc = binary_2d(
    100, 100,
    num_inclusions=1,
    inclusion_radius=30,
    positions=np.array([[10, 10]]),
    periodic=True
)

# Compare
fig, axes = plt.subplots(1, 2, figsize=(12, 5))
axes[0].imshow(data_no_pbc[:, :, 0].T, cmap='gray')
axes[0].set_title('Without PBC (cut off)')
axes[1].imshow(data_pbc[:, :, 0].T, cmap='gray')
axes[1].set_title('With PBC (wrapped)')
plt.show()
```

## 🔧 Migration Guide

**Breaking Change**: Simplified API

The previous verbose function names have been replaced with cleaner, shorter names:

**Old (removed)**:
```python
from drp_template.tools import create_binary_model_2d, create_binary_model_3d
data = create_binary_model_2d(...)  # Long name
```

**New (use this)**:
```python
from drp_template.model import binary_2d, binary_3d
data = binary_2d(...)  # Clean and concise!
```

**Benefits**:
- ✅ 60% shorter function names
- ✅ Cleaner imports
- ✅ Better with module prefix: `model.binary_3d()`
- ✅ Follows Python conventions

**Note**: Generic `create_binary_model()` completely removed - use explicit `binary_2d()` or `binary_3d()`.

## 📝 Summary of Changes

### Added
- ✅ `binary_2d()` function (clean API)
- ✅ `binary_3d()` function (clean API)
- ✅ New package location: `drp_template.model`
- ✅ `periodic` parameter for PBC
- ✅ True 3D Euler angle rotation
- ✅ Comprehensive documentation and examples
- ✅ Test suite for validation

### Fixed
- ✅ Critical ellipsoid geometry bug
- ✅ 2D-only rotation bug (now true 3D)

### Changed
- ✅ **API Simplification**: Shorter function names (`binary_2d`, `binary_3d`)
- ✅ **New Package**: Functions moved from `drp_template.tools` to `drp_template.model`
- ✅ **Removed**: Generic `create_binary_model()` function (use explicit 2D or 3D)
- ✅ Improved architecture (Single Responsibility Principle)
- ✅ Better maintainability and testability

### Maintained
- ✅ All core functionality preserved
- ✅ Periodic boundary logic
- ✅ True 3D rotation features
- ✅ Comprehensive parameter control

## 🎯 Use Cases

### When to use `periodic=True`:
- ✅ Creating RVEs for computational homogenization
- ✅ Generating periodic unit cells
- ✅ Seamless texture generation
- ✅ Avoiding boundary artifacts in statistics
- ✅ Finite element simulations with periodic BCs

### When to use `periodic=False`:
- ✅ Modeling finite domains (real rock samples)
- ✅ Boundary conditions matter for your application
- ✅ Inclusions should naturally be cut off at edges

---

## 📊 API Evolution Summary

### The Journey to Simplification

```
Version 1.x → Version 2.0
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

OLD (tools):                    NEW (model):
────────────────────────────    ─────────────────────
create_binary_model()           ❌ Removed (ambiguous)
create_binary_model_2d()    →   binary_2d() ✨
create_binary_model_3d()    →   binary_3d() ✨

Character count: 23 chars   →   9 chars (-60%) 🎉
```

### Why This Matters

| Aspect | Before | After | Benefit |
|--------|--------|-------|---------|
| **Import** | `from drp_template.tools` | `from drp_template.model` | Clearer intent |
| **Function** | `create_binary_model_3d()` | `binary_3d()` | 60% shorter |
| **Usage** | `tools.create_binary_model_3d(...)` | `model.binary_3d(...)` | Self-documenting |
| **Ambiguity** | 3 functions (1 generic) | 2 explicit functions | No confusion |

### The Result
```python
# Clean, concise, obvious
from drp_template.model import binary_2d, binary_3d

# 2D model - explicitly named
img_2d = binary_2d(200, 200, porosity=0.3)

# 3D model - explicitly named  
img_3d = binary_3d(100, 100, 100, porosity=0.2)
```

**Simple. Explicit. Pythonic.** ✨

---

## 📖 Further Reading

- [2D vs 3D Models Guide](docs/guides/2d_vs_3d_models.md)
- [API Reference: tools](docs/api/tools.md)
- [Quick Start Guide](docs/quickstart.md)
- [Changelog](docs/changelog.md)

## 🙏 Acknowledgments

These improvements address fundamental issues in the binary model creation system and significantly expand its capabilities for representative volume element (RVE) applications.

---

**Version at time of section**: 0.1.0-alpha  
**Date**: 2025-01-05  
**Status**: Superseded by 0.1.0b1 Beta

---

## Current Beta Version
**Version**: 0.1.0b1  
**Date**: 2025-11-07  
**Status**: Feature-Complete Beta (API stabilization phase)

