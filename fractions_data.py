# ------------------------------------------------------------------------------------------------- #
# ------------------------------------------------------------------------------------------------- #
# This is a script to calculate the fractions of a data set
# 14-04-2022
# Martin Balcewicz (Bochum University of Applied Sciences)
# website: https://rockphysics.org/people/members/martin-balcewicz
# ------------------------------------------------------------------------------------------------- #
# ------------------------------------------------------------------------------------------------- #
import numpy as np
import pandas as pd
from tabulate import tabulate

from import_data import import_raw
from save_table import save_table


def main():
    print('-------------------------------------------------------------------------------------------------')
    print('-------------------------------------------------------------------------------------------------')
    print('Welcome fractions calculator')
    print('developed 04/2023 by Martin Balcewicz (mail: martin.balcewicz@rockphysics.org)')
    print('-------------------------------------------------------------------------------------------------')
    print('-------------------------------------------------------------------------------------------------')
    print(' ')


def get_fractions(data):
    # Get the unique values and their counts
    unique_values, value_counts = np.unique(data, return_counts=True)

    # Calculate the percentage for each occurrence
    total = np.sum(value_counts)
    percentages = value_counts / total * 100

    # Combine the arrays into a single array
    table_values = np.vstack((unique_values, value_counts, percentages)).T

    # Define the headers for the table
    headers = ["Phase", "Count", "Fraction"]

    # Generate the table
    df = pd.DataFrame(table_values, columns=headers)

    # Format the columns
    df["Phase"] = df["Phase"].apply(lambda x: f"{x:.0f}")
    df["Count"] = df["Count"].apply(lambda x: f"{x:.0f}")
    df["Fraction"] = df["Fraction"].apply(lambda x: f"{x:.4f}")

    # Add the footer row to the table
    footer = [np.size(unique_values), np.sum(value_counts), np.sum(percentages)]
    df_footer = pd.DataFrame([footer], columns=headers)

    # Concatenate the table and footer
    df_table = pd.concat([df, df_footer])

    # Convert the table to a string format
    table = df_table.to_string(index=False)

    return table


# ------------------------------------------------------------------------------------------------- #


if __name__ == '__main__':
    main()


