# Copyright (C) 2021-2022 by the FEM on Colab authors
#
# This file is part of FEM on Colab-related actions.
#
# SPDX-License-Identifier: MIT
"""Tests for the open_in_colab_workflow.glob_notebooks package."""

import os

from open_in_colab_workflow import glob_notebooks


def test_glob_notebooks(root_directory: str) -> None:
    """Test pattern matching while listing notebooks in a directory."""
    nb_directory = os.path.join(root_directory, "tests", "data")
    nb_pattern = os.path.join("replace_images_in_markdown", "*.ipynb")
    nbs = glob_notebooks(nb_directory, nb_pattern)
    assert nbs == {
        os.path.join(nb_directory, nb_pattern).replace("*", nb_name) for nb_name in (
            "html_and_markdown_images", "html_image", "markdown_image")}
