# ------------------------------------------------------------------------------------------------- #
# ------------------------------------------------------------------------------------------------- #
# This script is used as an interface layer between input parameters and calculation modules
# 25-04-2022
# Martin Balcewicz (Bochum University of Applied Sciences)
# website: https://rockphysics.org/people/members/martin-balcewicz
# ------------------------------------------------------------------------------------------------- #
# ------------------------------------------------------------------------------------------------- #
import os


def main():
    print('-------------------------------------------------------------------------------------------------')
    print('-------------------------------------------------------------------------------------------------')
    print('Welcome to Parfile generator')
    print('developed 04/2023 by Martin Balcewicz (mail: martin.balcewicz@rockphysics.org)')
    print('-------------------------------------------------------------------------------------------------')
    print('-------------------------------------------------------------------------------------------------')
    print(' ')


def write_parameters(shape=None, dimension=None, resolution=None):
    if shape is None or shape is 1:
        # Define if model is a cube or not
        shape = 1  # 1 is cube, can be -1
        dimension = int(dimension)
        dimension_x = dimension
        dimension_y = dimension
        dimension_z = dimension
    else:
        print('You do not have a cube system!')
        # Work in progress
        # dimension_x = dimension_x
        # dimension_y = dimension_y
        # dimension_z = dimension_z

    if resolution is not None:
        # Create a paramters file for upcomming calculations
        resolution = resolution
    else:
        raise ValueError('Error! You must set a resolution in µm per voxel')

    # Collect all parameters into a final array
    # arr =

    filename = os.path.join('../', 'Parfile')
    # Write Parfile to local directory
    # with open(filename, "w") as f:
    #     f.write(arr)

    return


def read_parameters():
    return


# ------------------------------------------------------------------------------------------------- #

if __name__ == '__main__':
    main()
