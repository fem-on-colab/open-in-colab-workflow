# Copyright (C) 2021-2022 by the FEM on Colab authors
#
# This file is part of FEM on Colab-related actions.
#
# SPDX-License-Identifier: MIT
"""Tests for the open_in_colab_workflow.upload_files_to_google_drive package."""

import os
import shutil
import tempfile

import docker
import pytest
import requests

from open_in_colab_workflow.get_drive_url import get_drive_url
from open_in_colab_workflow.get_rclone_env import get_rclone_env
from open_in_colab_workflow.upload_files_to_google_drive import upload_files_to_google_drive


def assert_files_equal(root_directory: str, pattern: str, url: str) -> None:
    """Assert that the local file and the downloaded one have the same content."""
    remote_data = requests.get(url.replace("/open?", "/uc?"))
    with open(os.path.join(root_directory, pattern), "r") as f:
        assert f.read() == remote_data.content.decode("utf-8")


@pytest.mark.skipif("RCLONE_CONFIG_COLAB_TOKEN" not in os.environ, reason="Missing rclone environment variables")
def test_upload_files_to_google_drive_existing(root_directory: str) -> None:
    """Test that updating an existing file on Google Drive preserves its url."""
    pattern = os.path.join("tests", "data", "upload_file_to_google_drive", "existing_file.txt")
    upload_files_to_google_drive(root_directory, pattern, "GitHub/open_in_colab_workflow")
    url = get_drive_url(pattern, "GitHub/open_in_colab_workflow")
    assert url == "https://drive.google.com/open?id=1MUq5LVW4ScYDE1f1sHRi3XDupYe5jOra"
    assert_files_equal(root_directory, pattern, url)


@pytest.mark.skipif("RCLONE_CONFIG_COLAB_TOKEN" not in os.environ, reason="Missing rclone environment variables")
def test_upload_files_to_google_drive_new(root_directory: str) -> None:
    """Test uploading a new file on Google Drive."""
    original_pattern = os.path.join("tests", "data", "upload_file_to_google_drive", "new_file.txt")
    with tempfile.NamedTemporaryFile(
            dir=os.path.join(root_directory, os.path.dirname(original_pattern)), suffix=".txt") as tmp:
        shutil.copyfile(os.path.join(root_directory, original_pattern), tmp.name)
        pattern = os.path.relpath(tmp.name, root_directory)
        upload_files_to_google_drive(root_directory, pattern, "GitHub/open_in_colab_workflow")
        url = get_drive_url(pattern, "GitHub/open_in_colab_workflow")
        assert url is not None
        assert_files_equal(root_directory, pattern, url)
        # Clean up file on Drive
        rclone_env = get_rclone_env()
        client = docker.from_env()
        client.containers.run(
            "rclone/rclone", f'-q deletefile colab:{os.path.join("GitHub/open_in_colab_workflow", pattern)}',
            environment=rclone_env, remove=True
        )
