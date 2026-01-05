# Copyright (C) 2021-2026 by the FEM on Colab authors
#
# This file is part of FEM on Colab-related actions.
#
# SPDX-License-Identifier: MIT
"""Tests for the open_in_cloud_workflow.replace_images_in_markdown package."""

import os
import shutil
import tempfile
import typing

import nbformat
import pytest

from open_in_cloud_workflow.replace_images_in_markdown import (
    __main__ as replace_images_in_markdown_main, replace_images_in_markdown)


@pytest.fixture
def mock_images_as_base64(root_directory: str) -> dict[str, str]:
    """Return simplified version of the base64 encoding."""
    return {
        os.path.join("images", image_name): f"Base64 of {image_name}"
        for image_name in ("black.png", "blue.svg", "red.jpg")
    }


def test_replace_images_in_markdown_via_markdown_tag(
    root_directory: str, open_notebook: typing.Callable[[str, str], nbformat.NotebookNode],
    mock_images_as_base64: dict[str, str]
) -> None:
    """Test replacement of images in markdown notebook containing only an image defined via markdown tag."""
    nb = open_notebook("replace_images_in_markdown", "markdown_image")

    updated_cells = replace_images_in_markdown(nb.cells, mock_images_as_base64)
    assert len(updated_cells) == 1
    assert updated_cells[0].cell_type == "markdown"
    assert updated_cells[0].source == """This is the red image.
![Red](Base64 of red.jpg)"""


def test_replace_images_in_markdown_via_html_tag(
    root_directory: str, open_notebook: typing.Callable[[str, str], nbformat.NotebookNode],
    mock_images_as_base64: dict[str, str]
) -> None:
    """Test replacement of images in markdown notebook containing only an image defined via html tag."""
    nb = open_notebook("replace_images_in_markdown", "html_image")

    updated_cells = replace_images_in_markdown(nb.cells, mock_images_as_base64)
    assert len(updated_cells) == 1
    assert updated_cells[0].cell_type == "markdown"
    assert updated_cells[0].source == """This is the black image.
<img src="Base64 of black.png" alt="Black">"""


def test_replace_images_in_markdown_via_html_and_markdown_tags(
    root_directory: str, open_notebook: typing.Callable[[str, str], nbformat.NotebookNode],
    mock_images_as_base64: dict[str, str]
) -> None:
    """Test replacement of images in markdown notebook containing image defined via html or markdown tags."""
    nb = open_notebook("replace_images_in_markdown", "html_and_markdown_images")

    updated_cells = replace_images_in_markdown(nb.cells, mock_images_as_base64)
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
    root_directory: str, open_notebook: typing.Callable[[str, str], nbformat.NotebookNode],
    mock_images_as_base64: dict[str, str]
) -> None:
    """Test replacement of images in a notebook containing both markdown and code."""
    nb = open_notebook("replace_images_in_markdown", "image_and_code")

    updated_cells = replace_images_in_markdown(nb.cells, mock_images_as_base64)
    assert len(updated_cells) == 2
    assert updated_cells[0].cell_type == "markdown"
    assert updated_cells[0].source == """This is the red image.
![Red](Base64 of red.jpg)"""
    assert updated_cells[1] == nb.cells[1]


def test_replace_images_in_markdown_main(
    root_directory: str, open_notebook: typing.Callable[[str, str, str], nbformat.NotebookNode]
) -> None:
    """Test replacement of images when running the module as a script."""
    data_subdirectory = os.path.join("tests", "data", "replace_images_in_markdown")
    pattern = os.path.join(data_subdirectory, "*.ipynb")
    test_notebooks: dict[str, list[str | tuple[str, ...] | None]] = {
        "markdown_image": [
            """This is the red image.
![Red](data:image/png;base64"""
        ],
        "html_image": [
            """This is the black image.
<img src="data:image/png;base64"""
        ],
        "html_and_markdown_images": [
            (
                """This is the black image.
<img src="data:image/png;base64""",
                """This is the red image.
![Red](data:image/png;base64"""
            ),
            """This is the blue image.
![Blue](data:image/png;base64"""
        ],
        "image_and_code": [
            """This is the red image.
![Red](data:image/png;base64""",
            None  # placeholder to indicate code cell remains unchanged
        ]
    }

    with tempfile.TemporaryDirectory(dir=root_directory) as tmp_root_directory:
        os.makedirs(os.path.join(tmp_root_directory, data_subdirectory, "images"))
        # Copy test notebooks and images
        for nb_name in test_notebooks.keys():
            shutil.copyfile(
                os.path.join(root_directory, data_subdirectory, f"{nb_name}.ipynb"),
                os.path.join(tmp_root_directory, data_subdirectory, f"{nb_name}.ipynb")
            )
        for img_file in os.listdir(os.path.join(root_directory, data_subdirectory, "images")):
            shutil.copyfile(
                os.path.join(root_directory, data_subdirectory, "images", img_file),
                os.path.join(tmp_root_directory, data_subdirectory, "images", img_file)
            )
        # Run the replacement script
        replace_images_in_markdown_main(tmp_root_directory, pattern)
        # Validate each notebook
        for nb_name, expected in test_notebooks.items():
            original_nb = open_notebook(
                "replace_images_in_markdown", nb_name, os.path.join(root_directory, "tests", "data"))
            updated_nb = open_notebook(
                "replace_images_in_markdown", nb_name, os.path.join(tmp_root_directory, "tests", "data"))
            assert len(updated_nb.cells) == len(expected)
            for c, expected_c in enumerate(expected):
                if expected_c is None:  # code cell
                    assert updated_nb.cells[c].cell_type == "code"
                    assert updated_nb.cells[c].source == original_nb.cells[c].source
                else:
                    assert updated_nb.cells[c].cell_type == "markdown"
                    if isinstance(expected_c, str):
                        assert updated_nb.cells[c].source.startswith(expected_c)
                    elif isinstance(expected_c, tuple):
                        for expected_c_part in expected_c:
                            assert isinstance(expected_c_part, str)
                            assert expected_c_part in updated_nb.cells[c].source
                    else:
                        raise ValueError("Invalid expected string")
