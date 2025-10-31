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

### Planned
- Migration helpers for future schema versions
- Additional tutorials and examples
- Automated tests for validation logic
- Configuration adapter for YAML/TOML support
