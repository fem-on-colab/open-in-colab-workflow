# Copyright (C) 2021-2026 by the FEM on Colab authors
#
# This file is part of FEM on Colab-related actions.
#
# SPDX-License-Identifier: MIT
"""Tests for the open_in_cloud_workflow.packages_str_to_lists package."""

from open_in_cloud_workflow.packages_str_to_lists import packages_str_to_lists


def test_single_package_str_to_list() -> None:
    """Test single package conversion without URL or custom import."""
    (
        packages_name,
        packages_version,
        packages_url,
        packages_import,
        packages_dependent_imports,
        packages_install_command_line_options,
        packages_extra_commands_before_install,
    ) = packages_str_to_lists("numpy")
    assert len(packages_name) == 1
    assert packages_name[0] == "numpy"
    assert len(packages_version) == 1
    assert packages_version[0] == ""
    assert len(packages_url) == 1
    assert packages_url[0] == ""
    assert len(packages_import) == 1
    assert packages_import[0] == "numpy"
    assert len(packages_dependent_imports) == 1
    assert packages_dependent_imports[0] == ""
    assert len(packages_install_command_line_options) == 1
    assert packages_install_command_line_options[0] == ""
    assert len(packages_extra_commands_before_install) == 1
    assert packages_extra_commands_before_install[0] == ""


def test_single_package_minimum_version_str_to_list() -> None:
    """Test conversion of a single package with a minimum version."""
    (
        packages_name,
        packages_version,
        packages_url,
        packages_import,
        packages_dependent_imports,
        packages_install_command_line_options,
        packages_extra_commands_before_install,
    ) = packages_str_to_lists("numpy>=1.21.0")
    assert len(packages_name) == 1
    assert packages_name[0] == "numpy"
    assert len(packages_version) == 1
    assert packages_version[0] == ">=1.21.0"
    assert len(packages_url) == 1
    assert packages_url[0] == ""
    assert len(packages_import) == 1
    assert packages_import[0] == "numpy"
    assert len(packages_dependent_imports) == 1
    assert packages_dependent_imports[0] == ""
    assert len(packages_install_command_line_options) == 1
    assert packages_install_command_line_options[0] == ""
    assert len(packages_extra_commands_before_install) == 1
    assert packages_extra_commands_before_install[0] == ""


def test_single_package_minimum_maximum_version_str_to_list() -> None:
    """Test single package conversion with min and max version."""
    (
        packages_name,
        packages_version,
        packages_url,
        packages_import,
        packages_dependent_imports,
        packages_install_command_line_options,
        packages_extra_commands_before_install,
    ) = packages_str_to_lists("numpy>=1.21.0,<1.22.0")
    assert len(packages_name) == 1
    assert packages_name[0] == "numpy"
    assert len(packages_version) == 1
    assert packages_version[0] == ">=1.21.0,<1.22.0"
    assert len(packages_url) == 1
    assert packages_url[0] == ""
    assert len(packages_import) == 1
    assert packages_import[0] == "numpy"
    assert len(packages_dependent_imports) == 1
    assert packages_dependent_imports[0] == ""
    assert len(packages_install_command_line_options) == 1
    assert packages_install_command_line_options[0] == ""
    assert len(packages_extra_commands_before_install) == 1
    assert packages_extra_commands_before_install[0] == ""


def test_single_package_extras_str_to_list() -> None:
    """Test conversion of a single package with extras."""
    (
        packages_name,
        packages_version,
        packages_url,
        packages_import,
        packages_dependent_imports,
        packages_install_command_line_options,
        packages_extra_commands_before_install,
    ) = packages_str_to_lists("jax[cpu]")
    assert len(packages_name) == 1
    assert packages_name[0] == "jax"
    assert len(packages_version) == 1
    assert packages_version[0] == "[cpu]"
    assert len(packages_url) == 1
    assert packages_url[0] == ""
    assert len(packages_import) == 1
    assert packages_import[0] == "jax"
    assert len(packages_dependent_imports) == 1
    assert packages_dependent_imports[0] == ""
    assert len(packages_install_command_line_options) == 1
    assert packages_install_command_line_options[0] == ""
    assert len(packages_extra_commands_before_install) == 1
    assert packages_extra_commands_before_install[0] == ""


def test_single_package_url_str_to_list() -> None:
    """Test single package conversion with URL and default import."""
    (
        packages_name,
        packages_version,
        packages_url,
        packages_import,
        packages_dependent_imports,
        packages_install_command_line_options,
        packages_extra_commands_before_install,
    ) = packages_str_to_lists("numpy@https://github.com/numpy/numpy.git")
    assert len(packages_name) == 1
    assert packages_name[0] == "numpy"
    assert len(packages_version) == 1
    assert packages_version[0] == ""
    assert len(packages_url) == 1
    assert packages_url[0] == "https://github.com/numpy/numpy.git"
    assert len(packages_import) == 1
    assert packages_import[0] == "numpy"
    assert len(packages_dependent_imports) == 1
    assert packages_dependent_imports[0] == ""
    assert len(packages_install_command_line_options) == 1
    assert packages_install_command_line_options[0] == ""
    assert len(packages_extra_commands_before_install) == 1
    assert packages_extra_commands_before_install[0] == ""


def test_single_package_url_with_tag_str_to_list() -> None:
    """Test single package conversion with URL containing a tag."""
    (
        packages_name,
        packages_version,
        packages_url,
        packages_import,
        packages_dependent_imports,
        packages_install_command_line_options,
        packages_extra_commands_before_install,
    ) = packages_str_to_lists(
        "numpy@https://github.com/numpy/numpy.git@v1.22.0"
    )
    assert len(packages_name) == 1
    assert packages_name[0] == "numpy"
    assert len(packages_version) == 1
    assert packages_version[0] == ""
    assert len(packages_url) == 1
    assert packages_url[0] == "https://github.com/numpy/numpy.git@v1.22.0"
    assert len(packages_import) == 1
    assert packages_import[0] == "numpy"
    assert len(packages_dependent_imports) == 1
    assert packages_dependent_imports[0] == ""
    assert len(packages_install_command_line_options) == 1
    assert packages_install_command_line_options[0] == ""
    assert len(packages_extra_commands_before_install) == 1
    assert packages_extra_commands_before_install[0] == ""


def test_single_package_import_str_to_list() -> None:
    """Test single package conversion with custom import and no URL."""
    (
        packages_name,
        packages_version,
        packages_url,
        packages_import,
        packages_dependent_imports,
        packages_install_command_line_options,
        packages_extra_commands_before_install,
    ) = packages_str_to_lists("python-dateutil$dateutil")
    assert len(packages_name) == 1
    assert packages_name[0] == "python-dateutil"
    assert len(packages_version) == 1
    assert packages_version[0] == ""
    assert len(packages_url) == 1
    assert packages_url[0] == ""
    assert len(packages_import) == 1
    assert packages_import[0] == "dateutil"
    assert len(packages_dependent_imports) == 1
    assert packages_dependent_imports[0] == ""
    assert len(packages_install_command_line_options) == 1
    assert packages_install_command_line_options[0] == ""
    assert len(packages_extra_commands_before_install) == 1
    assert packages_extra_commands_before_install[0] == ""


def test_single_package_dependent_imports_str_to_list() -> None:
    """Test conversion with dependent imports and default import name."""
    (
        packages_name,
        packages_version,
        packages_url,
        packages_import,
        packages_dependent_imports,
        packages_install_command_line_options,
        packages_extra_commands_before_install,
    ) = packages_str_to_lists("kaleido%plotly")
    assert len(packages_name) == 1
    assert packages_name[0] == "kaleido"
    assert len(packages_version) == 1
    assert packages_version[0] == ""
    assert len(packages_url) == 1
    assert packages_url[0] == ""
    assert len(packages_import) == 1
    assert packages_import[0] == "kaleido"
    assert len(packages_dependent_imports) == 1
    assert packages_dependent_imports[0] == "plotly"
    assert len(packages_install_command_line_options) == 1
    assert packages_install_command_line_options[0] == ""
    assert len(packages_extra_commands_before_install) == 1
    assert packages_extra_commands_before_install[0] == ""


def test_single_package_url_import_str_to_list() -> None:
    """Test conversion of a single package with url and importable name."""
    (
        packages_name,
        packages_version,
        packages_url,
        packages_import,
        packages_dependent_imports,
        packages_install_command_line_options,
        packages_extra_commands_before_install,
    ) = packages_str_to_lists(
        "python-dateutil@https://github.com/dateutil/dateutil.git$dateutil"
    )
    assert len(packages_name) == 1
    assert packages_name[0] == "python-dateutil"
    assert len(packages_version) == 1
    assert packages_version[0] == ""
    assert len(packages_url) == 1
    assert packages_url[0] == "https://github.com/dateutil/dateutil.git"
    assert len(packages_import) == 1
    assert packages_import[0] == "dateutil"
    assert len(packages_dependent_imports) == 1
    assert packages_dependent_imports[0] == ""
    assert len(packages_install_command_line_options) == 1
    assert packages_install_command_line_options[0] == ""
    assert len(packages_extra_commands_before_install) == 1
    assert packages_extra_commands_before_install[0] == ""


def test_single_package_command_line_options_str_to_list() -> None:
    """Test conversion of a single package with command line options."""
    (
        packages_name,
        packages_version,
        packages_url,
        packages_import,
        packages_dependent_imports,
        packages_install_command_line_options,
        packages_extra_commands_before_install,
    ) = packages_str_to_lists('numpy£--no-binary="numpy"')
    assert len(packages_name) == 1
    assert packages_name[0] == "numpy"
    assert len(packages_version) == 1
    assert packages_version[0] == ""
    assert len(packages_url) == 1
    assert packages_url[0] == ""
    assert len(packages_import) == 1
    assert packages_import[0] == "numpy"
    assert len(packages_dependent_imports) == 1
    assert packages_dependent_imports[0] == ""
    assert len(packages_install_command_line_options) == 1
    assert packages_install_command_line_options[0] == '--no-binary="numpy"'
    assert len(packages_extra_commands_before_install) == 1
    assert packages_extra_commands_before_install[0] == ""


def test_single_package_extra_commands_before_install_str_to_list() -> None:
    """Test single package conversion with pre-install commands."""
    (
        packages_name,
        packages_version,
        packages_url,
        packages_import,
        packages_dependent_imports,
        packages_install_command_line_options,
        packages_extra_commands_before_install,
    ) = packages_str_to_lists("numpy€cd /tmp")
    assert len(packages_name) == 1
    assert packages_name[0] == "numpy"
    assert len(packages_version) == 1
    assert packages_version[0] == ""
    assert len(packages_url) == 1
    assert packages_url[0] == ""
    assert len(packages_import) == 1
    assert packages_import[0] == "numpy"
    assert len(packages_dependent_imports) == 1
    assert packages_dependent_imports[0] == ""
    assert len(packages_install_command_line_options) == 1
    assert packages_install_command_line_options[0] == ""
    assert len(packages_extra_commands_before_install) == 1
    assert packages_extra_commands_before_install[0] == "cd /tmp"


def test_single_package_minimum_version_command_line_options_str_to_list() -> (
    None
):
    """Test conversion with minimum version and command-line options."""
    (
        packages_name,
        packages_version,
        packages_url,
        packages_import,
        packages_dependent_imports,
        packages_install_command_line_options,
        packages_extra_commands_before_install,
    ) = packages_str_to_lists('numpy>=1.21.0£--no-binary="numpy"')
    assert len(packages_name) == 1
    assert packages_name[0] == "numpy"
    assert len(packages_version) == 1
    assert packages_version[0] == ">=1.21.0"
    assert len(packages_url) == 1
    assert packages_url[0] == ""
    assert len(packages_import) == 1
    assert packages_import[0] == "numpy"
    assert len(packages_dependent_imports) == 1
    assert packages_dependent_imports[0] == ""
    assert len(packages_install_command_line_options) == 1
    assert packages_install_command_line_options[0] == '--no-binary="numpy"'
    assert len(packages_extra_commands_before_install) == 1
    assert packages_extra_commands_before_install[0] == ""


def test_single_package_empty_package_import_command_line_options_str_to_list() -> (  # noqa: E501
    None
):
    """Test conversion with empty import and command-line options."""
    (
        packages_name,
        packages_version,
        packages_url,
        packages_import,
        packages_dependent_imports,
        packages_install_command_line_options,
        packages_extra_commands_before_install,
    ) = packages_str_to_lists('numpy$£--no-binary="numpy"')
    assert len(packages_name) == 1
    assert packages_name[0] == "numpy"
    assert len(packages_version) == 1
    assert packages_version[0] == ""
    assert len(packages_url) == 1
    assert packages_url[0] == ""
    assert len(packages_import) == 1
    assert packages_import[0] == ""
    assert len(packages_dependent_imports) == 1
    assert packages_dependent_imports[0] == ""
    assert len(packages_install_command_line_options) == 1
    assert packages_install_command_line_options[0] == '--no-binary="numpy"'
    assert len(packages_extra_commands_before_install) == 1
    assert packages_extra_commands_before_install[0] == ""


def test_multiple_packages_on_single_line_import_str_to_list() -> None:
    """Test conversion of multiple packages on one line with import."""
    (
        packages_name,
        packages_version,
        packages_url,
        packages_import,
        packages_dependent_imports,
        packages_install_command_line_options,
        packages_extra_commands_before_install,
    ) = packages_str_to_lists("itkwidgets pyvista$pyvista")
    assert len(packages_name) == 1
    assert packages_name[0] == "itkwidgets pyvista"
    assert len(packages_version) == 1
    assert packages_version[0] == ""
    assert len(packages_url) == 1
    assert packages_url[0] == ""
    assert len(packages_import) == 1
    assert packages_import[0] == "pyvista"
    assert len(packages_dependent_imports) == 1
    assert packages_dependent_imports[0] == ""
    assert len(packages_install_command_line_options) == 1
    assert packages_install_command_line_options[0] == ""
    assert len(packages_extra_commands_before_install) == 1
    assert packages_extra_commands_before_install[0] == ""
    assert len(packages_extra_commands_before_install) == 1
    assert packages_extra_commands_before_install[0] == ""


def test_multiple_packages_on_multiple_lines_str_to_list() -> None:
    """Test conversion of multiple packages on multiple lines."""
    (
        packages_name,
        packages_version,
        packages_url,
        packages_import,
        packages_dependent_imports,
        packages_install_command_line_options,
        packages_extra_commands_before_install,
    ) = packages_str_to_lists("numpy\nscipy")
    assert len(packages_name) == 2
    assert packages_name[0] == "numpy"
    assert packages_name[1] == "scipy"
    assert len(packages_version) == 2
    assert packages_version[0] == ""
    assert packages_version[1] == ""
    assert len(packages_url) == 2
    assert packages_url[0] == ""
    assert packages_url[1] == ""
    assert len(packages_import) == 2
    assert packages_import[0] == "numpy"
    assert packages_import[1] == "scipy"
    assert len(packages_dependent_imports) == 2
    assert packages_dependent_imports[0] == ""
    assert packages_dependent_imports[1] == ""
    assert len(packages_install_command_line_options) == 2
    assert packages_install_command_line_options[0] == ""
    assert packages_install_command_line_options[1] == ""
    assert len(packages_extra_commands_before_install) == 2
    assert packages_extra_commands_before_install[0] == ""
    assert packages_extra_commands_before_install[1] == ""


def test_no_package_str_to_list() -> None:
    """Test conversion of the empty string."""
    (
        packages_name,
        packages_version,
        packages_url,
        packages_import,
        packages_dependent_imports,
        packages_install_command_line_options,
        packages_extra_commands_before_install,
    ) = packages_str_to_lists("")
    assert len(packages_name) == 0
    assert len(packages_version) == 0
    assert len(packages_url) == 0
    assert len(packages_import) == 0
    assert len(packages_dependent_imports) == 0
    assert len(packages_extra_commands_before_install) == 0
    assert len(packages_install_command_line_options) == 0
