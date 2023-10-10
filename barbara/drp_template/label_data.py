# ------------------------------------------------------------------------------------------------- #
# ------------------------------------------------------------------------------------------------- #
# This is a script to label CT data_normal (int8)
# 14-04-2023
# Martin Balcewicz (Bochum University of Applied Sciences)
# website: https://rockphysics.org/people/members/martin-balcewicz
# ------------------------------------------------------------------------------------------------- #
# ------------------------------------------------------------------------------------------------- #
from barbarakit.drp_template import plot_slice
import numpy as np


def label_binary(data):
    # Create the centered slice of a 3D volume
    slice = int(np.shape(data)[0] / 2)

    # Get the unique values and their counts
    unique, counts = np.unique(data, return_counts=True)

    # Create an empty labels array
    labels = {}

    for m in range(len(unique)):
        # Create a copy of the input array and set all values to 0
        data_temp = np.zeros_like(data)

        # Set the values that match the current unique value to 1
        data_temp[data == unique[m]] = 1
        fig = plot_slice(data=data_temp, plane='xy')
        fig.show()

        # Prompt the user to name the presented phase and store the input in labels[m]
        phase_name = input(f'Name presented phase {unique[m]} with index {m}: ')
        labels[unique[m]] = phase_name

    return labels
