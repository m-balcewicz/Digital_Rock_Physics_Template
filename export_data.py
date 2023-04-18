import os
import numpy as np


def main():
    print('-------------------------------------------------------------------------------------------------')
    print('-------------------------------------------------------------------------------------------------')
    print('Welcome to exporter for raw files')
    print('developed 04/2023 by Martin Balcewicz (mail: martin.balcewicz@rockphysics.org)')
    print('-------------------------------------------------------------------------------------------------')
    print('-------------------------------------------------------------------------------------------------')
    print(' ')


def export_raw(data, path, varname):
    unique_phases, num_phases_count = np.unique(data, return_counts=True)
    num_phases = np.size(unique_phases)
    # Save new data as a 'uint8' raw file
    with open(os.path.join(path, varname + '.raw'), 'wb') as f:
        data.tofile(f)

    print(f'model: \'{varname}.raw\' with {num_phases} unique phase(s) is saved as uint8 in: {path}')


# ------------------------------------------------------------------------------------------------- #

if __name__ == '__main__':
    main()
