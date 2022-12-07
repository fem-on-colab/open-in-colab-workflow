# Copyright (C) 2021-2022 by the FEM on Colab authors
#
# This file is part of FEM on Colab-related actions.
#
# SPDX-License-Identifier: MIT
"""Tests for the open_in_cloud_workflow.publish_on package."""

import os

import pytest

from open_in_cloud_workflow.publish_on import PublishOnArtifact, PublishOnDrive, PublishOnGitHub


def test_publish_on_artifact(publish_on_artifact: PublishOnArtifact) -> None:
    """Test content of artifact publisher."""
    assert publish_on_artifact.name == "open-in-colab"
    with pytest.raises(RuntimeError):
        publish_on_artifact.get_url("colab", "relative_path")
    assert str(publish_on_artifact) == """publisher=artifact
name=open-in-colab"""


@pytest.mark.skipif("RCLONE_CONFIG_DRIVE_TOKEN" not in os.environ, reason="Missing rclone environment variables")
def test_publish_on_drive(publish_on_drive: PublishOnDrive) -> None:
    """Test content of Google Drive publisher."""
    assert publish_on_drive.drive_root_directory == "GitHub/open_in_colab_workflow"
    publish_on_drive.get_url(
        "colab", os.path.join("tests", "data", "upload_file_to_google_drive", "existing_file.txt")) == (
            "https://colab.research.google.com/drive/1MUq5LVW4ScYDE1f1sHRi3XDupYe5jOra")
    publish_on_drive.get_url(
        "kaggle", os.path.join("tests", "data", "upload_file_to_google_drive", "existing_file.txt")) == (
            "https://kaggle.com/kernels/welcome?src="
            + "https://drive.google.com/uc?id=13i5VtZV5n3Ipl5AB9b6c1EVVAWfDBaEW")
    assert str(publish_on_drive) == """publisher=drive
drive_root_directory=GitHub/open_in_colab_workflow"""


def test_publish_on_github(publish_on_github: PublishOnGitHub) -> None:
    """Test content of GitHub publisher."""
    assert publish_on_github.repository == "fem-on-colab/open-in-colab-workflow"
    assert publish_on_github.branch == "open-in-colab"
    publish_on_github.get_url(
        "colab", os.path.join("tests", "data", "add_installation_cells", "import_numpy.ipynb")) == (
            "https://colab.research.google.com/github/fem-on-colab/open-in-colab-workflow/blob/open-in-colab"
            + "/tests/data/add_installation_cells/import_numpy.ipynb")
    publish_on_github.get_url(
        "kaggle", os.path.join("tests", "data", "add_installation_cells", "import_numpy.ipynb")) == (
            "https://kaggle.com/kernels/welcome?src="
            + "https://github.com/fem-on-colab/open-in-colab-workflow/blob/open-in-colab"
            + "/tests/data/add_installation_cells/import_numpy.ipynb")
    assert str(publish_on_github) == """publisher=github
repository=fem-on-colab/open-in-colab-workflow
branch=open-in-colab"""
