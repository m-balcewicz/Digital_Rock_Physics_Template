# Installation

## Requirements

- Python >= 3.8
- conda or pip

## Install from source

Clone the repository and install in development mode:

```bash
git clone https://github.com/m-balcewicz/Digital_Rock_Physics_Template.git
cd Digital_Rock_Physics_Template
pip install -e .
```

Optional extras (install only what you need):

```bash
# Visualization stack (plotting, animations)
pip install -e .[viz]

# VTK export support
pip install -e .[vtk]

# Both extras
pip install -e .[viz,vtk]
```

## Dependencies

The following packages will be automatically installed:

- numpy >= 1.24.0
- matplotlib >= 3.7.2
- pandas >= 2.0.0
- scikit-image ~= 0.20.0
- tifffile ~= 2023.4.12
- h5py >= 2.2.3
- jsonschema >= 4.0.0
- cmcrameri ~= 1.7

Optional extras pull additional dependencies (examples):
- [viz] may include seaborn, imageio-ffmpeg, etc.
- [vtk] enables VTK `.vti` export and ParaView integration helpers

## Verify installation

```python
import drp_template
print(drp_template.__version__)
```
