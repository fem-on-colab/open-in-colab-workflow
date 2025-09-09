# Copyright (C) 2021-2025 by the FEM on Colab authors
#
# This file is part of FEM on Colab-related actions.
#
# SPDX-License-Identifier: MIT
"""Tests for the open_in_cloud_workflow.replace_links_in_markdown package."""

import os
import shutil
import tempfile
import typing

import nbformat
import pytest

from open_in_cloud_workflow.publish_on import PublishOnArtifact, PublishOnBaseClass, PublishOnDrive, PublishOnGitHub
from open_in_cloud_workflow.replace_links_in_markdown import (
    __main__ as replace_links_in_markdown_main, replace_links_in_markdown)


@pytest.fixture
def mock_links_replacement() -> dict[str, str | None]:
    """Return simplified version of the links replacement dictionary."""
    return {
        "main_notebook.ipynb": "Link to main_notebook.ipynb",
        "html_link_double_quotes.ipynb": "This link should have not been used",
        "html_link_single_quotes.ipynb": "This link should have not been used",
        "markdown_link.ipynb": "This link should have not been used"
    }


def test_replace_links_in_markdown_via_markdown_tag(
    root_directory: str, open_notebook: typing.Callable[[str, str], nbformat.NotebookNode],
    mock_links_replacement: dict[str, str | None]
) -> None:
    """Test replacement of links in markdown notebook containing only a link defined via markdown tag."""
    nb = open_notebook("replace_links_in_markdown", "markdown_link")

    updated_cells = replace_links_in_markdown(nb.cells, mock_links_replacement)
    assert len(updated_cells) == 1
    assert updated_cells[0].cell_type == "markdown"
    assert updated_cells[0].source == "[Link to the main notebook](Link to main_notebook.ipynb)"


def test_replace_links_in_markdown_via_html_tag_single_quotes(
    root_directory: str, open_notebook: typing.Callable[[str, str], nbformat.NotebookNode],
    mock_links_replacement: dict[str, str | None]
) -> None:
    """Test replacement of links in markdown notebook containing only a defined via an html tag with single quotes."""
    nb = open_notebook("replace_links_in_markdown", "html_link_single_quotes")

    updated_cells = replace_links_in_markdown(nb.cells, mock_links_replacement)
    assert len(updated_cells) == 1
    assert updated_cells[0].cell_type == "markdown"
    assert updated_cells[0].source == "<a href='Link to main_notebook.ipynb'>Link to the main notebook</a>"


def test_replace_links_in_markdown_via_html_tag_double_quotes(
    root_directory: str, open_notebook: typing.Callable[[str, str], nbformat.NotebookNode],
    mock_links_replacement: dict[str, str | None]
) -> None:
    """Test replacement of links in markdown notebook containing only a defined via an html tag with double quotes."""
    nb = open_notebook("replace_links_in_markdown", "html_link_double_quotes")

    updated_cells = replace_links_in_markdown(nb.cells, mock_links_replacement)
    assert len(updated_cells) == 1
    assert updated_cells[0].cell_type == "markdown"
    assert updated_cells[0].source == '<a href="Link to main_notebook.ipynb">Link to the main notebook</a>'


def test_replace_links_in_markdown_with_a_code_cell(
    root_directory: str, open_notebook: typing.Callable[[str, str], nbformat.NotebookNode],
    mock_links_replacement: dict[str, str | None]
) -> None:
    """Test replacement of links in a notebook containing both markdown and code."""
    nb = open_notebook("replace_links_in_markdown", "link_and_code")

    updated_cells = replace_links_in_markdown(nb.cells, mock_links_replacement)
    assert len(updated_cells) == 2
    assert updated_cells[0].cell_type == "markdown"
    assert updated_cells[0].source == "[Link to the main notebook](Link to main_notebook.ipynb)"
    assert updated_cells[1] == nb.cells[1]


def test_replace_links_in_markdown_main(
    root_directory: str, open_notebook: typing.Callable[[str, str, str], nbformat.NotebookNode],
    publisher: PublishOnBaseClass
) -> None:
    """Test replacement of links when running the module as a script."""
    data_subdirectory = os.path.join("tests", "data", "replace_links_in_markdown")
    pattern = os.path.join(data_subdirectory, "*.ipynb")
    test_notebooks = {
        "markdown_link": {
            PublishOnArtifact: "[Link to the main notebook](main_notebook.ipynb)",
            PublishOnDrive: (
                "[Link to the main notebook]("
                + "https://colab.research.google.com/drive/1lccx0xSlkAsX53sK0KboPWSW6kzqWG6Z)"
            ),
            PublishOnGitHub: (
                "[Link to the main notebook]("
                + "https://colab.research.google.com/github/fem-on-colab/open-in-colab-workflow/blob/"
                + "open-in-colab/tests/data/replace_links_in_markdown/main_notebook.ipynb)"
            )
        },
        "html_link_single_quotes": {
            PublishOnArtifact: "<a href='main_notebook.ipynb'>Link to the main notebook</a>",
            PublishOnDrive: (
                "<a href='https://colab.research.google.com/drive/1lccx0xSlkAsX53sK0KboPWSW6kzqWG6Z'>"
                + "Link to the main notebook</a>"
            ),
            PublishOnGitHub: (
                "<a href='https://colab.research.google.com/github/fem-on-colab/open-in-colab-workflow/blob/"
                + "open-in-colab/tests/data/replace_links_in_markdown/main_notebook.ipynb'>"
                + "Link to the main notebook</a>"
            )
        },
        "html_link_double_quotes": {
            PublishOnArtifact: '<a href="main_notebook.ipynb">Link to the main notebook</a>',
            PublishOnDrive: (
                '<a href="https://colab.research.google.com/drive/1lccx0xSlkAsX53sK0KboPWSW6kzqWG6Z">'
                + "Link to the main notebook</a>"
            ),
            PublishOnGitHub: (
                '<a href="https://colab.research.google.com/github/fem-on-colab/open-in-colab-workflow/blob/'
                + 'open-in-colab/tests/data/replace_links_in_markdown/main_notebook.ipynb">'
                + "Link to the main notebook</a>"
            )
        },
        "link_and_code": {
            PublishOnArtifact: "[Link to the main notebook](main_notebook.ipynb)",
            PublishOnDrive: (
                "[Link to the main notebook]("
                + "https://colab.research.google.com/drive/1lccx0xSlkAsX53sK0KboPWSW6kzqWG6Z)"
            ),
            PublishOnGitHub: (
                "[Link to the main notebook]("
                + "https://colab.research.google.com/github/fem-on-colab/open-in-colab-workflow/blob/"
                + "open-in-colab/tests/data/replace_links_in_markdown/main_notebook.ipynb)"
            )
        }
    }

    with tempfile.TemporaryDirectory(dir=root_directory) as tmp_root_directory:
        os.makedirs(os.path.join(tmp_root_directory, data_subdirectory))
        # Copy all test notebooks
        for nb_name in [*test_notebooks.keys(), "main_notebook"]:
            shutil.copyfile(
                os.path.join(root_directory, data_subdirectory, f"{nb_name}.ipynb"),
                os.path.join(tmp_root_directory, data_subdirectory, f"{nb_name}.ipynb")
            )
        # Run the replacement script
        replace_links_in_markdown_main(tmp_root_directory, pattern, "colab", publisher)
        # Validate each notebook
        for nb_name, expected in test_notebooks.items():
            updated_nb = open_notebook(
                "replace_links_in_markdown", nb_name, os.path.join(tmp_root_directory, "tests", "data"))
            assert updated_nb.cells[0].cell_type == "markdown"
            assert updated_nb.cells[0].source == expected[type(publisher)]
