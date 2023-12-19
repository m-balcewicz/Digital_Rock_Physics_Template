# ------------------------------------------------------------------------------------------------- #
# ------------------------------------------------------------------------------------------------- #
# This is a script to import CT.tif images and prepare a CT volume (int8)
# 14-04-2022
# Martin Balcewicz (Bochum University of Applied Sciences)
# website: https://rockphysics.org/people/members/martin-balcewicz
# 1 = RAW
# 2 = segmented
# ------------------------------------------------------------------------------------------------- #
# ------------------------------------------------------------------------------------------------- #
import sys

import numpy as np
import vtk
from skimage import io
from barbara.tools.data_review import check_binary
import struct
import os
from tifffile import tifffile

'''
This script will import and export a range of data sets, e.g. tiff sequences or 3D-raw files. 
If tiff sequences are selected than the user has... 
'''


def main():
    print('-------------------------------------------------------------------------------------------------')
    print('-------------------------------------------------------------------------------------------------')
    print('Welcome to the importer and exporter of high-resolution X-ray Computed Tomography')
    print('developed 04/2023 by Martin Balcewicz (mail: martin.balcewicz@rockphysics.org)')
    print('-------------------------------------------------------------------------------------------------')
    print('-------------------------------------------------------------------------------------------------')
    print(' ')


def import_3d_tiff(path):
    print('importing . . .')
    # Load the 3D TIFF file
    data = io.imread(path)

    return data


def import_2d_tiff(path, type):
    """
    Import raw data from a binary file.

    Parameters:
    -----------
    path : str
        Path to directory with multiple 2D tiff files.
    type : str
        Data type of the binary file. Valid values are 'raw' and 'binary'.

    """
    print('importing . . .')
    try:
        if type == 'raw':
            file_listing = io.imread_collection(f'{path}/*.tif*', plugin='tifffile')
            first_image = file_listing[0]
            cols, rows = first_image.shape
            slices = len(file_listing)
            data = np.zeros((slices, cols, rows))
            for m in range(slices):
                page = file_listing[m]
                data[m, :, :] = page

        elif type == 'binary':
            file_listing = io.imread_collection(f'{path}/*.tif*')
            first_image = file_listing[0]
            rows, cols = first_image.shape
            slices = len(file_listing)
            data = np.zeros((slices, rows, cols))
            for m in range(slices):
                data[m, :, :] = file_listing[m]
            data = data.astype(np.int8)

            # Check wrong label numbering
            data = check_binary(data)

    except IOError as e:
        raise IOError(f"Unable to read file: {e}") from e

    # # Flip the y-axis of the array
    data = np.flip(data, axis=1)
    return data


def import_raw(path, dtype, dimension, endian=None):
    """
    Import raw data from a binary file.

    Parameters:
    -----------
    path : str
        Path to the binary file.
    dtype : str
        Data type of the binary file. Valid values are 'uint8' and 'uint16'.
    endian : str
        Endianness of the binary file, if applicable. Valid values are 'big' and 'little'.
    dimension : int or list of 3 ints (z, y, x-dimension)
        Dimensions of the data. If an int is given, the dimensions are assumed to be equal.

    Returns:
    --------
    A numpy array containing the data.

    Raises:
    --------
    ValueError : If the dtype or endian parameter is invalid, or if the dimension parameter is invalid or missing.

    IOError : If the file cannot be read.
    """
    print('importing . . .')
    # Define a dictionary mapping data types and byte orders to their respective numpy dtypes
    dtype_dict = {'uint8': np.uint8,
                  'uint16': {'little': np.dtype('<u2'),
                             'big': np.dtype('>u2')}}

    # Check if the data type and byte order are valid
    if dtype not in dtype_dict:
        raise ValueError(f"Invalid dtype value: {dtype}")

    if endian is not None and endian not in dtype_dict[dtype]:
        raise ValueError(f"Invalid endian value: {endian}")

    # Define the shape of the data
    if dimension is False:
        raise ValueError("No dimension was set!")
    elif isinstance(dimension, int):
        z_size = y_size = x_size = dimension
    elif isinstance(dimension, list) and len(dimension) == 3:
        # TODO: Add to check if endian is set! else must be an error.
        # TODO: change dimensions to (z, x, y)
        z_size, y_size, x_size = dimension
    else:
        raise ValueError("Invalid dimension value!")

    # Read the data from the file
    try:
        with open(path, 'rb') as f:
            data_type = dtype_dict[dtype]
            if endian is not None:
                data_type = data_type[endian]
            data = np.fromfile(f, dtype=data_type)
    except IOError as e:
        raise IOError(f"Unable to read file: {e}") from e

    # Reshape the data_normal to the original shape
    data = data.reshape(z_size, y_size, x_size)

    # Check wrong label numbering
    data = check_binary(data=data)

    # return data.reshape(z_size, y_size, x_size) if dimension is not None else data
    return data

def import_csv(path, dimension):
    """
    Reads a header file and imports moduli data from a binary file.

    Args:
        path (str): The path to the directory containing the header and binary files.

    Returns:
        numpy.memmap: The moduli data stored in a memory-mapped array.

    """
    z = dimension[0]
    x = dimension[1]
    y = dimension[2]

    data_shape = (z, x, y)  # Define the shape of your data

    data = np.genfromtxt(path, dtype=np.int32, delimiter=',')
    data = data.reshape(data_shape)
    data = check_binary(data)

    return data


def import_moduli(path):
    """
    Reads binary data and corresponding header information from HEIDI files.

    Parameters:
        path (str): Path to the binary file without the '.header' extension.

    Returns:
        tuple: A tuple containing the following elements:
            - data (ndarray): Numpy array containing the binary data.
            - z (int): Number of elements in the first dimension of the data array.
            - x (int): Number of elements in the second dimension of the data array.
            - y (int): Number of elements in the third dimension of the data array.
            - seed (int): Seed value extracted from the header information.
            - inclusion (int): Inclusion value extracted from the header information.
            - scatterer (int): Scatterer value extracted from the header information.
    """
    # Read header entries
    header_file = path + 'header'
    with open(header_file, 'r') as f:
        lines = f.readlines()

    header = {}

    for line in lines:
        line = line.strip()
        if '=' in line:
            key, value = line.split('=')
            key = key.strip()
            value = value.strip()
            header[key] = value

    n1 = int(header['n1'])
    n2 = int(header['n2'])
    n3 = int(header['n3'])
    n4 = int(header['n4'])

    z = n1
    x = n2
    y = n3
    if n4 > 1:
        d = n4
        data_shape = (z, x, y, d)  # Define the shape of your data
    else:
        data_shape = (z, x, y)  # Define the shape of your data

    data = np.memmap(path, dtype='>f4', mode='r', shape=data_shape, order="F")
    # order: Fortran ordering or C ordering
    # dtype: big-endian
    # mode: read

    return data, header

def import_snap(filename):
    """
    Reads a header file and imports zsnap, xsnap, or ysnap data from a binary file.

    Args:
        path (str): The path to the directory containing the header and binary files.

    Returns:
        numpy.memmap: The moduli data stored in a memory-mapped array.

    """
    # Read header entries
    header_file = filename + 'header'
    with open(header_file, 'r') as f:
        lines = f.readlines()

    header = {}

    for line in lines:
        line = line.strip()
        if '=' in line:
            key, value = line.split('=')
            key = key.strip()
            value = value.strip()
            header[key] = value

    n1 = int(header['n1'])
    n2 = int(header['n2'])
    n3 = int(header['n3'])
    n4 = int(header['n4'])

    z = n1
    x = n2
    y = n3
    if n4 > 1:
        d = n4
        data_shape = (z, x, y, d)  # Define the shape of your data
    else:
        data_shape = (z, x, y)  # Define the shape of your data

    data = np.memmap(filename, dtype='>f4', mode='r', shape=data_shape, order="F")
    # order: Fortran ordering or C ordering
    # dtype: big-endian
    # mode: read

    return data, header


def import_test(path, dimension=None):
    # Define the shape of the data_normal
    if dimension is not None:
        x_size = dimension
        y_size = dimension
        z_size = dimension
    else:
        raise ValueError("No dimension was set!")

    # Read the data_normal from the file
    with open(path, 'rb') as f:
        data = np.fromfile(f, dtype=np.uint8)

    # Reshape the data_normal to the original shape
    data = data.reshape(z_size, y_size, x_size)
    print('+++ examples data imported')

    return data


def export_raw(data, path=None, filename=None, voxel_size=None, dtype='uint8', endian='little'):
    """
    Export raw data to a binary file with optional dimension, dtype and endian specification.
    Also writes an ASCII file with information about the exported data.

    Parameters:
    -----------
    data : ndarray
        The data to be exported.
    path : str
        The directory path to save the exported data.
    varname : str
        The name of the variable being exported.
    dtype : str, optional
        The data type of the exported data. Can be 'uint8' or 'uint16'. Default is 'uint8'.
    endian : str, optional
        The byte order of the exported data, if dtype is 'uint16'. Can be 'big' or 'little'. Default is None.

    Returns:
    --------
    None
    """
    # Create the directory if it doesn't exist
    if path is None:
        path = os.getcwd()
    else:
        os.makedirs(path, exist_ok=True)

    if filename is None:
        filename = 'output'

    # Flatten the data array
    flat_data = data.flatten()

    # Pack the flattened data array into a bytes object
    endian_check_data = data.dtype.byteorder
    endian_check_sys = sys.byteorder
    # print(f'check: {endian_check_data}')

    if dtype == 'uint8':
        # Flatten the data array
        flat_data = data.flatten()

        packed_data = struct.pack(f'>{data.size}B', *flat_data)
        # Write the packed data to file
        with open(os.path.join(path, filename + '.raw'), 'wb') as f:
            f.write(packed_data)

    elif dtype == 'uint16':
        if endian == 'little':
            if endian_check_data == '<':
                with open(os.path.join(path, filename + '_le.raw'), 'wb') as f:
                    data.tofile(f, sep='', format='<')

            elif endian_check_data == '>':
                with open(os.path.join(path, filename + '_le.raw'), 'wb') as f:
                    data.tofile(f, sep='', format='<')

            elif endian_check_data == '=' and endian_check_sys == 'big':
                with open(os.path.join(path, filename + '_le.raw'), 'wb') as f:
                    data.tofile(f, sep='', format='<')

            elif endian_check_data == '=' and endian_check_sys == 'little':
                with open(os.path.join(path, filename + '_le.raw'), 'wb') as f:
                    data.tofile(f, sep='', format='<')

        elif endian == 'big':
            if endian_check_data == '<':
                with open(os.path.join(path, filename + '_be.raw'), 'wb') as f:
                    data.tofile(f, sep='', format='>')

            elif endian_check_data or endian_check_sys == '>':
                with open(os.path.join(path, filename + '_be.raw'), 'wb') as f:
                    data.tofile(f, sep='', format='>')

            elif endian_check_data == '=' and endian_check_sys == 'little':
                with open(os.path.join(path, filename + '_be.raw'), 'wb') as f:
                    data.tofile(f, sep='', format='>')

            elif endian_check_data == '=' and endian_check_sys == 'big':
                with open(os.path.join(path, filename + '_be.raw'), 'wb') as f:
                    data.tofile(f, sep='', format='>')
        else:
            raise ValueError("Invalid endian value!")
    else:
        raise ValueError("Invalid dtype value!")

    # Write the ASCII file with information about the exported data
    if voxel_size is not None:
        voxel_size_info = voxel_size
    else:
        voxel_size_info = "unknown"

    info = f"This data was created by Digital Rock Physics Template\n" \
           f"by Martin Balcewicz (martin.balcewicz@rockphysics.org)\n\n" \
           f"data: {filename}\n" \
           f"dimension (z, y, x): {data.shape}\n" \
           f"type: {dtype}\n" \
           f"endian: {endian}\n"\
           f"voxel size (voxel/μm): {voxel_size_info}\n"\

    print("Path:", os.path.join(path, filename + '_header.txt'))
    print("Info:", info)
    print("Data shape:", data.shape)

    with open(os.path.join(path, filename + '_header.txt'), 'w', encoding="utf-8") as f:
        f.write(info)

    print(f'. . . raw data ({dtype}) saved as {path}/{filename}.raw')


def export_3d_tif(data, path, varname):
    # Create the directory if it doesn't exist
    os.makedirs(path, exist_ok=True)

    # Combine the directory and file name variables using os.path.join
    filepath = os.path.join(path, varname + '.tif')  # add '.tif' to the file name

    # Save the array as a 3D TIFF file using tifffile
    tifffile.imwrite(filepath, data)


def export_2d_tif(data, path, varname):
    # Create the subdirectory for the 2D TIFF images
    subdir_path = os.path.join(path, varname)
    os.makedirs(subdir_path, exist_ok=True)

    # Determine the number of digits needed for the slice index
    num_digits = len(str(data.shape[0])) + 1

    # Loop over each slice in the z-direction
    for z in range(data.shape[0]):
        # Extract the slice as a 2D array
        slice_data = data[z, :, :]

        # Create the file name for the slice using the slice index
        slice_filename = f"{varname}_xy_{z + 1:0{num_digits}d}.tif"  # e.g., "data_xy_001.tif"

        # Combine the directory and file name variables using os.path.join
        slice_filepath = os.path.join(subdir_path, slice_filename)

        # Save the slice as a 2D TIFF file using tifffile
        tifffile.imwrite(slice_filepath, slice_data)


def export_vtk(array_3d, path, varname):
    # Validate input: must be a 3D numpy array
    assert isinstance(array_3d, np.ndarray) and array_3d.ndim == 3, \
        "Input data must be a 3D numpy array"

    # Create the directory if it doesn't exist
    os.makedirs(path, exist_ok=True)

    # Create a VTKImageData object
    vtk_data = vtk.vtkImageData()
    vtk_data.SetDimensions(array_3d.shape)
    #  The SetSpacing() method sets the spacing between the points in
    #  the vtkImageData object. For example, if the spacing is set to (1,1,1),
    #  it means that each point in the object represents a voxel of size 1x1x1
    #  in physical units. Setting the spacing to different values changes the
    #  size of each voxel in physical units.
    vtk_data.SetSpacing(1, 1, 1)
    # The SetOrigin() method sets the physical coordinates of the origin of the
    # vtkImageData object. For example, if the origin is set to (0,0,0), it means
    # that the center of the first voxel in the vtkImageData object is located at
    # physical coordinates (0,0,0). Setting the origin to different values changes
    # the physical location of the origin and the location of each voxel in
    # physical units.
    vtk_data.SetOrigin(0, 0, 0)

    # Create a VTK array from the 3D numpy array
    vtk_array = vtk.vtkFloatArray()
    vtk_array.SetNumberOfComponents(1)
    vtk_array.SetNumberOfTuples(array_3d.size)
    vtk_array.SetVoidArray(array_3d.flatten(), array_3d.size, 1)

    # Set the VTK array as the point data of the VTKImageData object
    vtk_data.GetPointData().SetScalars(vtk_array)

    # Write the VTKImageData object to a VTK file
    output_filename = os.path.join(path, varname + '.vti')
    writer = vtk.vtkXMLImageDataWriter()
    writer.SetFileName(output_filename)
    writer.SetInputData(vtk_data)
    writer.Write()

    print(f"VTK file saved to {output_filename}")


# ------------------------------------------------------------------------------------------------- #

if __name__ == '__main__':
    main()
