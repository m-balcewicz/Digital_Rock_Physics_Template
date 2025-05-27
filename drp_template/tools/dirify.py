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

def check_output_folder():
    """
    Check if the 'output' folder exists in the current directory.
    If not, create the folder and save a README.md file.

    Returns:
    str: Full path to the 'output' folder.
    """
    output_folder = 'output'

    # Check if the 'output' folder exists, create if not
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

        # Get the path to the directory containing the module
        module_dir = os.path.dirname(os.path.abspath(__file__))

        # Create README.md file with information from JSON file
        readme_json_path = os.path.join(module_dir, 'readme_output.json')
        with open(readme_json_path, 'r') as readme_json_file:
            readme_content = json.load(readme_json_file)

        readme_md_path = os.path.join(output_folder, 'README.md')
        with open(readme_md_path, 'w') as readme_file:
            readme_file.write(readme_content['readme_content'])

    # Return the full path to the 'output' folder
    return os.path.abspath(output_folder)