# Copyright (C) 2021-2022 by the FEM on Colab authors
#
# This file is part of FEM on Colab-related actions.
#
# SPDX-License-Identifier: MIT
"""Prepare installation line for a FEM on Colab package."""

from open_in_cloud_workflow.get_git_head_hash import get_git_head_hash


def get_fem_on_colab_installation_line(package_name: str, package_version: str, package_url: str) -> str:
    """Return installation line for a FEM on Colab package."""
    if package_version != "":
        assert package_version.startswith("==")
        package_version = package_version.replace("==", "")
    if package_url == "":
        package_url_prefix = "https://fem-on-colab.github.io/releases"
    else:
        assert "https" not in package_url, "Please provide the commit SHA instead of the full URL"
        if package_url == "current":
            package_url = get_git_head_hash("https://github.com/fem-on-colab/fem-on-colab.github.io.git", "gh-pages")
        package_url_prefix = f"https://github.com/fem-on-colab/fem-on-colab.github.io/raw/{package_url}/releases"
    package_url_suffix = ".sh" if package_version == "" else f"-{package_version}.sh"
    package_url = f"{package_url_prefix}/{package_name}-install{package_url_suffix}"
    package_install = f"{package_name}-install.sh"
    return f'wget "{package_url}" -O "/tmp/{package_install}" && bash "/tmp/{package_install}"'
