# Copyright (C) 2021-2024 by the FEM on Colab authors
#
# This file is part of FEM on Colab-related actions.
#
# SPDX-License-Identifier: MIT
"""Tests for the open_in_cloud_workflow.get_kaggle_drive_url package."""

import os
import tempfile

import pytest

from open_in_cloud_workflow.get_kaggle_drive_url import get_kaggle_drive_url


@pytest.mark.skipif("RCLONE_CONFIG_DRIVE_TOKEN" not in os.environ, reason="Missing rclone environment variables")
def test_get_kaggle_drive_url_existing(root_directory: str) -> None:
    """Test Kaggle URL for a file which was previously uploaded on Google Drive."""
    data_directory = os.path.join(root_directory, "tests", "data")
    absolute_path = os.path.join(data_directory, "upload_file_to_google_drive", "existing_file.txt")
    relative_path = os.path.relpath(absolute_path, root_directory)
    url = get_kaggle_drive_url(relative_path, "GitHub/open_in_kaggle_workflow")
    assert url == (
        "https://kaggle.com/kernels/welcome?src="
        + "https://drive.google.com/uc?id=13i5VtZV5n3Ipl5AB9b6c1EVVAWfDBaEW"
    )


@pytest.mark.skipif("RCLONE_CONFIG_DRIVE_TOKEN" not in os.environ, reason="Missing rclone environment variables")
def test_get_drive_url_new(root_directory: str) -> None:
    """Test Kaggle URL for a file which was never uploaded on Google Drive."""
    data_directory = os.path.join(root_directory, "tests", "data")
    data_subdirectory = os.path.join(data_directory, "upload_file_to_google_drive")
    with tempfile.NamedTemporaryFile(dir=data_subdirectory) as tmp:
        relative_path = os.path.relpath(tmp.name, root_directory)
        url = get_kaggle_drive_url(relative_path, "GitHub/open_in_kaggle_workflow")
        assert url is None
