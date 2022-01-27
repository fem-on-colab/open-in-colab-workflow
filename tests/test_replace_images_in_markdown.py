# Copyright (C) 2021-2022 by the FEM on Colab authors
#
# This file is part of FEM on Colab-related actions.
#
# SPDX-License-Identifier: MIT
"""Tests for the open_in_colab_workflow.replace_images_in_markdown package."""

import os
import typing

import pytest

from open_in_colab_workflow import replace_images_in_markdown


@pytest.fixture
def mock_images_as_base64(root_directory: str) -> typing.Dict[str, str]:
    """Return simplified version of the base64 encoding."""
    images_as_base64 = dict()
    for image_name in ("black.png", "blue.svg", "red.jpg"):
        image_path = os.path.join(root_directory, "tests", "data", "replace_images_in_markdown", "images", image_name)
        images_as_base64[image_path] = f"Base64 of {image_name}"
    return images_as_base64


def test_replace_images_in_markdown_via_markdown_tag(
    root_directory: str, open_notebook: typing.Callable, mock_images_as_base64: typing.Dict[str, str]
) -> None:
    """Test replacement of images in markdown notebook containing only an image defined via markdown tag."""
    nb = open_notebook("replace_images_in_markdown", "markdown_image")

    updated_cells = replace_images_in_markdown(nb.cells, os.path.dirname(nb._filename), mock_images_as_base64)
    assert len(updated_cells) == 1
    assert updated_cells[0].cell_type == "markdown"
    assert updated_cells[0].source == """This is the red image.
![Red](Base64 of red.jpg)"""


def test_replace_images_in_markdown_via_html_tag(
    root_directory: str, open_notebook: typing.Callable, mock_images_as_base64: typing.Dict[str, str]
) -> None:
    """Test replacement of images in markdown notebook containing only an image defined via html tag."""
    nb = open_notebook("replace_images_in_markdown", "html_image")

    updated_cells = replace_images_in_markdown(nb.cells, os.path.dirname(nb._filename), mock_images_as_base64)
    assert len(updated_cells) == 1
    assert updated_cells[0].cell_type == "markdown"
    assert updated_cells[0].source == """This is the black image.
<img src="Base64 of black.png" alt="Black">"""


def test_replace_images_in_markdown_via_html_and_markdown_tags(
    root_directory: str, open_notebook: typing.Callable, mock_images_as_base64: typing.Dict[str, str]
) -> None:
    """Test replacement of images in markdown notebook containing image defined via html or markdown tags."""
    nb = open_notebook("replace_images_in_markdown", "html_and_markdown_images")

    updated_cells = replace_images_in_markdown(nb.cells, os.path.dirname(nb._filename), mock_images_as_base64)
    assert len(updated_cells) == 2
    assert updated_cells[0].cell_type == "markdown"
    assert updated_cells[0].source == """This is the black image.
<img src="Base64 of black.png" alt="Black">
This is the red image.
![Red](Base64 of red.jpg)"""
    assert updated_cells[1].cell_type == "markdown"
    assert updated_cells[1].source == """This is the blue image.
![Blue](Base64 of blue.svg)"""


def test_replace_images_in_markdown_with_a_code_cell(
    root_directory: str, open_notebook: typing.Callable, mock_images_as_base64: typing.Dict[str, str]
) -> None:
    """Test replacement of images in a notebook containing both markdown and code."""
    nb = open_notebook("replace_images_in_markdown", "image_and_code")

    updated_cells = replace_images_in_markdown(nb.cells, os.path.dirname(nb._filename), mock_images_as_base64)
    assert len(updated_cells) == 2
    assert updated_cells[0].cell_type == "markdown"
    assert updated_cells[0].source == """This is the red image.
![Red](Base64 of red.jpg)"""
    assert updated_cells[1] == nb.cells[1]
