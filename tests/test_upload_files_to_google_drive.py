# Copyright (C) 2021-2025 by the FEM on Colab authors
#
# This file is part of FEM on Colab-related actions.
#
# SPDX-License-Identifier: MIT
"""Tests for the open_in_cloud_workflow.upload_files_to_google_drive package."""

import datetime
import os
import shutil
import subprocess
import tempfile

import pytest
import requests

from open_in_cloud_workflow.get_drive_url import get_drive_url
from open_in_cloud_workflow.get_rclone_env import get_rclone_env
from open_in_cloud_workflow.upload_files_to_google_drive import upload_files_to_google_drive


def assert_files_equal(root_directory: str, pattern: str, url: str) -> None:
    """Assert that the local file and the downloaded one have the same content."""
    remote_data = requests.get(url.replace("/open?", "/uc?"))
    remote_data.raise_for_status()
    with open(os.path.join(root_directory, pattern)) as f:
        assert f.read() == remote_data.content.decode("utf-8")


@pytest.mark.skipif("RCLONE_CONFIG_DRIVE_TOKEN" not in os.environ, reason="Missing rclone environment variables")
def test_upload_files_to_google_drive_existing(root_directory: str) -> None:
    """Test that updating an existing file on Google Drive preserves its url."""
    pattern = os.path.join("tests", "data", "upload_file_to_google_drive", "existing_file.txt")
    with tempfile.TemporaryDirectory(dir=root_directory) as tmp_root_directory:
        os.makedirs(os.path.dirname(os.path.join(tmp_root_directory, pattern)))
        shutil.copyfile(os.path.join(root_directory, pattern), os.path.join(tmp_root_directory, pattern))
        with open(os.path.join(tmp_root_directory, pattern), "a") as f:
            f.write(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        upload_files_to_google_drive(tmp_root_directory, pattern, "GitHub/open_in_colab_workflow")
        url = get_drive_url(pattern, "GitHub/open_in_colab_workflow")
        assert url == "https://drive.google.com/open?id=1MUq5LVW4ScYDE1f1sHRi3XDupYe5jOra"
        assert_files_equal(tmp_root_directory, pattern, url)


@pytest.mark.skipif("RCLONE_CONFIG_DRIVE_TOKEN" not in os.environ, reason="Missing rclone environment variables")
def test_upload_files_to_google_drive_new_single_upload(root_directory: str) -> None:
    """Test uploading a new file on Google Drive."""
    original_pattern = os.path.join("tests", "data", "upload_file_to_google_drive", "new_file.txt")
    with tempfile.NamedTemporaryFile(
        dir=os.path.join(root_directory, os.path.dirname(original_pattern)), suffix=".txt"
    ) as tmp:
        shutil.copyfile(os.path.join(root_directory, original_pattern), tmp.name)
        pattern = os.path.relpath(tmp.name, root_directory)
        upload_files_to_google_drive(root_directory, pattern, "GitHub/open_in_colab_workflow")
        url = get_drive_url(pattern, "GitHub/open_in_colab_workflow")
        assert url is not None
        assert_files_equal(root_directory, pattern, url)
        # Clean up file on Drive
        subprocess.check_call(
            f'rclone -q deletefile drive:{os.path.join("GitHub/open_in_colab_workflow", pattern)}'.split(" "),
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, env=get_rclone_env())


@pytest.mark.skipif("RCLONE_CONFIG_DRIVE_TOKEN" not in os.environ, reason="Missing rclone environment variables")
def test_upload_files_to_google_drive_new_double_upload(root_directory: str) -> None:
    """Test uploading a new file on Google Drive, then replacing it with another."""
    copy_pattern = os.path.join("tests", "data", "upload_file_to_google_drive", "new_file.txt")
    upload_pattern = os.path.join(os.path.dirname(copy_pattern), "*.txt")
    # Do the first upload
    with tempfile.NamedTemporaryFile(
        dir=os.path.join(root_directory, os.path.dirname(upload_pattern)), suffix=".txt"
    ) as tmp1:
        shutil.copyfile(os.path.join(root_directory, copy_pattern), tmp1.name)
        pattern1 = os.path.relpath(tmp1.name, root_directory)
        upload_files_to_google_drive(root_directory, upload_pattern, "GitHub/open_in_colab_workflow")
        url1 = get_drive_url(pattern1, "GitHub/open_in_colab_workflow")
        assert url1 is not None
        assert_files_equal(root_directory, pattern1, url1)
    # Do the second upload
    with tempfile.NamedTemporaryFile(
        dir=os.path.join(root_directory, os.path.dirname(upload_pattern)), suffix=".txt"
    ) as tmp2:
        shutil.copyfile(os.path.join(root_directory, copy_pattern), tmp2.name)
        pattern2 = os.path.relpath(tmp2.name, root_directory)
        upload_files_to_google_drive(root_directory, upload_pattern, "GitHub/open_in_colab_workflow")
        url2 = get_drive_url(pattern2, "GitHub/open_in_colab_workflow")
        assert url2 is not None
        assert_files_equal(root_directory, pattern2, url2)
        # The file created in the first upload should have now been removed
        url1_deleted = get_drive_url(pattern1, "GitHub/open_in_colab_workflow")
        assert url1_deleted is None
        # Also delete the file created in the second upload
        subprocess.check_call(
            f'rclone -q deletefile drive:{os.path.join("GitHub/open_in_colab_workflow", pattern2)}'.split(" "),
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, env=get_rclone_env()
        )
