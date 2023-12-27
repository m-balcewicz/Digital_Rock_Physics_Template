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
