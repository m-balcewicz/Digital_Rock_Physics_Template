# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0b1] - 2025-11-11

### Added
- Backus averaging implementation with Thomsen parameters under `drp_template.compute.rockphysics.effective_medium`:
	- `backus_average()`, `thomsen_params()`, and `vti_velocity_vs_angle()` return structured dicts with SI units.
- Rock physics examples refreshed; VTI consistency guidance added for layered voxel models.

### Changed
- Rock physics namespace reorganized into focused subpackages:
	- `mixing/`, `bounds/`, `effective_medium/`, plus `isotropic.py` and `wood.py`.
- Consistent, descriptive parameter and return-key naming across rock physics APIs (e.g., `bulk_modulus_hill`, `shear_modulus_lower/upper/avg`).
- Bounds, mixing, and substitution functions now return dictionaries instead of tuples.

### Deprecated
- Legacy `drp_template.compute.rockphysics.bounds.py` and `mixing.py` kept as lightweight shims; prefer the submodules.
- Old key names and tuple-style returns will be removed in a future minor release.

### Documentation
- API and tutorials updated to new imports and key names.
- Autosummary/autodoc configuration improved to pull full docstrings for submodules.

### Migration Notes
- Update imports to subpackages, for example:
	- `from drp_template.compute.rockphysics.bounds import voigt_reuss_hill_bounds`
	- `from drp_template.compute.rockphysics.mixing import brie_fluid_mixing`
	- `from drp_template.compute.rockphysics.effective_medium import backus_average, gassmann_fluid_substitution`
- Adjust code to read descriptive dict keys instead of positional tuple returns.

## [0.1.0b1] - 2025-11-07

### Added
- Modularized package layout with explicit public APIs across `model`, `image`, `tools`, `io`, and `compute`.
- Integrated Binary Model API (`binary_2d`, `binary_3d`) with periodic boundary generation and true 3D rotations.
- Unified VTK export: `io.writers.export_vti` with JSON sidecar metadata; `io.utils.open_in_paraview` helper.
- Optional dependencies via extras:
	- `pip install drp_template[viz]`, `drp_template[vtk]`, or `drp_template[viz,vtk]`.

### Changed
- SI unit standardization across geometry-related functions; conversions available under `drp_template.compute`.
- Deprecated monolithic legacy modules; replaced with stubs that forward to new submodules.

### Documentation
- Docs generator moved to `docs/scripts/generate_docs.py`.
- Examples reorganized under `examples/<module>/{reference,tutorials}`.

### Testing
- Added tests for raw export + metadata; sample VTI export script provided.

## [0.1.0-alpha] - 2025-10-31

### Added
- Schema versioning system (v1.0) for parameter files
- JSON Schema validation with `jsonschema` package
- Provenance tracking (`generator`, `created_at`, `modified_at`)
- `validate_parameters_file()` public API
- File size metadata in parameter files (`file_size_bytes`, `file_size_mb`)
- Enhanced `get_model_properties()` with numpy-style dimension formatting
- Improved `get_phase_fractions()` with formatted DataFrame output
- Smart slice selection in `ortho_slice()` for multi-phase data
- `list_dir_info()` now supports optional file count return
- nbstripout configuration for cleaner notebook commits
- Comprehensive schema documentation in `schemas/README.md`
- Sphinx documentation with localhost server support

### Changed
- Version updated to `0.1.0-alpha` to signal alpha status
- Removed redundant `timestamp` field (use `modified_at` instead)
- Improved docstrings to NumPy-style format across all modules

### Fixed
- Smart slice selection when center slice doesn't contain all phases
- Better error messages for schema validation failures

## [Unreleased]

### Added (2025-01-05)
- **Binary Model Creation Enhancements**:
	- New `create_binary_model_2d()` function for dedicated 2D model creation
	- New `create_binary_model_3d()` function (wrapper around original with clearer intent)
	- **Periodic boundary conditions** (`periodic` parameter) for both 2D and 3D
		- 2D: Up to 9 periodic copies (1 original + 4 edges + 4 corners)
		- 3D: Up to 27 periodic copies (1 original + 6 faces + 12 edges + 8 corners)
	- **True 3D rotation** with Euler angles (α, β, γ) for random orientations
	- Fixed ellipsoid geometry bug (aspect_ratio now applied to correct axis)
- **Documentation**:
	- Comprehensive "2D vs 3D Models Guide" (`docs/guides/2d_vs_3d_models.md`)
	- Example notebooks:
		- `examples/tools/create_binary_2D_model.ipynb` (new)
		- `examples/tools/create_binary_3D_model.ipynb` (updated with PBC examples)
	- Test suite for periodic boundaries (`dev/test_periodic_boundaries.py`)

### Changed (2025-01-05)
- **Architecture improvements**:
	- Separated 2D and 3D logic for better maintainability (Single Responsibility Principle)
	- Private helper functions: `_make_ellipse_mask_2d()`, `_make_ellipsoid_mask()`
	- Original `create_binary_model()` preserved for backward compatibility
- **Rotation system**:
	- 2D: Simple in-plane rotation (angle around Z-axis)
	- 3D: Full Euler angle rotation (Rz(α) @ Ry(β) @ Rx(γ))

### Fixed (2025-01-05)
- **Critical bug**: Ellipsoid aspect_ratio was applied to wrong axis
	- `orientation='xy'`: Now correctly flattens along Z (was incorrectly Y)
	- `orientation='zx'`: Now correctly flattens along Y (was incorrectly X)
	- `orientation='zy'`: Now correctly flattens along X (was incorrectly Y)
- **Rotation bug**: Random orientations now produce true 3D rotation (was only 2D in-plane)

### Planned
- Migration helpers for future schema versions
- Additional tutorials and examples
- Automated tests for validation logic
- Configuration adapter for YAML/TOML support
