# Copyright (C) 2021-2025 by the FEM on Colab authors
#
# This file is part of FEM on Colab-related actions.
#
# SPDX-License-Identifier: MIT
"""Tests for the open_in_cloud_workflow.get_pip_installation_line package."""

import os

from open_in_cloud_workflow.get_git_head_hash import get_git_head_hash
from open_in_cloud_workflow.get_pip_installation_line import get_pip_installation_line


def test_pip_installation_line_only_name() -> None:
    """Test generation of installation line without any additonal version and url."""
    installation_line = get_pip_installation_line("numpy", "", "", "", "")
    assert installation_line == "pip3 install numpy"


def test_pip_installation_line_name_and_version() -> None:
    """Test generation of installation line with version."""
    installation_line = get_pip_installation_line("numpy", ">=1.21.0,<1.22.0", "", "", "")
    assert installation_line == 'pip3 install --upgrade "numpy>=1.21.0,<1.22.0"'


def test_pip_installation_line_name_and_extras() -> None:
    """Test generation of installation line with extras."""
    installation_line = get_pip_installation_line("jax", "[cpu]", "", "", "")
    assert installation_line == "pip3 install jax[cpu]"


def test_pip_installation_line_name_and_url() -> None:
    """Test generation of installation line with url."""
    installation_line = get_pip_installation_line("numpy", "", "https://github.com/numpy/numpy.git", "", "")
    assert installation_line == 'pip3 install "numpy@git+https://github.com/numpy/numpy.git"'


def test_pip_installation_line_name_and_url_at_fixed_commit() -> None:
    """Test generation of installation line with url at a fixed commit."""
    installation_line = get_pip_installation_line("numpy", "", "https://github.com/numpy/numpy.git@2a6daf3", "", "")
    assert installation_line == 'pip3 install "numpy@git+https://github.com/numpy/numpy.git@2a6daf3"'


def test_pip_installation_line_name_and_url_at_current_commit() -> None:
    """Test generation of installation line with url at the current commit."""
    installation_line = get_pip_installation_line("numpy", "", "https://github.com/numpy/numpy.git@current", "", "")
    numpy_head_commit = get_git_head_hash("https://github.com/numpy/numpy.git", "main")
    assert installation_line == f'pip3 install "numpy@git+https://github.com/numpy/numpy.git@{numpy_head_commit}"'


def test_pip_installation_line_name_and_extras_and_url() -> None:
    """Test generation of installation line with extras and url."""
    installation_line = get_pip_installation_line("jax", "[cpu]", "https://github.com/google/jax.git", "", "")
    assert installation_line == 'pip3 install "jax[cpu]@git+https://github.com/google/jax.git"'


def test_pip_installation_line_name_and_command_line_options() -> None:
    """Test generation of installation line with command line options."""
    installation_line = get_pip_installation_line("numpy", "", "", '--no-binary="numpy"', "")
    assert installation_line == 'pip3 install --no-binary="numpy" numpy'


def test_pip_installation_line_name_and_version_and_command_line_options() -> None:
    """Test generation of installation line with a version and command line options."""
    installation_line = get_pip_installation_line("numpy", ">=1.21.0", "", '--no-binary="numpy"', "")
    assert installation_line == 'pip3 install --upgrade --no-binary="numpy" "numpy>=1.21.0"'


def test_pip_installation_line_name_and_command_line_options_with_environment_variable() -> None:
    """Test generation of installation line with command line options employing an environment variable."""
    os.environ["INSTALL_PREFIX"] = "/my/install/prefix"
    installation_line = get_pip_installation_line(
        "basix", "", "", "--config-settings=cmake.define.CMAKE_PREFIX_PATH=${INSTALL_PREFIX}", "")
    assert installation_line == "pip3 install --config-settings=cmake.define.CMAKE_PREFIX_PATH=/my/install/prefix basix"


def test_pip_installation_line_name_and_extra_commands_before_install() -> None:
    """Test generation of installation line with extra commands before install."""
    installation_line = get_pip_installation_line("numpy", "", "", "", "cd /tmp")
    assert installation_line == "cd /tmp && pip3 install numpy"


def test_pip_installation_line_name_and_extra_commands_before_install_with_environment_variable() -> None:
    """Test generation of installation line with extra commands before install employing an environment variable."""
    os.environ["INSTALL_PREFIX"] = "/my/install/prefix"
    installation_line = get_pip_installation_line("numpy", "", "", "", "cd ${INSTALL_PREFIX}")
    assert installation_line == "cd /my/install/prefix && pip3 install numpy"


def test_pip_installation_line_multiple_packages() -> None:
    """Test generation of installation line when two packages are provided."""
    installation_line = get_pip_installation_line("itkwidgets pyvista", "", "", "", "")
    assert installation_line == "pip3 install itkwidgets pyvista"
