# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os
import sys
sys.path.insert(0, os.path.abspath('..'))

# -- Project information -----------------------------------------------------
project = 'Digital Rock Physics Template'
copyright = '2025, Martin Balcewicz'
author = 'Martin Balcewicz'
release = '0.1.0-alpha'

# -- General configuration ---------------------------------------------------
extensions = [
    'sphinx.ext.autodoc',        # Auto-generate docs from docstrings
    'sphinx.ext.napoleon',       # Support for NumPy/Google style docstrings
    'sphinx.ext.viewcode',       # Add links to source code
    'sphinx.ext.intersphinx',    # Link to other project docs
    'sphinx.ext.mathjax',        # Math equations support
    'myst_parser',               # Markdown support
    'nbsphinx',                  # Jupyter notebook support
]

# nbsphinx configuration
nbsphinx_execute = 'never'  # Don't execute notebooks during build (use saved outputs)
nbsphinx_allow_errors = True  # Continue building even if notebooks have errors
nbsphinx_kernel_name = 'python3'

# Napoleon settings for NumPy-style docstrings
napoleon_google_docstring = False
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = True
napoleon_use_param = True
napoleon_use_rtype = True

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# -- Options for HTML output -------------------------------------------------
html_theme = 'sphinx_rtd_theme'  # ReadTheDocs theme (clean, professional)
html_static_path = ['_static']

# Theme options
html_theme_options = {
    'navigation_depth': 4,
    'collapse_navigation': False,
    'sticky_navigation': True,
    'includehidden': True,
}

# -- Intersphinx configuration -----------------------------------------------
intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None),
    'numpy': ('https://numpy.org/doc/stable/', None),
    'matplotlib': ('https://matplotlib.org/stable/', None),
    'pandas': ('https://pandas.pydata.org/docs/', None),
}

# -- MyST Markdown configuration ---------------------------------------------
myst_enable_extensions = [
    "dollarmath",
    "amsmath",
    "deflist",
    "html_image",
]
