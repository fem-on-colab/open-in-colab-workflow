# Copyright (C) 2021-2025 by the FEM on Colab authors
#
# This file is part of FEM on Colab-related actions.
#
# SPDX-License-Identifier: MIT
"""Tests for the open_in_cloud_workflow.get_fem_on_cloud_installation_line package."""

from open_in_cloud_workflow.get_fem_on_cloud_installation_line import get_fem_on_cloud_installation_line
from open_in_cloud_workflow.get_git_head_hash import get_git_head_hash


def test_fem_on_cloud_installation_line_only_name() -> None:
    """Test generation of installation line without any additonal version and url."""
    installation_line = get_fem_on_cloud_installation_line("colab", "gmsh", "", "", "", "")
    assert installation_line == 'wget "https://fem-on-colab.github.io/releases/gmsh-install.sh" -O "/tmp/gmsh-install.sh" && bash "/tmp/gmsh-install.sh"'  # noqa: E501


def test_fem_on_cloud_installation_line_name_and_version() -> None:
    """Test generation of installation line with version."""
    installation_line = get_fem_on_cloud_installation_line("colab", "firedrake", "==real", "", "", "")
    assert installation_line == 'wget "https://fem-on-colab.github.io/releases/firedrake-install-real.sh" -O "/tmp/firedrake-install.sh" && bash "/tmp/firedrake-install.sh"'  # noqa: E501


def test_fem_on_cloud_installation_line_name_and_url_at_fixed_commit() -> None:
    """Test generation of installation line with url at fixed commit."""
    installation_line = get_fem_on_cloud_installation_line("colab", "gmsh", "", "357e49c", "", "")
    assert installation_line == 'wget "https://github.com/fem-on-colab/fem-on-colab.github.io/raw/357e49c/releases/gmsh-install.sh" -O "/tmp/gmsh-install.sh" && bash "/tmp/gmsh-install.sh"'  # noqa: E501


def test_fem_on_cloud_installation_line_name_and_url_at_current_commit() -> None:
    """Test generation of installation line with url at current commit."""
    installation_line = get_fem_on_cloud_installation_line("colab", "gmsh", "", "current", "", "")
    website_head_commit = get_git_head_hash("https://github.com/fem-on-colab/fem-on-colab.github.io.git", "gh-pages")
    assert installation_line == f'wget "https://github.com/fem-on-colab/fem-on-colab.github.io/raw/{website_head_commit}/releases/gmsh-install.sh" -O "/tmp/gmsh-install.sh" && bash "/tmp/gmsh-install.sh"'  # noqa: E501


def test_fem_on_cloud_installation_line_name_version_and_url() -> None:
    """Test generation of installation line with version and url."""
    installation_line = get_fem_on_cloud_installation_line("colab", "firedrake", "==real", "357e49c", "", "")
    assert installation_line == 'wget "https://github.com/fem-on-colab/fem-on-colab.github.io/raw/357e49c/releases/firedrake-install-real.sh" -O "/tmp/firedrake-install.sh" && bash "/tmp/firedrake-install.sh"'  # noqa: E501
