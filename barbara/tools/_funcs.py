import numpy as np

__all__ = [
    'check_binary'
]

from barbara.default_params import print_style


def check_binary(model, filename):
    unique_phases = np.unique(model)

    if min(unique_phases) == 0:
        print_style(f'{filename}:\n'
                    f'Nice data; the minimum value in your data is 0'
                    )
    elif min(unique_phases) == -1:
        # print("+++ automatic adjustment is needed")
        print_style(f'{filename}:\n'
                    f'Ups, the minimum value in your data is -1. Automatic adjustments are needed.'
                    )
        # print(f"min value: {min(unique_phases)}")
        model = model + 1
    elif min(unique_phases) == 1:
        # print("+++ automatic adjustment is needed")
        print_style(f'{filename}: \n'
                    f'Ups, the minimum value in your data is 1. Automatic adjustments are needed.'
                    )
        # print(f"min value: {min(unique_phases)}")
        model = model - 1

    return model
