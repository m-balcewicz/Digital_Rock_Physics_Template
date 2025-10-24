import json
import os
from datetime import datetime
import matplotlib.pyplot as plt
from cmcrameri import cm


__all__ = [
    'print_style',
    'check_output_folder',
    'update_parameters_file',
    'read_parameters_file',
    'read_package_config',
    'default_figure',
    'default_data_figure'
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


def read_package_config(config_filename):
    """
    Read a configuration file from the package directory (not from output folder).
    
    This is for reading package-internal configuration files like default_figure_settings.json,
    not user data files.
    
    Parameters:
    -----------
    config_filename : str
        Name of the configuration file to read from the package.
        
    Returns:
    --------
    dict
        The configuration data as a dictionary.
        
    Example:
    --------
    >>> settings = read_package_config('default_figure_settings.json')
    """
    # Get the directory where this module is located
    module_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Construct the full path to the config file
    config_path = os.path.join(module_dir, config_filename)
    
    if not os.path.isfile(config_path):
        raise FileNotFoundError(f"Package configuration file '{config_path}' does not exist.")
    
    # Read and return the configuration
    with open(config_path, 'r') as f:
        return json.load(f)


# Matplotlib figure defaults
# Colormap after: Crameri, Fabio: Scientific colour maps, https://zenodo.org/record/1243862, (2021)

def default_figure():
    """
    Set default matplotlib figure parameters for standard plots.
    
    Sets figure size, background color, subplot positions, and font size.
    """
    # set the default figure size
    plt.rcParams['figure.figsize'] = (10, 6)

    # set the background color of the figure
    plt.rcParams['figure.facecolor'] = 'white'

    # set the default x-axes position
    plt.rcParams['figure.subplot.left'] = 0.15          # left
    plt.rcParams['figure.subplot.bottom'] = 0.11        # bottom
    plt.rcParams['figure.subplot.right'] = 0.75         # width
    plt.rcParams['figure.subplot.top'] = 0.8            # height

    # set the font size
    plt.rcParams['font.size'] = 20


def default_data_figure():
    """
    Set default matplotlib figure parameters for data visualization plots.
    
    Sets figure size, background color, subplot positions, and font size.
    Slightly larger than default_figure for data-heavy plots.
    """
    # set the default figure size
    plt.rcParams['figure.figsize'] = (12, 7)

    # set the background color of the figure
    plt.rcParams['figure.facecolor'] = 'white'

    # set the default x-axes position
    plt.rcParams['figure.subplot.left'] = 0.15          # left
    plt.rcParams['figure.subplot.bottom'] = 0.11        # bottom
    plt.rcParams['figure.subplot.right'] = 0.75         # width

    # set the font size
    plt.rcParams['font.size'] = 20

