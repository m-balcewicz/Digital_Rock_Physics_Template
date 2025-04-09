from setuptools import setup, find_packages

setup(
    name='drp_template',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'numpy>=1.24.0',
        'matplotlib>=3.7.2',
        'cmcrameri~=1.7',
        'pandas>=2.0.0',
        'scikit-image~=0.20.0',
        'tifffile~=2023.4.12',
        'h5py>=2.2.3'
    ],
    python_requires='>=3.0, <4',
)