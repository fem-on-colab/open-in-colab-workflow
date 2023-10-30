# Copyright (C) 2021-2023 by the FEM on Colab authors
#
# This file is part of FEM on Colab-related actions.
#
# SPDX-License-Identifier: MIT
"""Prepare installation line for a pip-installable package."""

from open_in_cloud_workflow.get_git_head_hash import get_git_head_hash


def get_pip_installation_line(
    package_name: str, package_version: str, package_url: str, package_install_command_line_options: str
) -> str:
    """Return installation line for a pip installable package."""
    extras_operators = ("[", "]")
    versions_operators = ("==", ">=", ">", "<=", "<")
    if any(operator in package_version for operator in extras_operators):
        assert all([operator not in package_version for operator in versions_operators])
        install_arg = ""
    elif any(operator in package_version for operator in versions_operators):
        assert all([operator not in package_version for operator in extras_operators])
        install_arg = "--upgrade "
    else:
        assert package_version == ""
        install_arg = ""
    if package_install_command_line_options != "":
        install_arg += package_install_command_line_options + " "
    if package_url == "":
        if install_arg == "" and package_version == "":
            package_url = f"{package_name}"
        elif install_arg != "" and package_version == "":
            package_url = f"{install_arg}{package_name}"
        elif install_arg == "" and package_version != "":
            package_url = f"{package_name}{package_version}"
        else:
            package_url = f'{install_arg}"{package_name}{package_version}"'
    else:
        assert "https" in package_url
        if package_version != "":
            assert all([operator not in package_version for operator in versions_operators])
            assert any(operator in package_version for operator in extras_operators)
        if package_url.endswith("@current"):
            package_url_without_commit = package_url.replace("@current", "")
            package_url = package_url_without_commit + "@" + get_git_head_hash(package_url_without_commit, "HEAD")
        package_url = f'{install_arg}"{package_name}{package_version}@git+{package_url}"'
    return f"pip3 install {package_url}"
