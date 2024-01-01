# Copyright (C) 2021-2024 by the FEM on Colab authors
#
# This file is part of FEM on Colab-related actions.
#
# SPDX-License-Identifier: MIT
"""Prepare installation line for a FEM on Cloud package."""

from open_in_cloud_workflow.get_git_head_hash import get_git_head_hash


def get_fem_on_cloud_installation_line(
    cloud_provider: str, package_name: str, package_version: str, package_url: str,
    package_install_command_line_options: str, package_extra_commands_before_install: str
) -> str:
    """Return installation line for a FEM on Cloud package."""
    if package_version != "":
        assert package_version.startswith("==")
        package_version = package_version.replace("==", "")
    if package_url == "":
        package_url_prefix = f"https://fem-on-{cloud_provider}.github.io/releases"
    else:
        assert "https" not in package_url, "Please provide the commit SHA instead of the full URL"
        if package_url == "current":
            package_url = get_git_head_hash(
                f"https://github.com/fem-on-{cloud_provider}/fem-on-{cloud_provider}.github.io.git", "gh-pages")
        package_url_prefix = (
            f"https://github.com/fem-on-{cloud_provider}/fem-on-{cloud_provider}.github.io/raw/{package_url}/releases")
    package_url_suffix = ".sh" if package_version == "" else f"-{package_version}.sh"
    package_url = f"{package_url_prefix}/{package_name}-install{package_url_suffix}"
    assert package_install_command_line_options == ""
    assert package_extra_commands_before_install == ""
    package_install = f"{package_name}-install.sh"
    return f'wget "{package_url}" -O "/tmp/{package_install}" && bash "/tmp/{package_install}"'
