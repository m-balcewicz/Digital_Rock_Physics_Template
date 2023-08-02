import sys
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
