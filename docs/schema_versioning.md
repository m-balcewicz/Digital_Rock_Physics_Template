# Schema Versioning

The Digital Rock Physics Template uses **schema versioning** for parameter files to ensure data provenance and compatibility across versions.

## Overview

Every parameter JSON file created by this package includes:

```json
{
    "schema_version": "1.0",
    "generator": "drp_template v0.1.0-alpha",
    "created_at": "2025-10-31 12:00:00",
    "modified_at": "2025-10-31 12:30:00",
    ...
}
```

## Schema Version 1.0

### Required Fields

| Field | Type | Description |
|-------|------|-------------|
| `schema_version` | string | Schema version (currently "1.0") |
| `generator` | string | Tool and version that created the file |
| `created_at` | string | Timestamp when file was first created |
| `modified_at` | string | Timestamp of last modification |

### Optional Data Fields

| Field | Type | Description |
|-------|------|-------------|
| `nx`, `ny`, `nz` | integer | Dimensions of the 3D array |
| `dtype` | string | NumPy data type (e.g., "uint8", "float32") |
| `file_path` | string | Path to the data file |
| `file_size_mb` | number | File size in megabytes |
| `voxel_size` | number | Voxel size in micrometers |
| `labels` | object | Phase labels dictionary |
| `fractions` | object | Phase fractions dictionary |

## Versioning Policy

### When to bump MAJOR version (1.0 → 2.0)

- Remove required fields
- Change field types in incompatible ways
- Rename required fields

### When to bump MINOR version (1.0 → 1.1)

- Add new optional fields
- Add new enum values
- Expand validation constraints

## Validation

All parameter files are automatically validated against the JSON Schema when read or written:

```python
import drp_template.default_params as dp

# Automatic validation on write
dp.update_parameters_file('model.json', nx=400, ny=400, nz=400)

# Explicit validation
try:
    dp.validate_parameters_file('model.json')
    print("Valid!")
except ValueError as e:
    print(f"Invalid: {e}")
```

## Migration

When schema versions change, migration helpers will be provided to convert old files to new formats.

## More Information

See `drp_template/default_params/schemas/README.md` for complete schema documentation.
