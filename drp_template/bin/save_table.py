# ------------------------------------------------------------------------------------------------- #
# ------------------------------------------------------------------------------------------------- #
# This is a script to save tables as .txt files
# 17-04-2022
# Martin Balcewicz (Bochum University of Applied Sciences)
# website: https://rockphysics.org/people/members/martin-balcewicz
# ------------------------------------------------------------------------------------------------- #
# ------------------------------------------------------------------------------------------------- #
import os

def main():
    print('-------------------------------------------------------------------------------------------------')
    print('-------------------------------------------------------------------------------------------------')
    print('Welcome table extraction')
    print('developed 04/2023 by Martin Balcewicz (mail: martin.balcewicz@rockphysics.org)')
    print('-------------------------------------------------------------------------------------------------')
    print('-------------------------------------------------------------------------------------------------')
    print(' ')


def save_table(table, varname='table', path=None):

    if path is not None:
        # Construct the filename with the counter variable and folder path
        filename = os.path.join(path, f"{varname}.txt")
    else:
        # create figures directory if it doesn't exist
        if not os.path.exists('tables'):
            os.makedirs('tables')
        filename = os.path.join("tables", f"{varname}.txt")

    # Write the table to the txt file with the increasing number in the filename
    with open(filename, "w") as f:
        f.write(table)

    print(f'table {varname} saved as {filename}')

    return

# ------------------------------------------------------------------------------------------------- #


if __name__ == '__main__':
    main()