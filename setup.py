from setuptools import setup, find_packages

setup(
    name='drp_template',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'numpy~=1.24.4',
        'matplotlib~=3.7.2',
        'cmcrameri~=1.7',
        'pandas~=2.0.3',
        'scikit-image~=0.20.0',
        'vtk~=9.2.6',
        'tifffile~=2023.4.12',
        'pillow~=10.0.1',
        'porespy~=2.3.0',
        'openpnm~=3.3.0',
        'setuptools~=68.2.2',
    ],
    python_requires='>=3.0, <4',
)
