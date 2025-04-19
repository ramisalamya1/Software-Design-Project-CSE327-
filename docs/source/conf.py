# Configuration file for the Sphinx documentation builder.

# -- Project information -----------------------------------------------------
project = 'Secure_Payment_Feature'
copyright = '2025, Mahtab Newaz'
author = 'Mahtab Newaz'
release = '1.0'

# -- General configuration ---------------------------------------------------
extensions = [
    'sphinx.ext.autodoc',    # Automatically generate documentation from docstrings
    'sphinx.ext.napoleon',   # Support for Google and NumPy style docstrings
    'sphinx.ext.viewcode',   # Add links to the source code
]
import os
import sys
sys.path.insert(0, os.path.abspath('../..'))  # Adjust the path if needed

templates_path = ['_templates']
exclude_patterns = []

# -- Options for HTML output -------------------------------------------------
html_theme = 'sphinx_rtd_theme'  # Modern theme
html_static_path = ['_static']  # Static files for custom styles or images
# Optional logo and favicon:
# html_logo = "_static/logo.png"
# html_favicon = "_static/favicon.ico"
