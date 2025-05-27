import os


def mk_dir(path):
    """
    Create a directory if it doesn't exist.

    Parameters:
    - path (str): The path of the directory to be created.

    Returns:
    - bool: True if the directory was created or already exists, False otherwise.
    """
    try:
        # Check if the directory exists
        if not os.path.exists(path):
            # Create the directory if it doesn't exist
            os.makedirs(path)
            print(f"Directory created: {path}")

        return path
    except Exception as e:
        print(f"Error creating directory: {e}")
        return ''

def check_output_folder(output_folder='output'):
    """
    Ensure the output folder exists and return its absolute path.
    Default is a folder named 'output' in the current working directory.
    """
    abs_path = os.path.abspath(output_folder)
    if not os.path.exists(abs_path):
        os.makedirs(abs_path)
        print(f"Created output folder: {abs_path}")
    return abs_path