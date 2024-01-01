# Copyright (C) 2021-2024 by the FEM on Colab authors
#
# This file is part of FEM on Colab-related actions.
#
# SPDX-License-Identifier: MIT
"""Tests for the open_in_cloud_workflow.hardcode_environment_variable package."""

import os

import pytest

from open_in_cloud_workflow.hardcode_environment_variable import hardcode_environment_variable


def test_hardcode_environment_variable_set() -> None:
    """Test hardcoding environment variable when the variable value is correctly set."""
    os.environ["MY_VARIABLE"] = "my_value"
    assert hardcode_environment_variable(
        "MY_VARIABLE", "MY_VARIABLE=$MY_VARIABLE cmake .") == "MY_VARIABLE=my_value cmake ."
    assert hardcode_environment_variable(
        "MY_VARIABLE", "MY_VARIABLE=${MY_VARIABLE} cmake .") == "MY_VARIABLE=my_value cmake ."


def test_hardcode_environment_variable_unset() -> None:
    """Test failure of hardcoding a missing environment variable."""
    with pytest.raises(KeyError):
        hardcode_environment_variable("MISSING_VARIABLE", "MISSING_VARIABLE=$MISSING_VARIABLE cmake .")
