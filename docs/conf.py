# Copyright (C) 2021-2022 by the FEM on Colab authors
#
# This file is part of FEM on Colab-related actions.
#
# SPDX-License-Identifier: MIT
"""Open in Cloud workflow documentation configuration."""

# Project information
project = "Open in Cloud workflow"
copyright = "2021-2022, the FEM on Colab authors"
author = "Francesco Ballarin (and contributors)"

# General configuration
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode"
]

# Extensions configuration
autodoc_default_options = {
    "exclude-members": "__dict__,__init__,__module__,__weakref__",
    "imported-members": True,
    "members": True,
    "show-inheritance": True,
    "special-members": True,
    "undoc-members": True
}

# Options for HTML output
html_theme = "nature"
