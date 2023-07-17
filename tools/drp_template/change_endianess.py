# ------------------------------------------------------------------------------------------------- #
# ------------------------------------------------------------------------------------------------- #
# This is a script to transform form little-endian to big-endian and vice-versa.
# 04-05-2023
# Martin Balcewicz (Bochum University of Applied Sciences)
# website: https://rockphysics.org/people/members/martin-balcewicz
# ------------------------------------------------------------------------------------------------- #
# ------------------------------------------------------------------------------------------------- #
def little_to_big(data):
    """
    Transforming little-endian binary data to big-endian binary data.

    Parameters:
    -----------
    Input : binary data
        In little-endian format.

    Output : binary data
        Swapped byte order from little-endian to big-endian format.
    """
    output_be = data.byteswap().newbyteorder('>')
    return output_be


def big_to_little(data):
    """
    Transforming big-endian binary data to little-endian binary data.

    Parameters:
    -----------
    Input : binary data
        In big-endian format.

    Output : binary data
        Swapped byte order from big-endian to little-endian format.
    """
    output_le = data.byteswap().newbyteorder('<')
    return output_le
