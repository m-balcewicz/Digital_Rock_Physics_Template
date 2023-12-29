import numpy as np
import pandas as pd
import glob
import os
import matplotlib.pyplot as plt

from skimage.measure import label
from drp_template.default_params import read_parameters_file, check_output_folder
from drp_template.image import plot_slice

__all__ = [
    'get_connected_porosity',
    'get_phase_fractions',
    'label_binary'
]


def get_connected_porosity(data, paramsfile='parameters.json'):
    # Initialization
    nx = read_parameters_file(paramsfile=paramsfile, paramsvars='nx')
    ny = read_parameters_file(paramsfile=paramsfile, paramsvars='ny')
    nz = read_parameters_file(paramsfile=paramsfile, paramsvars='nz')

    image3DConnected = np.ones((nx, ny, nz), dtype=np.uint8)

    # Step 1: Labeling the pores
    # Inverse grains <-> pores
    image3DInverse = np.abs(1 - data)
    poreLabel = label(image3DInverse, connectivity=1)

    print(poreLabel)
    # image3DInverseLabel = poreLabel
    #
    # # Step 2: Find the label number that exist on both ends
    # tempFirstSlide = image3DInverseLabel[:, :, 0]
    # tempLastSlide = image3DInverseLabel[:, :, -1]
    #
    # labelFirstSlide = np.unique(tempFirstSlide)
    # labelLastSlide = np.unique(tempLastSlide)
    # labelEffective = np.intersect1d(labelFirstSlide, labelLastSlide)
    #
    # # Step 3: Create connected pore space
    # nLabel = len(labelEffective)
    # for i in range(nLabel):
    #     lbl = labelEffective[i]
    #     if lbl >= 1:  # Pore = 1+ -> 0
    #         image3DConnected[image3DInverseLabel == lbl] = 0
    #     else:  # Grain = 0 -> 1
    #         image3DConnected[image3DInverseLabel == lbl] = 1

    return poreLabel


def get_phase_fractions(data, labels=None, filename=None, log=True):
    """
    Calculate fractions and generate a table. Save the table to a text file with an incremental index.

    Args:
        data (array-like): The input data for which fractions need to be calculated.
        labels (dict, optional): A dictionary containing labels for each unique value in the data.
            The dictionary should have the form {key: label}, where key represents the unique value
            and label represents the corresponding label. Defaults to None.

    Returns:
        str: A formatted table containing the unique values, counts, fractions, and labels (if provided).

    Raises:
        ValueError: If labels is provided and is not a dictionary.

    """
    if labels is not None:
        if not isinstance(labels, dict):
            raise ValueError("The 'labels' argument should be a dictionary.")

    # Get the unique values and their counts
    unique_values, value_counts = np.unique(data, return_counts=True)

    # Calculate the percentage for each occurrence
    total = np.sum(value_counts)
    percentages = value_counts / total * 100

    # Combine the arrays into a single array
    table_values = np.column_stack((unique_values, value_counts, percentages))

    # Define the headers for the table
    headers = ["Phase", "Count", "Fraction"]

    # Create a DataFrame
    df = pd.DataFrame(table_values, columns=headers)

    # Add the "Name" column with labels
    if labels is not None:
        df["Name"] = [labels.get(phase, "") for phase in df["Phase"]]

    # Format the columns
    df["Phase"] = df["Phase"].astype(int).astype(str)
    df["Count"] = df["Count"].astype(int).astype(str)
    df["Fraction"] = df["Fraction"].apply(lambda x: f"{x:.4f}")

    # Add the footer row to the DataFrame
    footer = [len(unique_values), np.sum(value_counts), np.sum(percentages)]
    if labels is not None:
        footer.append("")
    df_footer = pd.DataFrame([footer], columns=headers + (["Name"] if labels is not None else []))

    # Concatenate the DataFrame and footer
    df_table = pd.concat([df, df_footer], ignore_index=True)

    # Convert the DataFrame to a string format
    table = df_table.to_string(index=False)

    # Check output folder
    output_path = check_output_folder()

    if filename is not None:
        # Use the index in the filename
        filename = f"{filename}.txt"

        # Save the table to a text file with the filename
        with open(os.path.join(output_path, filename), "w") as file:
            file.write(table)
    else:
        # Find the highest existing index
        existing_files = glob.glob(os.path.join(output_path, "fraction_*.txt"))
        existing_indices = [int(os.path.basename(filename).split("_")[1].split(".")[0]) for filename in existing_files]
        highest_index = max(existing_indices) if existing_indices else 0

        # Increment the index for the new file
        new_index = highest_index + 1

        # Format the index with leading zeros using %
        index_formatted = f"{new_index:03d}"

        # Use the index in the filename
        filename = os.path.join(output_path, f"fraction_{index_formatted}.txt")

        # Save the table to a text file with the filename
        with open(filename, "w") as file:
            file.write(table)

    if log:
        print(table)

    return table


def label_binary(data, paramsfile='parameters.json'):
    """
    Label binary phases in a 3D volume based on user input.

    Parameters:
    -----------
    data : numpy.ndarray
        3D binary volume to be labeled.

    Returns:
    --------
    labels : dict
        Dictionary mapping phase values to user-defined labels.
    """
    from IPython.display import display

    # Ensure the input is a binary array (contains only integers)
    if not np.issubdtype(data.dtype, np.integer):
        raise ValueError("Input data must be a binary array containing only integers (0 or 1).")

    # Get the unique values and their counts
    unique, counts = np.unique(data, return_counts=True)

    # Create an empty labels dictionary
    labels = {}

    for m, value in enumerate(unique):
        # Create a copy of the input array and set all values to 0
        data_temp = np.zeros_like(data)

        # Set the values that match the current unique value to 1
        data_temp[data == value] = 1

        # Set the values that match the current unique value to 1
        data_temp[data == unique[m]] = 1
        fig, ax = plot_slice(data=data_temp, plane='xy', paramsfile=paramsfile, title=f"Phase: {m}")
        
        # Display the figure in the Jupyter Notebook
        display(fig)

        # Prompt the user to name the presented phase and store the input in labels
        phase_name = input(f'Name the presented phase {value} with index {m}: ')
        labels[value] = phase_name
        
        # Close the figure to avoid displaying it again
        plt.close(fig)
        
    print(labels)

    return labels