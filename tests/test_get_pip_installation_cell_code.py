# Copyright (C) 2021-2026 by the FEM on Colab authors
#
# This file is part of FEM on Colab-related actions.
#
# SPDX-License-Identifier: MIT
"""Tests for the open_in_cloud_workflow.get_pip_installation_cell_code package."""  # noqa: E501, W505

from open_in_cloud_workflow.get_pip_installation_cell_code import (
    get_pip_installation_cell_code,
)


def test_pip_installation_cell_only_name() -> None:
    """Test installation cell generation without version or URL."""
    installation_cell_code = get_pip_installation_cell_code(
        "numpy", "", "", "numpy", "", ""
    )
    assert (
        installation_cell_code
        == """try:
    import numpy
except ImportError:
    !python3 -m pip install numpy
    import numpy"""
    )


def test_pip_installation_cell_name_and_version() -> None:
    """Test installation cell generation with version and no URL."""
    installation_cell_code = get_pip_installation_cell_code(
        "numpy", ">=1.21.0", "", "numpy", "", ""
    )
    assert (
        installation_cell_code
        == '!python3 -m pip install --upgrade "numpy>=1.21.0"'
    )


def test_pip_installation_cell_name_and_extras() -> None:
    """Test generation of installation cell with extras and without an url."""
    installation_cell_code = get_pip_installation_cell_code(
        "jax", "[cpu]", "", "jax", "", ""
    )
    assert (
        installation_cell_code
        == """try:
    import jax
except ImportError:
    !python3 -m pip install jax[cpu]
    import jax"""
    )


def test_pip_installation_cell_import_different_from_name() -> None:
    """Test installation cell when import name differs from package name."""
    installation_cell_code = get_pip_installation_cell_code(
        "python-dateutil", "", "", "dateutil", "", ""
    )
    assert (
        installation_cell_code
        == """try:
    import dateutil
except ImportError:
    !python3 -m pip install python-dateutil
    import dateutil"""
    )


def test_pip_installation_cell_multiple_packages() -> None:
    """Test installation cell for packages requiring widget manager setup."""
    installation_cell_code = get_pip_installation_cell_code(
        "itkwidgets pyvista", "", "", "pyvista", "", ""
    )
    assert (
        installation_cell_code
        == """try:
    import pyvista
except ImportError:
    !python3 -m pip install itkwidgets pyvista
    import pyvista"""
    )


def test_pip_installation_cell_name_and_command_line_options() -> None:
    """Test generation of installation cell with command line options."""
    installation_cell_code = get_pip_installation_cell_code(
        "numpy", "", "", "numpy", '--no-binary="numpy"', ""
    )
    assert (
        installation_cell_code
        == """try:
    import numpy
except ImportError:
    !python3 -m pip install --no-binary="numpy" numpy
    import numpy"""
    )


def test_pip_installation_cell_name_and_version_and_command_line_options() -> (
    None
):
    """Test installation cell with version and command-line options."""
    installation_cell_code = get_pip_installation_cell_code(
        "numpy", ">=1.21.0", "", "numpy", '--no-binary="numpy"', ""
    )
    assert (
        installation_cell_code
        == '!python3 -m pip install --upgrade --no-binary="numpy" "numpy>=1.21.0"'  # noqa: E501
    )


def test_pip_installation_cell_name_and_and_empty_package_import_and_command_line_options() -> (  # noqa: E501
    None
):
    """Test generation of installation cell with command line options."""
    installation_cell_code = get_pip_installation_cell_code(
        "numpy", "", "", "", '--no-binary="numpy"', ""
    )
    assert (
        installation_cell_code
        == '!python3 -m pip install --no-binary="numpy" numpy'
    )


def test_pip_installation_cell_name_and_extra_commands_before_install() -> None:
    """Test installation cell with pre-install extra commands."""
    installation_cell_code = get_pip_installation_cell_code(
        "numpy", "", "", "numpy", "", "cd /tmp"
    )
    assert (
        installation_cell_code
        == """try:
    import numpy
except ImportError:
    !cd /tmp && python3 -m pip install numpy
    import numpy"""
    )


def test_pip_installation_cell_name_and_version_and_extra_commands_before_install() -> (  # noqa: E501
    None
):
    """Test installation cell with version and pre-install commands."""
    installation_cell_code = get_pip_installation_cell_code(
        "numpy", ">=1.21.0", "", "numpy", "", "cd /tmp"
    )
    assert (
        installation_cell_code
        == '!cd /tmp && python3 -m pip install --upgrade "numpy>=1.21.0"'
    )
