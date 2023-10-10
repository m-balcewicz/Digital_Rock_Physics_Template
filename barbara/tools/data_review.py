import sys
import os
import numpy as np


def check_binary(data):
    unique_phases = np.unique(data)

    if min(unique_phases) == 0:
        print('+++ nice data!')
    elif min(unique_phases) == -1:
        print("+++ automatic adjustment is needed")
        print(f"min value: {min(unique_phases)}")
        data = data + 1
    elif min(unique_phases) == 1:
        print("+++ automatic adjustment is needed")
        print(f"min value: {min(unique_phases)}")
        data = data - 1

    return data


def check_endian(data):
    endian_data = data.dtype.byteorder
    endian_native = sys.byteorder
    if endian_data == '<':
        print("little-endian byte order")
    elif endian_data == '>':
        print("big-endian byte order")
    elif endian_data == '=':
        if endian_native == 'little':
            print("little-endian byte order")
        elif endian_native == 'big':
            print("big-endian byte order")
        else:
            raise ValueError("Invalid endian!")
    else:
        raise ValueError("Invalid endian!")

    return endian_data


# def calculate_conversion_factor(file_size_bytes, voxel_size, dimensions):
#     # Calculate the number of voxels in each dimension
#     num_voxels = [size / voxel_size for size in dimensions]
#
#     # Calculate the conversion factor for each dimension
#     conversion_factors = [size / num_voxel for size, num_voxel in zip(dimensions, num_voxels)]
#
#     return conversion_factors
#
#
# def check_voxel_size(filepath, dimension):
#     if not dimension:
#         raise ValueError("No dimension was set!")
#     elif isinstance(dimension, int):
#         z_size = y_size = x_size = dimension
#     elif isinstance(dimension, list) and len(dimension) == 3:
#         z_size, y_size, x_size = dimension
#     else:
#         raise ValueError("Invalid dimension value!")
#
#     # Calculate the total number of voxels based on the data size and voxel size
#     file_size_bytes = os.path.getsize(filepath)  # Get the file size in bytes
#     print(f"file size in bytes: {file_size_bytes}")
#
#     # Calculate the total number of voxels
#     total_voxels = x_size * y_size * z_size
#     print(f"total voxels: {total_voxels}")
#
#     # Conversion factor from bytes to micrometers (µm)
#     # Replace this with the actual conversion factor based on your data format.
#     bytes_to_micrometers = 1.0  # For example, if 1 byte represents 0.1 µm
#
#     # Calculate the size of each voxel in bytes
#     voxel_size_bytes = file_size_bytes / total_voxels
#
#     # Calculate the voxel size in micrometers
#     voxel_size = voxel_size_bytes * bytes_to_micrometers
#
#     # voxel_count = file_size_bytes / (z_size * x_size * y_size * 2)  # Assuming 2 bytes per voxel (16-bit)
#
#     # Calculate the voxel size in micrometers
#     # Assuming that the data is isotropic (equal voxel sizes in all dimensions)
#     # voxel_size = x_size / (voxel_count ** (1 / 3))
#
#     return voxel_size