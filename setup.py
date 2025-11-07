from setuptools import setup, find_packages

setup(
    name='drp_template',
    version='0.1.0b1',
    packages=find_packages(),
    package_data={
        'drp_template.default_params': ['*.json'],
        'drp_template': ['**/*.json'],
    },
    include_package_data=True,
    install_requires=[
        'numpy>=1.24.0',
        'matplotlib>=3.7.2,<3.8.2',
        'cmcrameri~=1.7',
        'pandas>=2.0.0',
        'scikit-image~=0.20.0',
        'tifffile~=2023.4.12',
        'imagecodecs>=2023.1.23',
        'h5py>=2.2.3',
        'jsonschema>=4.0.0'
    ],
    extras_require={
        'viz': [
            'pyvista>=0.43.0',
            'trame>=3.4',
            'trame-vtk',
            'trame-vuetify',
            'ipywidgets>=8.0.0',
        ],
        'vtk': [
            'vtk>=9.2',
        ],
    },
    python_requires='>=3.8, <4',
)