"""
Default Parameters Module
==========================

Configuration, styling, and utility functions for the drp_template package.

This module provides:
- Parameter file I/O (read/write/validate JSON configuration files)
- Console output styling (formatted print messages)
- Matplotlib figure defaults (standard plot configurations)
- Package configuration utilities

Structure
---------
- config: Parameter file operations (read, write, validate, check_output_folder)
- styling: Print styling and matplotlib figure defaults
"""

# Parameter file operations
from .config import (
    check_output_folder,
    update_parameters_file,
    read_parameters_file,
    validate_parameters_file,
    read_package_config,
    SCHEMA_VERSION,
)

# Styling utilities
from .styling import (
    print_style,
    default_figure,
    default_data_figure,
)
