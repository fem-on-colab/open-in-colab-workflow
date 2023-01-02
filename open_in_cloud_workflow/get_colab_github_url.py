# Copyright (C) 2021-2023 by the FEM on Colab authors
#
# This file is part of FEM on Colab-related actions.
#
# SPDX-License-Identifier: MIT
"""Get the URL that a file will have on Google Colab when hosted on GitHub."""


def get_colab_github_url(relative_path: str, repository: str, branch: str) -> str:
    """Get the URL that a file will have on Google Colab when hosted on GitHub."""
    return f"https://colab.research.google.com/github/{repository}/blob/{branch}/{relative_path}"
