# Copyright (C) 2021-2023 by the FEM on Colab authors
#
# This file is part of FEM on Colab-related actions.
#
# SPDX-License-Identifier: MIT
"""Tests for the open_in_cloud_workflow.get_pip_installation_cell_code package."""

from open_in_cloud_workflow.get_pip_installation_cell_code import get_pip_installation_cell_code


def test_pip_installation_cell_only_name() -> None:
    """Test generation of installation cell without any additonal version and url."""
    installation_cell_code = get_pip_installation_cell_code("numpy", "", "", "numpy", "")
    assert installation_cell_code == """try:
    import numpy
except ImportError:
    !pip3 install numpy
    import numpy"""


def test_pip_installation_cell_name_and_version() -> None:
    """Test generation of installation cell with a version and without an url."""
    installation_cell_code = get_pip_installation_cell_code("numpy", ">=1.21.0", "", "numpy", "")
    assert installation_cell_code == '!pip3 install --upgrade "numpy>=1.21.0"'


def test_pip_installation_cell_name_and_extras() -> None:
    """Test generation of installation cell with extras and without an url."""
    installation_cell_code = get_pip_installation_cell_code("jax", "[cpu]", "", "jax", "")
    assert installation_cell_code == """try:
    import jax
except ImportError:
    !pip3 install jax[cpu]
    import jax"""


def test_pip_installation_cell_import_different_from_name() -> None:
    """Test generation of installation cell when package importable name is not the same as the package name."""
    installation_cell_code = get_pip_installation_cell_code("python-dateutil", "", "", "dateutil", "")
    assert installation_cell_code == """try:
    import dateutil
except ImportError:
    !pip3 install python-dateutil
    import dateutil"""


def test_pip_installation_cell_multiple_packages() -> None:
    """Test generation of installation cell when a package requires the custom widget manager to be enabled."""
    installation_cell_code = get_pip_installation_cell_code("itkwidgets pyvista", "", "", "pyvista", "")
    assert installation_cell_code == """try:
    import pyvista
except ImportError:
    !pip3 install itkwidgets pyvista
    import pyvista"""


def test_pip_installation_cell_name_and_command_line_options() -> None:
    """Test generation of installation cell with command line options."""
    installation_cell_code = get_pip_installation_cell_code("numpy", "", "", "numpy", '--no-binary="numpy"')
    assert installation_cell_code == """try:
    import numpy
except ImportError:
    !pip3 install --no-binary="numpy" numpy
    import numpy"""


def test_pip_installation_cell_name_and_version_and_command_line_options() -> None:
    """Test generation of installation cell with a version and command line options."""
    installation_cell_code = get_pip_installation_cell_code("numpy", ">=1.21.0", "", "numpy", '--no-binary="numpy"')
    assert installation_cell_code == '!pip3 install --upgrade --no-binary="numpy" "numpy>=1.21.0"'


def test_pip_installation_cell_name_and_and_empty_package_import_and_command_line_options() -> None:
    """Test generation of installation cell with command line options."""
    installation_cell_code = get_pip_installation_cell_code("numpy", "", "", "", '--no-binary="numpy"')
    assert installation_cell_code == '!pip3 install --no-binary="numpy" numpy'
