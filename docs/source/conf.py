# Configuration file for the Sphinx documentation builder.

# -- Project information -----------------------------------------------------
project = 'Global_Medicare_Connect_Sphinx_Documentation'
copyright = '2025, Mahtab Newaz'
author = 'Mahtab Newaz'
release = '1.0'

# -- General configuration ---------------------------------------------------
# Extensions to enable for Sphinx documentation
extensions = [
    'sphinx.ext.autodoc',  # Automatically generate documentation from docstrings
    'sphinx.ext.napoleon',  # Support for Google and NumPy style docstrings
    'sphinx.ext.viewcode',  # Allows linking to the source code
    'sphinx_autodoc_typehints',  # To include type hints in the documentation
]

# The path to the source files, typically the project root
import os
import sys
sys.path.insert(0, os.path.abspath('../..'))  
os.environ['DJANGO_SETTINGS_MODULE'] = 'global_medicare_connect.settings.py'  

# Templates path
templates_path = ['_templates']

# List of patterns to exclude from the documentation build
exclude_patterns = []

# -- Options for HTML output -------------------------------------------------
# Choose a theme for the HTML output
html_theme = 'alabaster'

# Path to static files (CSS, images, etc.)
html_static_path = ['_static']

# -- Autodoc configuration --------------------------------------------------
# Generate API documentation from docstrings in your project
autoclass_content = 'both'  # Include both class and __init__ methods in documentation
autodoc_member_order = 'bysource'  # Order members by source code order

# -- Napoleon configuration -------------------------------------------------
# Enable Napoleon for Google-style docstrings
napoleon_google_docstring = True
napoleon_numpy_docstring = True
