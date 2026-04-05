# Copyright (C) 2021-2026 by the FEM on Colab authors
#
# This file is part of FEM on Colab-related actions.
#
# SPDX-License-Identifier: MIT
"""Tests for the open_in_cloud_workflow.download_files_from_google_drive package."""  # noqa: E501, W505

import os
import tempfile

import pytest
import requests

from open_in_cloud_workflow.download_files_from_google_drive import (
    download_files_from_google_drive,
)
from open_in_cloud_workflow.get_drive_url import get_drive_url


def assert_files_equal(root_directory: str, pattern: str, url: str) -> None:
    """Assert that local and downloaded files have identical content."""
    remote_data = requests.get(url.replace("/open?", "/uc?"))
    remote_data.raise_for_status()
    with open(os.path.join(root_directory, pattern)) as f:
        assert f.read() == remote_data.content.decode("utf-8")


@pytest.mark.skipif(
    "RCLONE_CONFIG_DRIVE_TOKEN" not in os.environ,
    reason="Missing rclone environment variables",
)
def test_download_files_from_google_drive(root_directory: str) -> None:
    """Test that updating an existing file on Google Drive preserves its url."""
    download_pattern = os.path.join(
        "tests", "data", "download_files_from_google_drive", "*.txt"
    )
    check_pattern = os.path.join(
        "tests", "data", "download_files_from_google_drive", "existing_file.txt"
    )
    with tempfile.TemporaryDirectory(dir=root_directory) as tmp_root_directory:
        os.makedirs(
            os.path.dirname(os.path.join(tmp_root_directory, download_pattern))
        )
        download_files_from_google_drive(
            tmp_root_directory,
            download_pattern,
            "GitHub/open_in_colab_workflow",
        )
        url = get_drive_url(check_pattern, "GitHub/open_in_colab_workflow")
        assert (
            url
            == "https://drive.google.com/open?id=1cvMOE2HbDxzQSK6fH4frs0ifZflDsaJY"
        )
        assert_files_equal(tmp_root_directory, check_pattern, url)
