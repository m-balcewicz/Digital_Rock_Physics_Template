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
from skimage import io
import time
from control_data import check_binary
import struct
import os
from alive_progress import alive_bar
# import re
from tqdm import tqdm

'''
This script will import an range of data sets, e.g. tiff sequences or 3D-raw files. If tiff sequences are selected than 
the user has 
'''


def main():
    print('-------------------------------------------------------------------------------------------------')
    print('-------------------------------------------------------------------------------------------------')
    print('Welcome to the importer of high-resolution X-ray Computed Tomography')
    print('developed 04/2023 by Martin Balcewicz (mail: martin.balcewicz@rockphysics.org)')
    print('-------------------------------------------------------------------------------------------------')
    print('-------------------------------------------------------------------------------------------------')
    print(' ')


def import_tiff(path, type):
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

        # # CHECK WRONG LABEL NUMBERING
        # if 0 in binaries:
        #     data_recovery = data
        #     for m in range(len(binaries)):
        #         # SEARCH FOR CURRENT BINARY AND CHANGE TO ABSTRACT (OLD_BINARY + 100)
        #         data[data == binaries[m]] = 100 + m
        #     for m in range(len(binaries)):
        #         data[data == (100 + m)] = m
        # else:
        #     print('## nice data')

        # Check wrong label numbering
        data = check_binary(data)

    else:
        print('## ERROR: Please define type = 1 (for RAW CT images) or type = 2 (for segmented CT images)')
        binaries = 'NaN'
        return

    # # IMPORTANT: due to reading automations of arrays the final array's
    # # columns must be flipped to fit the original data set!
    # data = np.flip(data, axis=1)
    return data, rows, cols, pages, binaries


def import_raw(path, dimension=None):
    print('+-------------------------------------------------------------------------------------------------+')
    print('+-------------------------------------------------------------------------------------------------+')
    print('+--- Welcome to the importer of high-resolution X-ray Computed Tomography                      ---+')
    print('+--- developed 04/2023 by Martin Balcewicz (mail: martin.balcewicz@rockphysics.org)            ---+')
    print('+-------------------------------------------------------------------------------------------------+')
    print('+-------------------------------------------------------------------------------------------------+')
    print(' ')

    # Define the shape of the data
    if dimension is not None:
        x_size = dimension
        y_size = dimension
        z_size = dimension
    else:
        raise ValueError("No dimension was set!")


    # # Read the data from the file
    # with open(path, 'rb') as f:
    #     data = np.fromfile(tqdm(f, desc="Importing data"), dtype=np.uint8)

    # Read the data from the file with alive_progress bar
    with open(path, 'rb') as f:
        data = np.fromfile(f, dtype=np.uint8)

    # Reshape the data to the original shape
    data = data.reshape((x_size, y_size, z_size))

    # Check wrong label numbering
    data = check_binary(data)

    return data


def import_heidi(path, z, x, y, d):
    """
    Reads big-endian binary data from the 'moduli' file at the specified path,
    reads the header entries from the 'moduliheader' file in the same directory,
    parses the header entries to get the dimensions of the data, and returns a
    NumPy array containing the reshaped data.
    """
    try:
        # Construct paths to the 'moduli' and 'moduliheader' files in the given directory
        moduli_file = os.path.join(path, 'moduli')
        header_file = os.path.join(path, 'moduliheader')

        # Read binary data from the 'moduli' file and interpret it as big-endian floats
        with open(moduli_file, 'rb') as fid:
            data = np.array(struct.unpack('>{}f'.format(os.path.getsize(moduli_file) // 4), fid.read()))

        # Read the header entries from the 'moduliheader' file and parse them to get the dimensions
        # Read the header entries from the 'moduliheader' file as text and parse them to get the dimensions
        with open(header_file, 'r') as f:
            header = f.readlines()#[2:6]
            # z, x, y, d = [int(line.strip().split()[-1]) for line in header_entries]

        # # Define a regular expression pattern to match the "nX=YYYYYY" format
        # pattern = r"n(\d)=(\d+)"
        #
        # # Find all matches of the pattern in the header string
        # matches = re.findall(pattern, header_file)
        #
        # # Extract the second group of each match (the number part), convert to int, and store in a NumPy array
        # dimensions = np.array([int(match[1]) for match in matches])

        # Reshape the data into a 4D array with the parsed dimensions
        data = data.reshape(z, x, y, d)

        return data, header

    except Exception as e:
        print('Error:', e)
        return None


# ------------------------------------------------------------------------------------------------- #

if __name__ == '__main__':
    main()
