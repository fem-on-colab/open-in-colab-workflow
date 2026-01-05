# Copyright (C) 2021-2026 by the FEM on Colab authors
#
# This file is part of FEM on Colab-related actions.
#
# SPDX-License-Identifier: MIT
"""Tests for the open_in_cloud_workflow.glob_links package."""

import os

import pytest

from open_in_cloud_workflow.glob_links import glob_links
from open_in_cloud_workflow.publish_on import PublishOnArtifact, PublishOnDrive, PublishOnGitHub


def test_glob_links_with_artifact_publisher(root_directory: str, publish_on_artifact: PublishOnArtifact) -> None:
    """Test creation of link replacements dictionary with an artifact publisher."""
    nb_pattern = os.path.join("tests", "data", "replace_links_in_markdown", "*.ipynb")
    links_replacement = glob_links(root_directory, nb_pattern, "colab", publish_on_artifact)
    assert links_replacement == {}


@pytest.mark.skipif("RCLONE_CONFIG_DRIVE_TOKEN" not in os.environ, reason="Missing rclone environment variables")
def test_glob_links_with_drive_publisher(root_directory: str, publish_on_drive: PublishOnDrive) -> None:
    """Test creation of link replacements dictionary with a Google Drive publisher."""
    nb_pattern = os.path.join("tests", "data", "replace_links_in_markdown", "*.ipynb")
    links_replacement = glob_links(root_directory, nb_pattern, "colab", publish_on_drive)
    absolute_nb_pattern = os.path.join(root_directory, nb_pattern).replace("*", "{nb_name}")
    colab_pattern = "https://colab.research.google.com/drive/{drive_id}"
    assert links_replacement == {
        absolute_nb_pattern.format(nb_name=nb_name): colab_pattern.format(drive_id=drive_id)
        for (nb_name, drive_id) in (
            ("main_notebook", "1lccx0xSlkAsX53sK0KboPWSW6kzqWG6Z"),
            ("html_link_double_quotes", "179Yu6XEy3voI1Y8aQ8KWdjF1Np9FTWg4"),
            ("html_link_single_quotes", "1IwowRCntESea4c4jUk7jO9wX9-GnGn1b"),
            ("link_and_code", "10vNTBpBXggXkGGCY53bpiDL_SXwazzms"),
            ("markdown_link", "17iqh9FU_d3X9mhSnvnCtpHPyarxl96lK")
        )
    }


def test_glob_links_with_github_publisher(root_directory: str, publish_on_github: PublishOnGitHub) -> None:
    """Test creation of link replacements dictionary with a GitHub publisher."""
    nb_pattern = os.path.join("tests", "data", "replace_links_in_markdown", "*.ipynb")
    links_replacement = glob_links(root_directory, nb_pattern, "colab", publish_on_github)
    absolute_nb_pattern = os.path.join(root_directory, nb_pattern).replace("*", "{nb_name}")
    colab_pattern = os.path.join(
        "https://colab.research.google.com/github", publish_on_github.repository, "blob",
        publish_on_github.branch, os.path.relpath(absolute_nb_pattern, root_directory).replace("*", "{nb_name}")
    )
    assert links_replacement == {
        absolute_nb_pattern.format(nb_name=nb_name): colab_pattern.format(nb_name=nb_name)
        for nb_name in (
            "main_notebook", "html_link_double_quotes", "html_link_single_quotes", "link_and_code", "markdown_link")
    }
