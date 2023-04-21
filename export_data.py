import os
import numpy as np
from tifffile import tifffile


def main():
    print('-------------------------------------------------------------------------------------------------')
    print('-------------------------------------------------------------------------------------------------')
    print('Welcome to exporter for raw files')
    print('developed 04/2023 by Martin Balcewicz (mail: martin.balcewicz@rockphysics.org)')
    print('-------------------------------------------------------------------------------------------------')
    print('-------------------------------------------------------------------------------------------------')
    print(' ')


# def export_raw(data, path, varname):
#     # Transpose the dimensions to ensure the format is data(x,y,z)
#     data = np.transpose(data, axes=(2, 0, 1))
#     unique_phases, num_phases_count = np.unique(data, return_counts=True)
#     num_phases = np.size(unique_phases)
#     # Save new data as a 'uint8' raw file
#     with open(os.path.join(path, varname + '.raw'), 'wb') as f:
#         data.tofile(f)
#
#     print(f'model: \'{varname}.raw\' with {num_phases} unique phase(s) is saved as uint8 in: {path}')

def export_raw(data, path, varname):
    # Transpose the dimensions to ensure the format is data(x,y,z)
    data = np.transpose(data, axes=(2, 0, 1))

    # Get the number of unique phases in the data
    unique_phases, num_phases_count = np.unique(data, return_counts=True)
    num_phases = np.size(unique_phases)

    # Save the data as a big-endian uint8 raw file
    with open(os.path.join(path, varname + '.raw'), 'wb') as f:
        data.astype(np.uint8).byteswap().tofile(f, sep='', format='')

    print(f"Model: '{varname}.raw' with {num_phases} unique phase(s) is saved as big-endian uint8 in: {path}")


def export_3d_tif(data, path, varname):
    # Transpose the dimensions to ensure the format is data(x,y,z)
    data = np.transpose(data, axes=(2, 0, 1))

    # Save the data as a 3D TIFF file
    tifffile.imwrite(os.path.join(path, varname + '.tif'), data, imagej=True)

    print(f"Model: '{varname}.tif' is saved as 3D TIFF in: {path}")


# ------------------------------------------------------------------------------------------------- #

if __name__ == '__main__':
    main()
