# Copyright (C) 2021-2022 by the FEM on Colab authors
#
# This file is part of FEM on Colab-related actions.
#
# SPDX-License-Identifier: MIT
"""Prepare installation cell code for a pip-installable package."""

from open_in_colab_workflow.get_pip_installation_line import get_pip_installation_line


def get_pip_installation_cell_code(
    package_name: str, package_version: str, package_url: str, package_import: str
) -> str:
    """Return installation cell code for a pip installable package."""
    versions_operators = ("==", ">=", ">", "<=", "<")
    if any(operator in package_version for operator in versions_operators):
        return f"!{get_pip_installation_line(package_name, package_version, package_url)}"
    else:
        return f"""try:
    import {package_import}
except ImportError:
    !{get_pip_installation_line(package_name, package_version, package_url)}
    import {package_import}""" + _enable_custom_widget_manager(package_name)


def _enable_custom_widget_manager(package_name: str) -> str:
    """Return additional finally block for packages that require a custom widget manager."""
    if any([requires_custom_widget_manager in package_name for requires_custom_widget_manager in (
            "itkwidgets", )]):
        return "\n" + """finally:
    import google.colab
    google.colab.output.enable_custom_widget_manager()"""
    else:
        return ""
