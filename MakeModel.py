import numpy as np


def make_model(size, num_phases):
    data = np.random.randint(0, num_phases, size=(size, size, size), dtype=np.uint8)
    # Increase each cell by 1
    data += 1

    return data
