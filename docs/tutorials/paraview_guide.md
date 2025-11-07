# ParaView Visualization Guide

This guide explains how to visualize your exported 3D digital rock models in ParaView.

## Quick Start

After exporting a model with `export_model()`, you'll have:
- A `.raw` file containing the binary data
- A `.json` file with metadata (dimensions, voxel size, data type, etc.)

## Opening Raw Files in ParaView

### Step 1: Import Raw Data

1. Open ParaView
2. **File → Open** → Select your `.raw` file
3. Choose **"Image Reader"** when prompted

### Step 2: Configure Data Properties

In the Properties panel, you need to set:

#### Data Extent
Based on your model dimensions `(nx, ny, nz)`:
- X: `0` to `nx-1`
- Y: `0` to `ny-1`
- Z: `0` to `nz-1`

Example: For a 100×100×100 model:
```
Data Extent: 0 99 0 99 0 99
```

#### Data Scalar Type

**This is critical!** Choose the correct type based on your Python `dtype`:

| Python dtype | ParaView Scalar Type |
|--------------|---------------------|
| `uint8`      | **unsigned char**   |
| `uint16`     | unsigned short      |
| `int8`       | char                |
| `int16`      | short               |
| `int32`      | int                 |
| `uint32`     | unsigned int        |
| `float32`    | float               |
| `float64`    | double              |

**For binary models** (pore/solid with values 0 and 1), use `dtype='uint8'` → **unsigned char**

#### Data Byte Order
- **Little Endian** (most common for modern systems)
- Check your `parameters.json` for the `order` field

### Step 3: Apply and Visualize

1. Click **Apply** in the Properties panel
2. The model should appear in the 3D view
3. Adjust visualization settings:
   - **Color Map**: Choose appropriate colors for your phases
   - **Opacity**: Adjust for transparency
   - **Slice/Clip**: Create cross-sections

## Reading Metadata from parameters.json

Your exported `.json` file contains all the information needed:

```json
{
  "dimensions": {
    "nx": 100,
    "ny": 100,
    "nz": 100
  },
  "dtype": "uint8",
  "voxel_size": 10.0,
  "order": "C",
  "labels": {
    "0": "Pore",
    "1": "Solid"
  }
}
```

Use this to set ParaView properties:
- **Data Extent**: `0 (nx-1) 0 (ny-1) 0 (nz-1)`
- **Data Scalar Type**: Based on `dtype` (see table above)
- **Data Byte Order**: `C` order = Little Endian

## Common Issues

### Problem: Values appear corrupted
**Solution**: Check that Data Scalar Type matches your `dtype`
- Wrong: Using "int" for uint8 data → values >255 or negative
- Correct: Use "unsigned char" for uint8 data

### Problem: Model dimensions look wrong
**Solution**: Verify Data Extent matches `(nx-1, ny-1, nz-1)`
- ParaView uses 0-indexed ranges
- 100×100×100 model = extent `0 99 0 99 0 99`

### Problem: Colors don't match phase labels
**Solution**: 
1. Open the Color Map Editor
2. Set discrete colors for your phase values (0, 1, 2, etc.)
3. Match colors to your `labels` in the JSON file

## Example Workflow

### Python Export
```python
from drp_template.io import export_model
from drp_template.model import create_binary_model_3d as create_binary_model

# Create model
data = create_binary_model(nx=100, ny=100, nz=100, num_inclusions=5)

# Export with metadata
labels = {0: 'Pore', 1: 'Rock Matrix'}
export_model(
    filename='my_rock_model',
    data=data,
    voxel_size=10.0,
    dtype='uint8',
    order='C',
    filetype='.raw',
    labels=labels
)
```

### ParaView Import Settings
Based on the export above:
- **File**: `my_rock_model.raw`
- **Data Extent**: `0 99 0 99 0 99`
- **Data Scalar Type**: **unsigned char** (because dtype='uint8')
- **Data Byte Order**: Little Endian (because order='C')

### Visualization Tips
1. **Threshold Filter**: Isolate pores (value=0) or solid (value=1)
2. **Contour Filter**: Create isosurfaces at phase boundaries
3. **Slice Filter**: View orthogonal cross-sections
4. **Clip Filter**: Cut the volume to see internal structure

## Advanced: Scaling to Physical Units

If you set `voxel_size` (e.g., 10 µm), you can scale the visualization:

1. Apply **Transform** filter
2. Set scale factors: `(voxel_size, voxel_size, voxel_size)`
3. Now axes show physical dimensions in micrometers

## Quick Reference: Data Type Mapping

```
Python → ParaView
─────────────────────
uint8   → unsigned char  ✓ Most common for binary models
uint16  → unsigned short
int16   → short
int32   → int
float32 → float
float64 → double
```

**Remember**: For binary digital rock models with `dtype='uint8'`, always use **unsigned char** in ParaView!

## See Also

- [Input/Output API Reference](../api/io.md)
- [Tools API Reference](../api/tools.md) - Creating synthetic models
- [Quickstart Guide](../quickstart.md)
