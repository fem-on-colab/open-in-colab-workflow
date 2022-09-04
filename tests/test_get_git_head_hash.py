# Copyright (C) 2021-2022 by the FEM on Colab authors
#
# This file is part of FEM on Colab-related actions.
#
# SPDX-License-Identifier: MIT
"""Tests for the open_in_colab_workflow.get_git_head_hash package."""

import subprocess

from open_in_colab_workflow.get_git_head_hash import get_git_head_hash


def test_get_git_head_hash_new() -> None:
    """Test Google Drive URL for a file which was never uploaded."""
    this_repo_url = subprocess.run(
        "git remote get-url origin".split(" "),
        capture_output=True, check=True).stdout.decode("utf-8").strip("\n")
    head_commit = get_git_head_hash(this_repo_url)
    subprocess.run(
        "git fetch origin main".split(" "),
        capture_output=True, check=True)
    expected_head_commit = subprocess.run(
        "git rev-parse origin/main".split(" "),
        capture_output=True, check=True).stdout.decode("utf-8").strip("\n")[:7]
    assert head_commit == expected_head_commit