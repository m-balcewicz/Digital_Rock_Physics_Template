import numpy as np


def check_binary(data):
    unique_phases = np.unique(data)

    if min(unique_phases) == 0:
        print('+++ nice data!')

    else:
        print('+++ automatic adjustment is needed')
        data = data - 1

    return data
