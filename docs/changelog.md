# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
