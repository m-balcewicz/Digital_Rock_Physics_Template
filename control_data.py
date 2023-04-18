import numpy as np


def check_binary(data):
    unique_phases = np.unique(data)

    if min(unique_phases) == 0:
        print('+--------------------------------------------+')
        print('nice data!')
        print('+--------------------------------------------+')
    else:
        print('+--------------------------------------------+')
        print('I am sorry, automatic adjustment is necessary.')
        print('+--------------------------------------------+')
        data = data - 1

    return data
