# Copyright (C) 2021-2022 by the FEM on Colab authors
#
# This file is part of FEM on Colab-related actions.
#
# SPDX-License-Identifier: MIT
"""Open in Colab workflow main module."""

from open_in_colab_workflow.add_installation_cells import add_installation_cells
from open_in_colab_workflow.get_fem_on_colab_installation_cell_code import get_fem_on_colab_installation_cell_code
from open_in_colab_workflow.get_pip_installation_cell_code import get_pip_installation_cell_code
from open_in_colab_workflow.get_pip_installation_line import get_pip_installation_line
from open_in_colab_workflow.glob_images import glob_images
from open_in_colab_workflow.glob_notebooks import glob_notebooks
from open_in_colab_workflow.packages_str_to_lists import packages_str_to_lists
from open_in_colab_workflow.replace_images_in_markdown import replace_images_in_markdown
