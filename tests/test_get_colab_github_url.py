# Copyright (C) 2021-2022 by the FEM on Colab authors
#
# This file is part of FEM on Colab-related actions.
#
# SPDX-License-Identifier: MIT
"""Tests for the open_in_colab_workflow.get_colab_github_url package."""

from open_in_colab_workflow.get_colab_github_url import get_colab_github_url


def test_get_colab_github_url() -> None:
    """Test Google Colab URL for a file on a public GitHub repository."""
    url = get_colab_github_url("mock/test.ipynb", "fem-on-colab/fem-on-colab", "main")
    assert url == "https://colab.research.google.com/github/fem-on-colab/fem-on-colab/blob/main/mock/test.ipynb"
