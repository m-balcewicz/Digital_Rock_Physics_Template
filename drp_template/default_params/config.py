"""
Parameter file configuration and I/O operations.

This module handles reading, writing, and validating parameters.json files
that store model metadata and configuration.
"""

import json
import os
from datetime import datetime
from importlib.metadata import version as _pkg_version, PackageNotFoundError


__all__ = [
    'check_output_folder',
    'update_parameters_file',
    'read_parameters_file',
    'validate_parameters_file',
    'read_package_config',
    'SCHEMA_VERSION'
]


# Central place to declare the schema version for parameter files written by this package
# Increment this string when you make a breaking change to the parameter file structure
SCHEMA_VERSION = "1.0"


def _get_generator_string():
    """Return a generator provenance string like 'drp_template vX.Y.Z'."""
    try:
        pkg_ver = _pkg_version('drp_template')
        return f"drp_template v{pkg_ver}"
    except PackageNotFoundError:
        return "drp_template"


def _load_parameters_schema():
    """Load the embedded JSON Schema for parameters files."""
    schema_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'schemas')
    schema_path = os.path.join(schema_dir, 'parameters.schema.json')
    if not os.path.isfile(schema_path):
        # Schema is optional at runtime; return None if not packaged
        return None
    with open(schema_path, 'r') as f:
        return json.load(f)


def _validate_parameters_dict(data):
    """Validate a dict against the parameters JSON Schema if available.

    Raises ValueError with a helpful message if validation fails.
    """
    schema = _load_parameters_schema()
    if schema is None:
        return  # No-op if schema not present
    try:
        from jsonschema import validate
        validate(instance=data, schema=schema)
    except Exception as e:
        # Re-raise as ValueError with context for callers
        raise ValueError(f"parameters.json failed schema validation: {e}")


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
    """
    Update or create a parameters JSON file with validation.
    
    This function automatically adds provenance fields (schema_version, generator,
    created_at, modified_at) and validates against the JSON Schema before writing.
    
    Parameters
    ----------
    paramsfile : str, optional
        Name of the JSON file (default: 'parameters.json')
    **kwargs : dict
        Key-value pairs to add/update in the parameters file
        
    Raises
    ------
    ValueError
        If the resulting data fails schema validation
        
    Examples
    --------
    >>> import drp_template.default_params as dp
    >>> dp.update_parameters_file('my_model.json', nx=400, ny=400, nz=400, dtype='uint8')
    
    Notes
    -----
    Provenance fields added automatically:
    - schema_version: Current schema version (e.g., "1.0")
    - generator: Tool and version that created the file
    - created_at: Set once on creation; preserved on updates
    - modified_at: Updated every write
    """
    # Check output folder
    output_path = check_output_folder()

    # Check if the file exists
    file_path = os.path.join(output_path, paramsfile)
    is_existing = os.path.isfile(file_path)
    if is_existing:
        # File exists, load existing data
        with open(file_path, 'r') as file:
            data = json.load(file)
    else:
        # File doesn't exist, create an empty dictionary
        data = {}

    # Ensure schema version exists and is not overwritten if already present
    if 'schema_version' not in data:
        data['schema_version'] = SCHEMA_VERSION

    # Provenance fields
    now_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # Set created_at only once on first creation
    if 'created_at' not in data:
        data['created_at'] = now_str
    # Always update modified_at
    data['modified_at'] = now_str
    # Generator string
    if 'generator' not in data:
        data['generator'] = _get_generator_string()

    # Update or add new parameters
    data.update(kwargs)

    # Validate prior to write (best-effort)
    try:
        _validate_parameters_dict(data)
    except ValueError as ve:
        # Surface a clear message to users
        print(f"[parameters.json validation] {ve}")
        # Re-raise to prevent writing invalid files
        raise

    # Write data back to the file
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)


def read_parameters_file(paramsfile='parameters.json', paramsvars=None):
    """
    Read specific parameters from a JSON file with automatic validation.

    Parameters
    ----------
    paramsfile : str, optional
        Name of the JSON file (default: 'parameters.json')
    paramsvars : str, list, or None, optional
        Name or list of parameter names to read. If None, returns all parameters.

    Returns
    -------
    Any
        The value of the specified parameter, a dictionary of values, or all parameters.
        
    Raises
    ------
    FileNotFoundError
        If the parameters file doesn't exist
    ValueError
        If the file fails schema validation or requested parameters are missing
        
    Examples
    --------
    Read a single parameter:
    
    >>> nz_value = dp.read_parameters_file(paramsfile='model.json', paramsvars='nz')
    >>> print(nz_value)
    400
    
    Read multiple parameters:
    
    >>> params = dp.read_parameters_file(paramsfile='model.json', 
    ...                                  paramsvars=['nx', 'ny', 'nz'])
    >>> print(params)
    [400, 400, 400]
    
    Read all parameters:
    
    >>> all_params = dp.read_parameters_file(paramsfile='model.json')
    >>> print(all_params['schema_version'])
    '1.0'
    
    Notes
    -----
    - Automatically validates the file against the JSON Schema
    - Raises clear errors if validation fails or parameters are missing
    - See drp_template/default_params/schemas/README.md for schema details
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

    # Validate on read (best-effort; raise helpful error)
    try:
        _validate_parameters_dict(data)
    except ValueError as ve:
        raise ValueError(f"Invalid parameters file '{file_path}': {ve}")

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


def validate_parameters_file(paramsfile='parameters.json'):
    """Validate a parameters JSON file against the embedded schema.

    Raises ValueError if validation fails; returns True on success.
    """
    output_path = check_output_folder()
    file_path = os.path.join(output_path, paramsfile)
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"The file '{file_path}' does not exist.")

    with open(file_path, 'r') as f:
        data = json.load(f)

    _validate_parameters_dict(data)
    return True


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
