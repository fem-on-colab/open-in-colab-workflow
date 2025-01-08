# Copyright (C) 2021-2025 by the FEM on Colab authors
#
# This file is part of FEM on Colab-related actions.
#
# SPDX-License-Identifier: MIT
"""Tests for the open_in_cloud_workflow.get_kaggle_github_url package."""

from open_in_cloud_workflow.get_kaggle_github_url import get_kaggle_github_url


def test_get_kaggle_github_url() -> None:
    """Test Kaggle URL for a file on a public GitHub repository."""
    url = get_kaggle_github_url("mock/test.ipynb", "fem-on-colab/fem-on-colab", "main")
    assert url == (
        "https://kaggle.com/kernels/welcome?src="
        + "https://github.com/fem-on-colab/fem-on-colab/blob/main/mock/test.ipynb"
    )
