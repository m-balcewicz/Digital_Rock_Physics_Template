# ------------------------------------------------------------------------------------------------- #
# ------------------------------------------------------------------------------------------------- #
# This is a script to label CT data (int8)
# 14-04-2023
# Martin Balcewicz (Bochum University of Applied Sciences)
# website: https://rockphysics.org/people/members/martin-balcewicz
# ------------------------------------------------------------------------------------------------- #
# ------------------------------------------------------------------------------------------------- #
import show_data as sc
import numpy as np


def label_binary(data, type=2):
    # Create the centered slice of a 3D volume
    slice = int(np.shape(data)[0] / 2)

    # Get the unique values and their counts
    unique, counts = np.unique(data, return_counts=True)

    # Create an empty labels array
    # labels = np.zeros(len(unique), 2)
    labels = [""] * len(unique)

    for m in range(len(unique)):
        # Create a copy of the input array and set all values to 0
        data_temp = np.zeros_like(data)

        # Set the values that match the current unique value to 1
        data_temp[data == unique[m]] = 1
        fig = sc.visualize_plane(data_temp, type, slice, plane='xy')
        fig.show()

        # Prompt the user to name the presented phase and store the input in labels[m]
        phase_name = input(f'Name presented phase {unique[m]} with index {m}: ')
        labels[m] = phase_name

    labels = list(zip(unique, labels))

    return labels
