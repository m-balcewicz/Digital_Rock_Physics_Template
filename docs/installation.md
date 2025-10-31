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

## Verify installation

```python
import drp_template
print(drp_template.__version__)
```
