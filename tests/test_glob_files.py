# Copyright (C) 2021-2022 by the FEM on Colab authors
#
# This file is part of FEM on Colab-related actions.
#
# SPDX-License-Identifier: MIT
"""Tests for the open_in_cloud_workflow.glob_files package."""

import os

from open_in_cloud_workflow.glob_files import glob_files


def test_glob_files_single_pattern(root_directory: str) -> None:
    """Test pattern matching while listing notebooks in a directory."""
    data_directory = os.path.join(root_directory, "tests", "data")
    nb_pattern = os.path.join("replace_images_in_markdown", "*.ipynb")
    files = glob_files(data_directory, nb_pattern)
    assert files == {
        os.path.join(data_directory, nb_pattern).replace("*", nb_name) for nb_name in (
            "html_and_markdown_images", "html_image", "image_and_code", "markdown_image")}


def test_glob_files_multiple_patterns(root_directory: str) -> None:
    """Test pattern matching while listing notebooks and text files in a directory."""
    data_directory = os.path.join(root_directory, "tests", "data")
    nb_pattern = os.path.join("replace_images_in_markdown", "*.ipynb")
    txt_pattern = os.path.join("upload_file_to_google_drive", "*.txt")
    files = glob_files(data_directory, nb_pattern + "\n" + txt_pattern)
    assert files == {
        os.path.join(data_directory, nb_pattern).replace("*", nb_name) for nb_name in (
            "html_and_markdown_images", "html_image", "image_and_code", "markdown_image")
    }.union({
        os.path.join(data_directory, txt_pattern).replace("*", txt_name) for txt_name in (
            "existing_file", "new_file")
    })
