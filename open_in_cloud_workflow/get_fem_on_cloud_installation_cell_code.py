# Copyright (C) 2021-2023 by the FEM on Colab authors
#
# This file is part of FEM on Colab-related actions.
#
# SPDX-License-Identifier: MIT
"""Prepare installation cell code for a FEM on Cloud package."""

from open_in_cloud_workflow.get_fem_on_cloud_installation_line import get_fem_on_cloud_installation_line


def get_fem_on_cloud_installation_cell_code(
    cloud_provider: str, package_name: str, package_version: str, package_url: str, package_import: str
) -> str:
    """Return installation cell code for a FEM on Cloud package."""
    return f"""try:
    import {package_import}
except ImportError:
    !{get_fem_on_cloud_installation_line(cloud_provider, package_name, package_version, package_url)}
    import {package_import}"""
