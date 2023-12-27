import json
import os
from datetime import datetime


__all__ = [
    'print_style',
    'check_output_folder',
    'update_parameters_file',
    'read_parameters_file'
]


def print_style(message, style='indented_separator'):
    """Print the given message with a specified style."""
    if style == 'box':
        style_chars = '#'
    elif style == 'section':
        style_chars = '='
    elif style == 'decorative':
        style_chars = '*'
    elif style == 'indented_separator':
        style_chars = '-'
    else:
        # Default to a simple line separator
        style_chars = '-'

    lines = message.split('\n')  # Split the multiline message into lines

    max_line_length = max(len(line) for line in lines)

    print(f"{style_chars * max_line_length}")
    for line in lines:
        # Pad shorter lines with spaces to match the maximum length
        print(f"{line.ljust(max_line_length)}")
    print(f"{style_chars * max_line_length}")


def check_output_folder():
    """
    Check if the 'output' folder exists in the current directory.
    If not, create the folder.

    Returns:
    str: Full path to the 'output' folder.
    """
    output_folder = 'output'

    # Check if the 'output' folder exists, create if not
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Return the full path to the 'output' folder
    return os.path.abspath(output_folder)


def update_parameters_file(paramsfile='parameters.json', **kwargs):
    # Check output folder
    output_path = check_output_folder()

    # Check if the file exists
    file_path = os.path.join(output_path, paramsfile)
    if os.path.isfile(file_path):
        # File exists, load existing data
        with open(file_path, 'r') as file:
            data = json.load(file)
    else:
        # File doesn't exist, create an empty dictionary
        data = {}

    # Update timestamp
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    data['timestamp'] = timestamp

    # Update or add new parameters
    data.update(kwargs)

    # Write data back to the file
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)


def read_parameters_file(paramsfile='parameters.json', paramsvars=None):
    """
    Read specific parameters from a JSON file.

    Parameters:
    -----------
    paramsfile : str (optional)
        Name of the JSON file. Default is 'parameters.json'.
    paramsvars : str, list, or None (optional)
        Name or list of variables of parameters to read from the file. If None, all parameters are read.

    Returns:
    Any
        The value of the specified parameter or a dictionary of parameter values.
    ```
    Example usage
    nz_value = read_parameters_file(paramsfile='parameters.json', paramsvars='nz')
    print(nz_value)

    Or with a list of parameter names
    params_values = read_parameters_file(paramsfile='parameters.json', paramsvars=['nx', 'ny', 'nz'])
    print(params_values)
    ```
    """
    # Check output folder
    output_path = check_output_folder()

    # Check if the file exists
    file_path = os.path.join(output_path, paramsfile)
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"The file '{file_path}' does not exist.")

    # File exists, load existing data
    with open(file_path, 'r') as file:
        data = json.load(file)

    # If specific parameter names are provided, get the values
    if paramsvars:
        if isinstance(paramsvars, str):
            # If a single parameter name is provided, return its value
            return data.get(paramsvars)
        elif isinstance(paramsvars, list):
            # If a list of parameter names is provided, return a dictionary of values
            read_parameters = {param: data.get(param) for param in paramsvars}
            missing_parameters = [param for param in paramsvars if param not in data]

            if missing_parameters:
                raise ValueError(f"Parameters not found: {', '.join(missing_parameters)}")
            else:
                return list(read_parameters.values())[0] if len(read_parameters) == 1 else read_parameters
        else:
            raise ValueError("Invalid type for parameter_names. Use str, list, or None.")
    else:
        return data

