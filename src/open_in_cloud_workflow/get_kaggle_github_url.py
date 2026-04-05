# Copyright (C) 2021-2026 by the FEM on Colab authors
#
# This file is part of FEM on Colab-related actions.
#
# SPDX-License-Identifier: MIT
"""Build the Kaggle URL for a GitHub-hosted file."""


def get_kaggle_github_url(
    relative_path: str, repository: str, branch: str
) -> str:
    """Build the Kaggle URL for a GitHub-hosted file."""
    return f"https://kaggle.com/kernels/welcome?src=https://github.com/{repository}/blob/{branch}/{relative_path}"
