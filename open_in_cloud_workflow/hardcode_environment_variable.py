# Copyright (C) 2021-2026 by the FEM on Colab authors
#
# This file is part of FEM on Colab-related actions.
#
# SPDX-License-Identifier: MIT
"""Hardcode an environment variable in a string."""

import os


def hardcode_environment_variable(variable_name: str, string: str) -> str:
    """Get the URL that a file will have on Kaggle when hosted on GitHub."""
    variable_value = os.environ[variable_name]
    return string.replace(
        f"${variable_name}", f"{variable_value}").replace(
        f"${{{variable_name}}}", f"{variable_value}")
