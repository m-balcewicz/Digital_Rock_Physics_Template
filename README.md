# Digital Rock Physics Template (0.1.0b1 Beta)

> A modular Python toolkit for generating, importing, analyzing, and visualizing digital rock volumes using explicit, testable APIs and SI-consistent metadata.

## ✨ Key Concepts

Digital rock physics combines computational geometry, image analysis, and effective medium / rock physics models to estimate physical properties (e.g. elastic moduli, attenuation, porosity) from voxel-scale representations. This template provides:

* Synthetic model generation (ellipses / ellipsoids with Euler rotations, optional periodic boundaries)
* Data validation, labeling, statistics & metadata extraction
* Geometry / physics helpers (CT geometry, wavelength utilities, unit conversions)
* Export + visualization pipeline (raw, VTK ImageData, ParaView launcher)
* Modular namespace for clarity & maintainability

> This project is independent; references to published works (e.g. Rock Physics Handbook) are contextual only.

---

## 🧱 Package Structure

| Namespace | Role | Examples |
|-----------|------|----------|
| `drp_template.model` | Synthetic binary models | `binary_2d`, `binary_3d` |
| `drp_template.image` | Visualization & figure helpers | `ortho_slice`, `ortho_views`, `histogram`, `volume_rendering`, `create_rotation_animation` |
| `drp_template.tools.validation` | Validation & statistics | `check_binary`, `classify_data_type`, `get_value_statistics` |
| `drp_template.tools.labeling` | Label operations | `label_binary`, `reorder_labels` |
| `drp_template.tools.file_utils` | File & metadata utilities | `get_model_properties`, `infer_dtype_from_filesize` |
| `drp_template.io.writers` | Export functions | `export_model`, `export_vti` |
| `drp_template.io.utils` | IO helpers | `open_in_paraview`, `reorient_volume`, `resolve_params_filename` |
| `drp_template.compute` | Physics / math | `ct_geometry`, wavelength funcs, `m2mm`, `mm2m`, `m2um`, `um2m` |

All arrays use order (x, y, z) with `x` fastest and VTK export requires pre-normalized xyz.

---

## 🚀 Quick Start

Install core package:
```bash
pip install drp_template==0.1.0b1
```

Add visualization extras:
```bash
pip install drp_template[viz]
```

Add VTK export support:
```bash
pip install drp_template[vtk]
```

Combine:
```bash
pip install drp_template[viz,vtk]
```

Generate a 3D model and export to VTI:
```python
from drp_template.model import binary_3d
from drp_template.io import export_vti

data = binary_3d(150, 150, 150, num_inclusions=25, random_orientation=True, periodic=True)
export_vti(data, path="output/model.vti", spacing=(1e-3, 1e-3, 1e-3))
```

Launch ParaView (if installed):
```python
from drp_template.io import open_in_paraview
open_in_paraview("output/model.vti")
```

---

## 🧪 Synthetic Binary Models

```python
from drp_template.model import binary_2d, binary_3d

img2d = binary_2d(200, 200, num_inclusions=15, inclusion_radius=20, periodic=True, seed=42)
vol3d = binary_3d(100, 120, 140, num_inclusions=18, inclusion_radius=12, inclusion_aspect_ratio=1.6, random_orientation=True)
```

Features:
* Explicit dimensional APIs (`binary_2d`, `binary_3d`)
* Elliptical / ellipsoidal inclusions with aspect ratio & Euler angle rotation
* Optional periodic boundary copies (tiling-friendly RVEs)
* Deterministic seeding for reproducibility

---

## 📊 Validation & Metadata

```python
from drp_template.tools.validation import check_binary, get_value_statistics
from drp_template.tools.file_utils import get_model_properties

assert check_binary(vol3d)
stats = get_value_statistics(vol3d)
props = get_model_properties("output/")  # after export_model
```

Provides quick sanity checks, basic descriptive statistics, and structured metadata (dimensions, dtype, spacing if present, label counts, porosity estimates when applicable).

---

## 🖼️ Visualization Helpers

```python
from drp_template.image import ortho_views, histogram, volume_rendering

fig, axes = ortho_views(vol3d)          # axial/coronal/sagittal slices
hist_fig = histogram(vol3d)             # value distribution
vr_fig = volume_rendering(vol3d)        # rudimentary volume render
```

Animations:
```python
from drp_template.image import create_rotation_animation
create_rotation_animation(vol3d, output_path="output/turntable.gif", n_frames=36)
```

---

## 📦 Export Pipeline

Raw model + params JSON:
```python
from drp_template.io import export_model
export_model(vol3d, folder="output", paramsfile="my_model")
```

VTK ImageData (`.vti`) + metadata sidecar:
```python
from drp_template.io import export_vti
export_vti(vol3d, path="output/model.vti", spacing=(0.0005, 0.0005, 0.0005))
```

ParaView integration (auto-detect executable):
```python
from drp_template.io import open_in_paraview
open_in_paraview("output/model.vti")
```

All export metadata adheres to SI units (meters) for spacing and origin.

---

## 🔬 Physics & Geometry Utilities

```python
from drp_template.compute import ct_geometry, m2mm, mm2m

geom = ct_geometry(n_voxels=(512, 512, 256), voxel_size_m=(4e-6, 4e-6, 4e-6))
millimeters = m2mm(0.012)
```

These helpers encourage consistent units and reduce ad hoc conversions.

---

## 🧪 Testing & Examples

Reference + tutorial notebooks (ongoing restructuring) reside under `examples/<module>/reference` & `examples/<module>/tutorials`. Run minimal validation scripts or adapt examples for custom workflows.

Editable install for development:
```bash
pip install -e .
```

Run a quick smoke check (example):
```python
python tests/test_io_export_model.py  # or adapt to pytest if reintroduced
```

---

## 🛠️ Contributing

1. Fork & branch (`feature/<short-description>`).
2. Add / update focused tests (small arrays, deterministic seeds).
3. Maintain xyz array order before VTK export.
4. Document new public functions (docstring + example snippet).
5. Submit PR referencing issue / enhancement motivation.

Style & Principles:
* Small, composable functions over large multi-purpose scripts.
* SI units for physical quantities.
* Deterministic randomness via `seed` where applicable.

---

## ⚠️ Deprecations & Roadmap

Pending removal (future minor release): legacy `_funcs` stubs and transitional `io.vtk` shim. Please migrate imports now.

Upcoming focus:
* Expanded unit test matrix (validation, labeling, IO readers)
* Performance profiling for large VTI exports
* Consolidated examples & richer gallery

---

## 📄 License

See `LICENSE`. Third-party references are provided for educational context only.

---

## ❓ FAQ

**Why enforce xyz array order?**  Transparency: avoids silent permutation and ambiguity in spatial axes.

**Why SI units internally?**  Enables consistent physics calculations and interoperable metadata.

**Can I disable periodic boundaries?**  Yes—set `periodic=False` to represent finite samples.

**What if ParaView isn't installed?**  `open_in_paraview` fails gracefully; you can still load `.vti` manually.

---

## 📬 Contact / Support

Open an issue for bugs, enhancement proposals, or clarification requests. Include:
* Environment (OS, Python version)
* Repro snippet (minimal code)
* Expected vs actual behavior

---

**Version**: 0.1.0b1  
**Status**: Beta (API stabilization phase)
