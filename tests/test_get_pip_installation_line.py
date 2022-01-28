# Copyright (C) 2021-2022 by the FEM on Colab authors
#
# This file is part of FEM on Colab-related actions.
#
# SPDX-License-Identifier: MIT
"""Tests for the open_in_colab_workflow.get_pip_installation_line package."""

from open_in_colab_workflow.get_pip_installation_line import get_pip_installation_line


def test_pip_installation_line_only_name() -> None:
    """Test generation of installation line without any additonal version and url."""
    installation_line = get_pip_installation_line("numpy", "", "")
    assert installation_line == "pip3 install numpy"


def test_pip_installation_line_name_and_version() -> None:
    """Test generation of installation line with version."""
    installation_line = get_pip_installation_line("numpy", ">=1.21.0,<1.22.0", "")
    assert installation_line == "pip3 install --upgrade numpy>=1.21.0,<1.22.0"


def test_pip_installation_line_name_and_url() -> None:
    """Test generation of installation line with url."""
    installation_line = get_pip_installation_line("numpy", "", "https://github.com/numpy/numpy.git")
    assert installation_line == 'pip3 install "numpy@git+https://github.com/numpy/numpy.git"'


def test_pip_installation_line_multiple_packages() -> None:
    """Test generation of installation line when two packages are provided."""
    installation_line = get_pip_installation_line("itkwidgets pyvista", "", "")
    assert installation_line == "pip3 install itkwidgets pyvista"
