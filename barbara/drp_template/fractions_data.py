# ------------------------------------------------------------------------------------------------- #
# ------------------------------------------------------------------------------------------------- #
# This is a script to calculate the fractions of a data_normal set
# 14-04-2022
# Martin Balcewicz (Bochum University of Applied Sciences)
# website: https://rockphysics.org/people/members/martin-balcewicz
# ------------------------------------------------------------------------------------------------- #
# ------------------------------------------------------------------------------------------------- #
import numpy as np
import pandas as pd

def main():
    print('-------------------------------------------------------------------------------------------------')
    print('-------------------------------------------------------------------------------------------------')
    print('Welcome fractions calculator')
    print('developed 04/2023 by Martin Balcewicz (mail: martin.balcewicz@rockphysics.org)')
    print('-------------------------------------------------------------------------------------------------')
    print('-------------------------------------------------------------------------------------------------')
    print(' ')


import numpy as np
import pandas as pd
import glob


def get_fractions(data, labels=None, filename=None):
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

    if filename is not None:
        # Use the index in the filename
        filename = f"{filename}.txt"

        # Save the table to a text file with the filename
        with open(filename, "w") as file:
            file.write(table)
    else:
        # Find the highest existing index
        existing_files = glob.glob("fraction_*.txt")
        existing_indices = [int(filename.split("_")[1].split(".")[0]) for filename in existing_files]
        highest_index = max(existing_indices) if existing_indices else 0

        # Increment the index for the new file
        new_index = highest_index + 1

        # Use the index in the filename
        filename = f"fraction_{new_index}.txt"

        # Format the index with leading zeros using %
        index_formatted = "%03d" % new_index

        # Use the index in the filename
        filename = f"fraction_{index_formatted}.txt"

        # Save the table to a text file with the filename
        with open(filename, "w") as file:
            file.write(table)

    print(table)
    return table


# ------------------------------------------------------------------------------------------------- #


if __name__ == '__main__':
    main()


