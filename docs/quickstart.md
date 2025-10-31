# Quick Start Guide

This guide will walk you through the basic workflow of the Digital Rock Physics Template.

## 1. Import Data

### From RAW binary file

```python
import drp_template.input_output as io

# Import raw binary data
data = io.import_model(
    file_path='path/to/data.raw',
    dtype='uint8',
    dimensions={'nz': 400, 'ny': 400, 'nx': 400},
    voxel_size=2.5  # micrometers
)
```

This automatically creates a JSON parameter file (`data.json`) with metadata.

### From TIFF sequence

```python
# Import a sequence of TIFF files
data = io.import_tiff_sequence(
    directory='path/to/tiff_folder',
    file_pattern='slice_*.tif'
)
```

## 2. Visualize Data

### Orthogonal slice view

```python
import drp_template.image as image

fig, ax, pcm = image.ortho_slice(
    data=data,
    paramsfile='data.json',
    plane='xy',  # or 'xz', 'yz'
    cmap_set='gray',
    slice=200  # or None for middle slice
)

# Save the figure
image.save_figure(fig, filename='slice_view')
```

### Histogram

```python
fig, ax = image.histogram(
    data=data,
    paramsfile='data.json',
    log_scale='y'
)
```

## 3. Analyze Phase Distribution

### Quick overview

```python
import drp_template.tools as tools

props = tools.get_model_properties(
    filepath='data.raw',
    dimensions={'nz': 400, 'ny': 400, 'nx': 400},
    labels={'0': 'Pore', '1': 'Quartz', '2': 'Feldspar'},
    verbose=True
)
```

### Detailed phase analysis

```python
import drp_template.math as drp_math

# Define phase labels
labels = {
    '0': 'Pore',
    '1': 'Quartz',
    '2': 'Feldspar',
    '3': 'Clay'
}

# Get detailed phase fractions
table = drp_math.get_phase_fractions(
    data=data,
    labels=labels,
    paramsfile='data.json',
    log=True
)
```

## 4. Parameter File Management

### Read parameters

```python
import drp_template.default_params as dp

# Read single parameter
nx = dp.read_parameters_file('data.json', paramsvars='nx')

# Read multiple parameters
dims = dp.read_parameters_file('data.json', paramsvars=['nx', 'ny', 'nz'])

# Read all parameters
all_params = dp.read_parameters_file('data.json')
```

### Validate parameter file

```python
# Validate against JSON Schema
is_valid = dp.validate_parameters_file('data.json')
print(f"Valid: {is_valid}")
```

## Next Steps

- Check out the [Tutorials](tutorials/index.md) for detailed examples
- Explore the [API Reference](api/input_output.md) for all available functions
- Learn about [Schema Versioning](schema_versioning.md) for data provenance
