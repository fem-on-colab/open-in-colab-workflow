# Copyright (C) 2021-2026 by the FEM on Colab authors
#
# This file is part of FEM on Colab-related actions.
#
# SPDX-License-Identifier: MIT
"""Get the hash of the HEAD commit of a Git repository."""

import subprocess


def get_git_head_hash(repo_url: str, branch: str) -> str:
    """Get the hash of an HEAD commit of a Git repository."""
    return subprocess.run(
        f"git ls-remote {repo_url} {branch} | cut -f1".split(" "),
        capture_output=True, check=True).stdout.decode("utf-8").strip("\n")[:7]
