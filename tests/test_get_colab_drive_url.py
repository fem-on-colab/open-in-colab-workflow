# Copyright (C) 2021-2026 by the FEM on Colab authors
#
# This file is part of FEM on Colab-related actions.
#
# SPDX-License-Identifier: MIT
"""Tests for the open_in_cloud_workflow.get_colab_drive_url package."""

import os
import tempfile

import pytest

from open_in_cloud_workflow.get_colab_drive_url import get_colab_drive_url


@pytest.mark.skipif("RCLONE_CONFIG_DRIVE_TOKEN" not in os.environ, reason="Missing rclone environment variables")
def test_get_colab_drive_url_existing(root_directory: str) -> None:
    """Test Google Colab URL for a file which was previously uploaded on Google Drive."""
    data_directory = os.path.join(root_directory, "tests", "data")
    absolute_path = os.path.join(data_directory, "upload_file_to_google_drive", "existing_file.txt")
    relative_path = os.path.relpath(absolute_path, root_directory)
    url = get_colab_drive_url(relative_path, "GitHub/open_in_colab_workflow")
    assert url == "https://colab.research.google.com/drive/1MUq5LVW4ScYDE1f1sHRi3XDupYe5jOra"


@pytest.mark.skipif("RCLONE_CONFIG_DRIVE_TOKEN" not in os.environ, reason="Missing rclone environment variables")
def test_get_drive_url_new(root_directory: str) -> None:
    """Test Google Colab URL for a file which was never uploaded on Google Drive."""
    data_directory = os.path.join(root_directory, "tests", "data")
    data_subdirectory = os.path.join(data_directory, "upload_file_to_google_drive")
    with tempfile.NamedTemporaryFile(dir=data_subdirectory) as tmp:
        relative_path = os.path.relpath(tmp.name, root_directory)
        url = get_colab_drive_url(relative_path, "GitHub/open_in_colab_workflow")
        assert url is None
