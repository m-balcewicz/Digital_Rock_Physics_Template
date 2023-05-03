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
import numpy as np
import vtk
from skimage import io
from drp_template.data_review import check_binary
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
    # Load the 3D TIFF file
    data = io.imread(path)

    return data


def import_2d_tiff(path, type):
    if type == 1:
        file_Listing = io.imread_collection(f'{path}/*.tif*')
        first_image = file_Listing[0]
        rows, cols = first_image.shape
        pages = len(file_Listing)
        data = np.zeros((rows, cols, pages))
        for m in range(pages):
            page = file_Listing[m]
            data[:, :, m] = page
        binaries = np.unique(data)
        print('## RAW CT image is loaded')
    elif type == 2:
        file_Listing = io.imread_collection(f'{path}/*.tif*')
        first_image = file_Listing[0]
        rows, cols = first_image.shape
        pages = len(file_Listing)
        data = np.zeros((rows, cols, pages))
        for m in range(pages):
            data[:, :, m] = file_Listing[m]
        data = data.astype(np.int8)
        binaries = np.unique(data)
        print('## segmented CT image is loaded')

        # Check wrong label numbering
        data = check_binary(data)

    else:
        print('## ERROR: Please define type = 1 (for RAW CT images) or type = 2 (for segmented CT images)')
        binaries = 'NaN'
        return

    # Flip the y-axis of the array
    data = np.flip(data, axis=0)

    return data


def import_raw(path, dtype, endian=None, dimension=None):
    """
    Import raw data from a binary file.

    Parameters:
    path (str): Path to the binary file.
    dtype (str): Data type of the binary file. Valid values are 'uint8' and 'uint16'.
    endian (str): Endianness of the binary file, if applicable. Valid values are 'big' and 'little'.
    dimension (int or list of 3 ints): Dimensions of the data. If an int is given, the dimensions are assumed to be equal.

    Returns:
    A numpy array containing the data.

    Raises:
    ValueError: If the dtype or endian parameter is invalid, or if the dimension parameter is invalid or missing.
    IOError: If the file cannot be read.
    """
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
    if dimension is None:
        raise ValueError("No dimension was set!")
    elif isinstance(dimension, int):
        z_size = y_size = x_size = dimension
    elif isinstance(dimension, list) and len(dimension) == 3:
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
    data = check_binary(data)

    # return data.reshape(z_size, y_size, x_size) if dimension is not None else data
    return data

def import_heidi(path, z, x, y, d):
    """
    Reads big-endian binary data_normal from the 'moduli' file at the specified path,
    reads the header entries from the 'moduliheader' file in the same directory,
    parses the header entries to get the dimensions of the data_normal, and returns a
    NumPy array containing the reshaped data_normal.
    """
    try:
        # Construct paths to the 'moduli' and 'moduliheader' files in the given directory
        moduli_file = os.path.join(path, 'moduli')
        header_file = os.path.join(path, 'moduliheader')

        # Read binary data_normal from the 'moduli' file and interpret it as big-endian floats
        with open(moduli_file, 'rb') as fid:
            data = np.array(struct.unpack('>{}f'.format(os.path.getsize(moduli_file) // 4), fid.read()))

        # Read the header entries from the 'moduliheader' file and parse them to get the dimensions
        # Read the header entries from the 'moduliheader' file as text and parse them to get the dimensions
        with open(header_file, 'r') as f:
            header = f.readlines()  # [2:6]
            # z, x, y, d = [int(line.strip().split()[-1]) for line in header_entries]

        # # Define a regular expression pattern to match the "nX=YYYYYY" format
        # pattern = r"n(\d)=(\d+)"
        #
        # # Find all matches of the pattern in the header string
        # matches = re.findall(pattern, header_file)
        #
        # # Extract the second group of each match (the number part), convert to int, and store in a NumPy array
        # dimensions = np.array([int(match[1]) for match in matches])

        # Reshape the data_normal into a 4D array with the parsed dimensions
        data = data.reshape(z, x, y, d)

        return data, header

    except Exception as e:
        print('Error:', e)
        return None


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

    # The data_normal is order in data_normal(z, x, y). Therefore, a transpose is needed:
    # data = np.transpose(data, axes=(1, 2, 0))

    # Finally, flip the data_normal in the y-axis:
    # data = np.flip(data, axis=1)

    print('+++ examples data imported')

    return data


def export_raw(data, path, varname):
    # Create the directory if it doesn't exist
    os.makedirs(path, exist_ok=True)

    # Flatten the data array
    flat_data = data.flatten()

    # Pack the flattened data array into a bytes object
    packed_data = struct.pack(f'>{data.size}B', *flat_data)  # data.size indicating the total number of bytes

    with open(os.path.join(path, varname + '.raw'), 'wb') as f:
        f.write(packed_data)


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
