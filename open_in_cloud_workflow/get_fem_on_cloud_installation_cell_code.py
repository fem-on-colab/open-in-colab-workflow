# Copyright (C) 2021-2025 by the FEM on Colab authors
#
# This file is part of FEM on Colab-related actions.
#
# SPDX-License-Identifier: MIT
"""Prepare installation cell code for a FEM on Cloud package."""

from open_in_cloud_workflow.get_fem_on_cloud_installation_line import get_fem_on_cloud_installation_line


def get_fem_on_cloud_installation_cell_code(
    cloud_provider: str, package_name: str, package_version: str, package_url: str, package_import: str,
    package_install_command_line_options: str, package_extra_commands_before_install: str
) -> str:
    """Return installation cell code for a FEM on Cloud package."""
    fem_on_cloud_installation_line = get_fem_on_cloud_installation_line(
        cloud_provider, package_name, package_version, package_url, package_install_command_line_options,
        package_extra_commands_before_install)
    assert package_import != ""
    return f"""try:
    import {package_import}
except ImportError:
    !{fem_on_cloud_installation_line}
    import {package_import}"""
