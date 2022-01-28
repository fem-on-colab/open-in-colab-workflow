# Copyright (C) 2021-2022 by the FEM on Colab authors
#
# This file is part of FEM on Colab-related actions.
#
# SPDX-License-Identifier: MIT
"""Tests for the open_in_colab_workflow.packages_str_to_lists package."""

from open_in_colab_workflow.packages_str_to_lists import packages_str_to_lists


def test_single_package_str_to_list() -> None:
    """Test conversion of a single package without any additonal url and importable name."""
    packages_name, packages_version, packages_url, packages_import = packages_str_to_lists("numpy")
    assert len(packages_name) == 1
    assert packages_name[0] == "numpy"
    assert len(packages_version) == 1
    assert packages_version[0] == ""
    assert len(packages_url) == 1
    assert packages_url[0] == ""
    assert len(packages_import) == 1
    assert packages_import[0] == "numpy"


def test_single_package_minimum_version_str_to_list() -> None:
    """Test conversion of a single package with a minimum version."""
    packages_name, packages_version, packages_url, packages_import = packages_str_to_lists("numpy>=1.21.0")
    assert len(packages_name) == 1
    assert packages_name[0] == "numpy"
    assert len(packages_version) == 1
    assert packages_version[0] == ">=1.21.0"
    assert len(packages_url) == 1
    assert packages_url[0] == ""
    assert len(packages_import) == 1
    assert packages_import[0] == "numpy"


def test_single_package_minimum_maximum_version_str_to_list() -> None:
    """Test conversion of a single package with a minimum and maximum version."""
    packages_name, packages_version, packages_url, packages_import = packages_str_to_lists("numpy>=1.21.0,<1.22.0")
    assert len(packages_name) == 1
    assert packages_name[0] == "numpy"
    assert len(packages_version) == 1
    assert packages_version[0] == ">=1.21.0,<1.22.0"
    assert len(packages_url) == 1
    assert packages_url[0] == ""
    assert len(packages_import) == 1
    assert packages_import[0] == "numpy"


def test_single_package_url_str_to_list() -> None:
    """Test conversion of a single package with url and without importable name."""
    packages_name, packages_version, packages_url, packages_import = packages_str_to_lists(
        "numpy@https://github.com/numpy/numpy.git")
    assert len(packages_name) == 1
    assert packages_name[0] == "numpy"
    assert len(packages_version) == 1
    assert packages_version[0] == ""
    assert len(packages_url) == 1
    assert packages_url[0] == "https://github.com/numpy/numpy.git"
    assert len(packages_import) == 1
    assert packages_import[0] == "numpy"


def test_single_package_url_with_tag_str_to_list() -> None:
    """Test conversion of a single package with url (containing a tag) and without importable name."""
    packages_name, packages_version, packages_url, packages_import = packages_str_to_lists(
        "numpy@https://github.com/numpy/numpy.git@v1.22.0")
    assert len(packages_name) == 1
    assert packages_name[0] == "numpy"
    assert len(packages_version) == 1
    assert packages_version[0] == ""
    assert len(packages_url) == 1
    assert packages_url[0] == "https://github.com/numpy/numpy.git@v1.22.0"
    assert len(packages_import) == 1
    assert packages_import[0] == "numpy"


def test_single_package_import_str_to_list() -> None:
    """Test conversion of a single package with importable name and without url."""
    packages_name, packages_version, packages_url, packages_import = packages_str_to_lists("python-dateutil$dateutil")
    assert len(packages_name) == 1
    assert packages_name[0] == "python-dateutil"
    assert len(packages_version) == 1
    assert packages_version[0] == ""
    assert len(packages_url) == 1
    assert packages_url[0] == ""
    assert len(packages_import) == 1
    assert packages_import[0] == "dateutil"


def test_single_package_url_import_str_to_list() -> None:
    """Test conversion of a single package with url and importable name."""
    packages_name, packages_version, packages_url, packages_import = packages_str_to_lists(
        "python-dateutil@https://github.com/dateutil/dateutil.git$dateutil")
    assert len(packages_name) == 1
    assert packages_name[0] == "python-dateutil"
    assert len(packages_version) == 1
    assert packages_version[0] == ""
    assert len(packages_url) == 1
    assert packages_url[0] == "https://github.com/dateutil/dateutil.git"
    assert len(packages_import) == 1
    assert packages_import[0] == "dateutil"


def test_multiple_packages_on_single_line_import_str_to_list() -> None:
    """Test conversion of a multiple packages on a single line, with a necessary import name."""
    packages_name, packages_version, packages_url, packages_import = packages_str_to_lists(
        "itkwidgets pyvista$pyvista")
    assert len(packages_name) == 1
    assert packages_name[0] == "itkwidgets pyvista"
    assert len(packages_version) == 1
    assert packages_version[0] == ""
    assert len(packages_url) == 1
    assert packages_url[0] == ""
    assert len(packages_import) == 1
    assert packages_import[0] == "pyvista"


def test_multiple_packages_on_multiple_lines_str_to_list() -> None:
    """Test conversion of a multiple packages on multiple lines without any additonal url and importable name."""
    packages_name, packages_version, packages_url, packages_import = packages_str_to_lists("numpy\nscipy")
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


def test_no_package_str_to_list() -> None:
    """Test conversion of the empty string."""
    packages_name, packages_version, packages_url, packages_import = packages_str_to_lists("")
    assert len(packages_name) == 0
    assert len(packages_version) == 0
    assert len(packages_url) == 0
    assert len(packages_import) == 0
