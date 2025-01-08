# Copyright (C) 2021-2025 by the FEM on Colab authors
#
# This file is part of FEM on Colab-related actions.
#
# SPDX-License-Identifier: MIT
"""Get the URL that a file will have on Kaggle when hosted on GitHub."""


def get_kaggle_github_url(relative_path: str, repository: str, branch: str) -> str:
    """Get the URL that a file will have on Kaggle when hosted on GitHub."""
    return f"https://kaggle.com/kernels/welcome?src=https://github.com/{repository}/blob/{branch}/{relative_path}"
