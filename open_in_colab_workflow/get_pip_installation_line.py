# Copyright (C) 2021-2022 by the FEM on Colab authors
#
# This file is part of FEM on Colab-related actions.
#
# SPDX-License-Identifier: MIT
"""Prepare installation line for a pip-installable package."""


def get_pip_installation_line(package_name: str, package_version: str, package_url: str) -> str:
    """Return installation line for a pip installable package."""
    if package_version != "":
        install_arg = "--upgrade "
    else:
        install_arg = ""
    if package_url == "":
        package_url = f"{install_arg}{package_name}{package_version}"
    else:
        assert "https" in package_url
        assert package_version == ""
        package_url = f'{install_arg}"{package_name}@git+{package_url}"'
    return f"pip3 install {package_url}"
