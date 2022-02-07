# Copyright (C) 2021-2022 by the FEM on Colab authors
#
# This file is part of FEM on Colab-related actions.
#
# SPDX-License-Identifier: MIT
"""Tests for the open_in_colab_workflow.add_installation_cells package."""

import os
import shutil
import tempfile
import typing

import nbformat
import pytest

from open_in_colab_workflow.add_installation_cells import (
    __main__ as add_installation_cells_main, add_installation_cells)


@pytest.mark.parametrize(
    "fem_on_colab_packages_str,pip_packages_str",
    [
        ("", "numpy"),
        ("", "numpy\nscipy"),
        ("mpi4py", "numpy"),
        ("mpi4py", "numpy\nscipy")
    ]
)
def test_add_installation_cells_single_pip_package(  # type: ignore[no-any-unimported]
    fem_on_colab_packages_str: str, pip_packages_str: str,
    open_notebook: typing.Callable[[str, str], nbformat.NotebookNode]
) -> None:
    """Test addition of installation cells with a single pip package, possibly providing unused packages."""
    nb = open_notebook("add_installation_cells", "import_numpy")
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
def test_add_installation_cells_single_fem_on_colab_package(  # type: ignore[no-any-unimported]
    fem_on_colab_packages_str: str, pip_packages_str: str,
    open_notebook: typing.Callable[[str, str], nbformat.NotebookNode]
) -> None:
    """Test addition of installation cells with a single FEM on Colab package, possibly providing unused packages."""
    nb = open_notebook("add_installation_cells", "import_mpi4py")
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
def test_add_installation_cells_mix_pip_package_and_fem_on_colab_package(  # type: ignore[no-any-unimported]
    fem_on_colab_packages_str: str, pip_packages_str: str,
    open_notebook: typing.Callable[[str, str], nbformat.NotebookNode]
) -> None:
    """Test addition of installation cells with both pip and FEM on Colab packages."""
    nb = open_notebook("add_installation_cells", "import_mpi4py_numpy")
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


def test_add_installation_cells_from_form(  # type: ignore[no-any-unimported]
    open_notebook: typing.Callable[[str, str], nbformat.NotebookNode]
) -> None:
    """Test addition of installation cells when the from form of the import is used."""
    nb = open_notebook("add_installation_cells", "from_numpy_import")
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


def test_add_installation_cells_import_name(  # type: ignore[no-any-unimported]
    open_notebook: typing.Callable[[str, str], nbformat.NotebookNode]
) -> None:
    """Test addition of installation cells with non-default import name."""
    nb = open_notebook("add_installation_cells", "import_dateutil")
    assert len(nb.cells) == 1
    updated_cells, new_cells_position = add_installation_cells(nb.cells, "", "python-dateutil$dateutil")
    assert len(updated_cells) == 2
    assert updated_cells[0].cell_type == "code"
    assert updated_cells[0].source == """try:
    import dateutil
except ImportError:
    !pip3 install python-dateutil
    import dateutil"""
    assert updated_cells[1] == nb.cells[0]
    assert len(new_cells_position) == 1
    assert new_cells_position[0] == 0


def test_add_installation_cells_dependent_imports(  # type: ignore[no-any-unimported]
    open_notebook: typing.Callable[[str, str], nbformat.NotebookNode]
) -> None:
    """Test addition of installation cells with dependent imports."""
    nb = open_notebook("add_installation_cells", "import_plotly")
    assert len(nb.cells) == 1
    updated_cells, new_cells_position = add_installation_cells(nb.cells, "", "kaleido%plotly")
    assert len(updated_cells) == 2
    assert updated_cells[0].cell_type == "code"
    assert updated_cells[0].source == """try:
    import kaleido
except ImportError:
    !pip3 install kaleido
    import kaleido"""
    assert updated_cells[1] == nb.cells[0]
    assert len(new_cells_position) == 1
    assert new_cells_position[0] == 0


def test_add_installation_cells_multiple_pip_packages(  # type: ignore[no-any-unimported]
    open_notebook: typing.Callable[[str, str], nbformat.NotebookNode]
) -> None:
    """Test that addition of installation cells preserves the order in which the packages are provided."""
    nb = open_notebook("add_installation_cells", "import_numpy_scipy")
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


def test_add_installation_cells_markdown(  # type: ignore[no-any-unimported]
    open_notebook: typing.Callable[[str, str], nbformat.NotebookNode]
) -> None:
    """Test that the installation cells are placed after markdown cells."""
    nb = open_notebook("add_installation_cells", "import_numpy_markdown")
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


def test_add_installation_cells_main_single_pip_package(  # type: ignore[no-any-unimported]
    root_directory: str, open_notebook: typing.Callable[[str, str, str], nbformat.NotebookNode]
) -> None:
    """Test addition of installation cells with a single pip package when running the module as a script."""
    data_directory = os.path.join(root_directory, "tests", "data")
    nb_pattern = os.path.join("add_installation_cells", "import_numpy.ipynb")
    fem_on_colab_packages = ""
    pip_packages = "numpy"

    with tempfile.TemporaryDirectory(dir=data_directory) as tmp_data_directory:
        os.mkdir(os.path.dirname(os.path.join(tmp_data_directory, nb_pattern)))
        shutil.copyfile(os.path.join(data_directory, nb_pattern), os.path.join(tmp_data_directory, nb_pattern))
        add_installation_cells_main(tmp_data_directory, nb_pattern, fem_on_colab_packages, pip_packages)

        nb = open_notebook(
            os.path.dirname(nb_pattern), os.path.basename(nb_pattern).replace(".ipynb", ""), data_directory)
        updated_nb = open_notebook(
            os.path.dirname(nb_pattern), os.path.basename(nb_pattern).replace(".ipynb", ""), tmp_data_directory)
        assert len(updated_nb.cells) == 2
        assert updated_nb.cells[0].cell_type == "code"
        assert updated_nb.cells[0].source == """try:
    import numpy
except ImportError:
    !pip3 install numpy
    import numpy"""
        assert updated_nb.cells[1] == nb.cells[0]


def test_add_installation_cells_main_single_fem_on_colab_package(  # type: ignore[no-any-unimported]
    root_directory: str, open_notebook: typing.Callable[[str, str, str], nbformat.NotebookNode]
) -> None:
    """Test addition of installation cells with a single FEM on Colab package when running the module as a script."""
    data_directory = os.path.join(root_directory, "tests", "data")
    nb_pattern = os.path.join("add_installation_cells", "import_mpi4py.ipynb")
    fem_on_colab_packages = "mpi4py"
    pip_packages = ""

    with tempfile.TemporaryDirectory(dir=data_directory) as tmp_data_directory:
        os.mkdir(os.path.dirname(os.path.join(tmp_data_directory, nb_pattern)))
        shutil.copyfile(os.path.join(data_directory, nb_pattern), os.path.join(tmp_data_directory, nb_pattern))
        add_installation_cells_main(tmp_data_directory, nb_pattern, fem_on_colab_packages, pip_packages)

        nb = open_notebook(
            os.path.dirname(nb_pattern), os.path.basename(nb_pattern).replace(".ipynb", ""), data_directory)
        updated_nb = open_notebook(
            os.path.dirname(nb_pattern), os.path.basename(nb_pattern).replace(".ipynb", ""), tmp_data_directory)
        assert len(updated_nb.cells) == 2
        assert updated_nb.cells[0].cell_type == "code"
        assert updated_nb.cells[0].source == """try:
    import mpi4py
except ImportError:
    !wget "https://fem-on-colab.github.io/releases/mpi4py-install.sh" -O "/tmp/mpi4py-install.sh" && bash "/tmp/mpi4py-install.sh"
    import mpi4py"""  # noqa: E501
        assert updated_nb.cells[1] == nb.cells[0]


def test_add_installation_cells_main_import_name(  # type: ignore[no-any-unimported]
    root_directory: str, open_notebook: typing.Callable[[str, str, str], nbformat.NotebookNode]
) -> None:
    """Test addition of installation cells with non-default import name when running the module as a script."""
    data_directory = os.path.join(root_directory, "tests", "data")
    nb_pattern = os.path.join("add_installation_cells", "import_dateutil.ipynb")
    fem_on_colab_packages = ""
    pip_packages = "python-dateutil$dateutil"

    with tempfile.TemporaryDirectory(dir=data_directory) as tmp_data_directory:
        os.mkdir(os.path.dirname(os.path.join(tmp_data_directory, nb_pattern)))
        shutil.copyfile(os.path.join(data_directory, nb_pattern), os.path.join(tmp_data_directory, nb_pattern))
        add_installation_cells_main(tmp_data_directory, nb_pattern, fem_on_colab_packages, pip_packages)

        nb = open_notebook(
            os.path.dirname(nb_pattern), os.path.basename(nb_pattern).replace(".ipynb", ""), data_directory)
        updated_nb = open_notebook(
            os.path.dirname(nb_pattern), os.path.basename(nb_pattern).replace(".ipynb", ""), tmp_data_directory)
        assert len(updated_nb.cells) == 2
        assert updated_nb.cells[0].cell_type == "code"
        assert updated_nb.cells[0].source == """try:
    import dateutil
except ImportError:
    !pip3 install python-dateutil
    import dateutil"""
        assert updated_nb.cells[1] == nb.cells[0]


def test_add_installation_cells_main_dependent_imports(  # type: ignore[no-any-unimported]
    root_directory: str, open_notebook: typing.Callable[[str, str, str], nbformat.NotebookNode]
) -> None:
    """Test addition of installation cells with dependent imports when running the module as a script."""
    data_directory = os.path.join(root_directory, "tests", "data")
    nb_pattern = os.path.join("add_installation_cells", "import_plotly.ipynb")
    fem_on_colab_packages = ""
    pip_packages = "kaleido%plotly"

    with tempfile.TemporaryDirectory(dir=data_directory) as tmp_data_directory:
        os.mkdir(os.path.dirname(os.path.join(tmp_data_directory, nb_pattern)))
        shutil.copyfile(os.path.join(data_directory, nb_pattern), os.path.join(tmp_data_directory, nb_pattern))
        add_installation_cells_main(tmp_data_directory, nb_pattern, fem_on_colab_packages, pip_packages)

        nb = open_notebook(
            os.path.dirname(nb_pattern), os.path.basename(nb_pattern).replace(".ipynb", ""), data_directory)
        updated_nb = open_notebook(
            os.path.dirname(nb_pattern), os.path.basename(nb_pattern).replace(".ipynb", ""), tmp_data_directory)
        assert len(updated_nb.cells) == 2
        assert updated_nb.cells[0].cell_type == "code"
        assert updated_nb.cells[0].source == """try:
    import kaleido
except ImportError:
    !pip3 install kaleido
    import kaleido"""
        assert updated_nb.cells[1] == nb.cells[0]
