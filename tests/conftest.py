# Copyright (C) 2021-2022 by the FEM on Colab authors
#
# This file is part of FEM on Colab-related actions.
#
# SPDX-License-Identifier: MIT
"""Definition of common fixtures."""

import os
import typing

import nbformat
import pytest


@pytest.fixture
def root_directory() -> str:
    """Return the root directory of the repository."""
    return os.path.dirname(os.path.dirname(__file__))


@pytest.fixture
def open_notebook(root_directory: str) -> typing.Callable:
    """Return a fixture to open a local notebook."""
    def _(local_directory: str, filename: str) -> nbformat.NotebookNode:
        """Open notebook with nbformat."""
        filename = os.path.join(root_directory, "tests", "data", local_directory, filename + ".ipynb")
        with open(filename, "r") as f:
            nb = nbformat.read(f, as_version=4)
        nb._filename = filename
        return nb
    return _
