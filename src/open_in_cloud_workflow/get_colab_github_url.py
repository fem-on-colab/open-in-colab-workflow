# Copyright (C) 2021-2026 by the FEM on Colab authors
#
# This file is part of FEM on Colab-related actions.
#
# SPDX-License-Identifier: MIT
"""Build the Google Colab URL for a GitHub-hosted file."""


def get_colab_github_url(
    relative_path: str, repository: str, branch: str
) -> str:
    """Build the Google Colab URL for a GitHub-hosted file."""
    return f"https://colab.research.google.com/github/{repository}/blob/{branch}/{relative_path}"
