# Copyright (C) 2021-2022 by the FEM on Colab authors
#
# This file is part of FEM on Colab-related actions.
#
# SPDX-License-Identifier: MIT
"""Tests for the open_in_colab_workflow.add_installation_cells package."""

import os
import typing

import nbformat
import pytest

from open_in_colab_workflow import add_installation_cells


@pytest.fixture
def root_directory() -> str:
    """Return the root directory of the repository."""
    return os.path.dirname(os.path.dirname(__file__))


@pytest.fixture
def open_notebook(root_directory: str) -> typing.Callable:
    """Return a fixture to open a local notebook."""
    def _(filename: str) -> nbformat.NotebookNode:
        """Open notebook with nbformat."""
        with open(os.path.join(
                root_directory, "tests", "data", "add_installation_cells", filename + ".ipynb"), "r") as f:
            return nbformat.read(f, as_version=4)
    return _


@pytest.mark.parametrize(
    "fem_on_colab_packages_str,pip_packages_str",
    [
        ("", "numpy"),
        ("", "numpy\nscipy"),
        ("mpi4py", "numpy"),
        ("mpi4py", "numpy\nscipy")
    ]
)
def test_add_installation_cells_single_pip_package(
    fem_on_colab_packages_str: str, pip_packages_str: str, open_notebook: typing.Callable
) -> None:
    """Test addition of installation cells with a single pip package, possibly providing unused packages."""
    nb = open_notebook("import_numpy")
    assert len(nb.cells) == 1
    updated_cells, new_cells_position = add_installation_cells(nb.cells, fem_on_colab_packages_str, pip_packages_str)
    assert len(updated_cells) == 2
    assert updated_cells[0].cell_type == "code"
    assert updated_cells[0].source == """try:
    import numpy
except ImportError:
    !pip3 install numpy
    import numpy"""
    assert updated_cells[1] == nb.cells[0]
    assert len(new_cells_position) == 1
    assert new_cells_position[0] == 0


@pytest.mark.parametrize(
    "fem_on_colab_packages_str,pip_packages_str",
    [
        ("mpi4py", ""),
        ("mpi4py\nh5py", ""),
        ("mpi4py", "numpy"),
        ("mpi4py\nh5py", "numpy")
    ]
)
def test_add_installation_cells_single_fem_on_colab_package(
    fem_on_colab_packages_str: str, pip_packages_str: str, open_notebook: typing.Callable
) -> None:
    """Test addition of installation cells with a single FEM on Colab package, possibly providing unused packages."""
    nb = open_notebook("import_mpi4py")
    assert len(nb.cells) == 1
    updated_cells, new_cells_position = add_installation_cells(nb.cells, fem_on_colab_packages_str, pip_packages_str)
    assert len(updated_cells) == 2
    assert updated_cells[0].cell_type == "code"
    assert updated_cells[0].source == """try:
    import mpi4py
except ImportError:
    !wget "https://fem-on-colab.github.io/releases/mpi4py-install.sh" -O "/tmp/mpi4py-install.sh" && bash "/tmp/mpi4py-install.sh"
    import mpi4py"""  # noqa: E501
    assert updated_cells[1] == nb.cells[0]
    assert len(new_cells_position) == 1
    assert new_cells_position[0] == 0


@pytest.mark.parametrize(
    "fem_on_colab_packages_str,pip_packages_str",
    [
        ("mpi4py", "numpy"),
        ("mpi4py", "numpy\nscipy"),
        ("mpi4py\nh5py", "numpy"),
        ("mpi4py\nh5py", "numpy\nscipy")
    ]
)
def test_add_installation_cells_mix_pip_package_and_fem_on_colab_package(
    fem_on_colab_packages_str: str, pip_packages_str: str, open_notebook: typing.Callable
) -> None:
    """Test addition of installation cells with both pip and FEM on Colab packages."""
    nb = open_notebook("import_mpi4py_numpy")
    assert len(nb.cells) == 1
    updated_cells, new_cells_position = add_installation_cells(nb.cells, fem_on_colab_packages_str, pip_packages_str)
    assert len(updated_cells) == 3
    assert updated_cells[0].cell_type == "code"
    assert updated_cells[0].source == """try:
    import mpi4py
except ImportError:
    !wget "https://fem-on-colab.github.io/releases/mpi4py-install.sh" -O "/tmp/mpi4py-install.sh" && bash "/tmp/mpi4py-install.sh"
    import mpi4py"""  # noqa: E501
    assert updated_cells[1].cell_type == "code"
    assert updated_cells[1].source == """try:
    import numpy
except ImportError:
    !pip3 install numpy
    import numpy"""
    assert updated_cells[2] == nb.cells[0]
    assert len(new_cells_position) == 2
    assert new_cells_position[0] == 0
    assert new_cells_position[1] == 1


def test_add_installation_cells_from_form(open_notebook: typing.Callable) -> None:
    """Test addition of installation cells when the from form of the import is used."""
    nb = open_notebook("from_numpy_import")
    assert len(nb.cells) == 1
    updated_cells, new_cells_position = add_installation_cells(nb.cells, "", "numpy")
    assert len(updated_cells) == 2
    assert updated_cells[0].cell_type == "code"
    assert updated_cells[0].source == """try:
    import numpy
except ImportError:
    !pip3 install numpy
    import numpy"""
    assert updated_cells[1] == nb.cells[0]
    assert len(new_cells_position) == 1
    assert new_cells_position[0] == 0


def test_add_installation_cells_multiple_pip_packages(open_notebook: typing.Callable) -> None:
    """Test that addition of installation cells preserves the order in which the packages are provided."""
    nb = open_notebook("import_numpy_scipy")
    assert len(nb.cells) == 1
    updated_cells, new_cells_position = add_installation_cells(nb.cells, "", "scipy\nnumpy")
    assert len(updated_cells) == 3
    assert updated_cells[0].cell_type == "code"
    assert updated_cells[0].source == """try:
    import scipy
except ImportError:
    !pip3 install scipy
    import scipy"""
    assert updated_cells[1].cell_type == "code"
    assert updated_cells[1].source == """try:
    import numpy
except ImportError:
    !pip3 install numpy
    import numpy"""
    assert updated_cells[2] == nb.cells[0]
    assert len(new_cells_position) == 2
    assert new_cells_position[0] == 0
    assert new_cells_position[1] == 1


def test_add_installation_cells_markdown(open_notebook: typing.Callable) -> None:
    """Test that the installation cells are placed after markdown cells."""
    nb = open_notebook("import_numpy_markdown")
    assert len(nb.cells) == 2
    updated_cells, new_cells_position = add_installation_cells(nb.cells, "", "numpy")
    assert len(updated_cells) == 3
    assert updated_cells[0] == nb.cells[0]
    assert updated_cells[1].cell_type == "code"
    assert updated_cells[1].source == """try:
    import numpy
except ImportError:
    !pip3 install numpy
    import numpy"""
    assert updated_cells[2] == nb.cells[1]
    assert len(new_cells_position) == 1
    assert new_cells_position[0] == 1
