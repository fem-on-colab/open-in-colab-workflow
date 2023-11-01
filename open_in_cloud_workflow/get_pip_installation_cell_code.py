# Copyright (C) 2021-2023 by the FEM on Colab authors
#
# This file is part of FEM on Colab-related actions.
#
# SPDX-License-Identifier: MIT
"""Prepare installation cell code for a pip-installable package."""

from open_in_cloud_workflow.get_pip_installation_line import get_pip_installation_line


def get_pip_installation_cell_code(
    package_name: str, package_version: str, package_url: str, package_import: str,
    package_install_command_line_options: str, package_extra_commands_before_install: str
) -> str:
    """Return installation cell code for a pip installable package."""
    pip_installation_line = get_pip_installation_line(
        package_name, package_version, package_url, package_install_command_line_options,
        package_extra_commands_before_install)
    versions_operators = ("==", ">=", ">", "<=", "<")
    if any(operator in package_version for operator in versions_operators) or package_import == "":
        return f"!{pip_installation_line}"
    else:
        return f"""try:
    import {package_import}
except ImportError:
    !{pip_installation_line}
    import {package_import}"""
