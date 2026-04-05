# Copyright (C) 2021-2026 by the FEM on Colab authors
#
# This file is part of FEM on Colab-related actions.
#
# SPDX-License-Identifier: MIT
"""Tests for the open_in_cloud_workflow.source_from package."""

import os

import pytest

from open_in_cloud_workflow.source_from import SourceFromDrive, SourceFromGitHub


@pytest.mark.skipif("RCLONE_CONFIG_DRIVE_TOKEN" not in os.environ, reason="Missing rclone environment variables")
def test_source_from_drive(source_from_drive: SourceFromDrive) -> None:
    """Test content of Google Drive source."""
    assert source_from_drive.drive_root_directory == "GitHub/open_in_colab_workflow"
    assert str(source_from_drive) == """source=drive
drive_root_directory=GitHub/open_in_colab_workflow"""


def test_source_from_github(source_from_github: SourceFromGitHub) -> None:
    """Test content of GitHub source."""
    assert source_from_github.repository == "fem-on-colab/open-in-colab-workflow"
    assert source_from_github.branch == "open-in-colab"
    assert str(source_from_github) == """source=github
repository=fem-on-colab/open-in-colab-workflow
branch=open-in-colab"""
