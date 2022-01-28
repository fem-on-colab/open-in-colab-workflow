# Copyright (C) 2021-2022 by the FEM on Colab authors
#
# This file is part of FEM on Colab-related actions.
#
# SPDX-License-Identifier: MIT
"""Tests for the open_in_colab_workflow.get_fem_on_colab_installation_cell_code package."""

from open_in_colab_workflow.get_fem_on_colab_installation_cell_code import get_fem_on_colab_installation_cell_code


def test_fem_on_colab_installation_cell_only_name() -> None:
    """Test generation of installation cell without any additonal version and url."""
    installation_cell_code = get_fem_on_colab_installation_cell_code("gmsh", "", "", "gmsh")
    assert installation_cell_code == """try:
    import gmsh
except ImportError:
    !wget "https://fem-on-colab.github.io/releases/gmsh-install.sh" -O "/tmp/gmsh-install.sh" && bash "/tmp/gmsh-install.sh"
    import gmsh"""  # noqa: E501


def test_fem_on_colab_installation_cell_name_and_version() -> None:
    """Test generation of installation cell with version."""
    installation_cell_code = get_fem_on_colab_installation_cell_code("firedrake", "==real", "", "firedrake")
    assert installation_cell_code == """try:
    import firedrake
except ImportError:
    !wget "https://fem-on-colab.github.io/releases/firedrake-install-real.sh" -O "/tmp/firedrake-install.sh" && bash "/tmp/firedrake-install.sh"
    import firedrake"""  # noqa: E501


def test_fem_on_colab_installation_cell_name_and_url() -> None:
    """Test generation of installation cell with url."""
    installation_cell_code = get_fem_on_colab_installation_cell_code("gmsh", "", "357e49c", "gmsh")
    assert installation_cell_code == """try:
    import gmsh
except ImportError:
    !wget "https://github.com/fem-on-colab/fem-on-colab.github.io/raw/357e49c/releases/gmsh-install.sh" -O "/tmp/gmsh-install.sh" && bash "/tmp/gmsh-install.sh"
    import gmsh"""  # noqa: E501


def test_fem_on_colab_installation_cell_name_version_and_url() -> None:
    """Test generation of installation cell with version and url."""
    installation_cell_code = get_fem_on_colab_installation_cell_code("firedrake", "==real", "357e49c", "firedrake")
    assert installation_cell_code == """try:
    import firedrake
except ImportError:
    !wget "https://github.com/fem-on-colab/fem-on-colab.github.io/raw/357e49c/releases/firedrake-install-real.sh" -O "/tmp/firedrake-install.sh" && bash "/tmp/firedrake-install.sh"
    import firedrake"""  # noqa: E501


def test_fem_on_colab_installation_cell_import_different_from_name() -> None:
    """Test generation of installation cell when package importable name is not the same as the package name."""
    installation_cell_code = get_fem_on_colab_installation_cell_code("fenics", "", "", "dolfin")
    assert installation_cell_code == """try:
    import dolfin
except ImportError:
    !wget "https://fem-on-colab.github.io/releases/fenics-install.sh" -O "/tmp/fenics-install.sh" && bash "/tmp/fenics-install.sh"
    import dolfin"""  # noqa: E501
