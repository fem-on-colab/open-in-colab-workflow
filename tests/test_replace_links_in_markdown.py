# Copyright (C) 2021-2023 by the FEM on Colab authors
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
def mock_links_replacement(root_directory: str) -> typing.Dict[str, typing.Optional[str]]:
    """Return simplified version of the links replacement dictionary."""
    data_subdirectory = os.path.join(root_directory, "tests", "data", "replace_links_in_markdown")
    return {
        os.path.join(data_subdirectory, "main_notebook.ipynb"): "Link to main_notebook.ipynb",
        os.path.join(data_subdirectory, "html_link_double_quotes.ipynb"): "This link should have not been used",
        os.path.join(data_subdirectory, "html_link_single_quotes.ipynb"): "This link should have not been used",
        os.path.join(data_subdirectory, "markdown_link.ipynb"): "This link should have not been used"
    }


def test_replace_links_in_markdown_via_markdown_tag(
    root_directory: str, open_notebook: typing.Callable[[str, str], nbformat.NotebookNode],
    mock_links_replacement: typing.Dict[str, typing.Optional[str]]
) -> None:
    """Test replacement of links in markdown notebook containing only a link defined via markdown tag."""
    nb = open_notebook("replace_links_in_markdown", "markdown_link")

    updated_cells = replace_links_in_markdown(nb.cells, os.path.dirname(nb._filename), mock_links_replacement)
    assert len(updated_cells) == 1
    assert updated_cells[0].cell_type == "markdown"
    assert updated_cells[0].source == "[Link to the main notebook](Link to main_notebook.ipynb)"


def test_replace_images_in_markdown_via_html_tag_single_quotes(
    root_directory: str, open_notebook: typing.Callable[[str, str], nbformat.NotebookNode],
    mock_links_replacement: typing.Dict[str, typing.Optional[str]]
) -> None:
    """Test replacement of links in markdown notebook containing only a defined via an html tag with single quotes."""
    nb = open_notebook("replace_links_in_markdown", "html_link_single_quotes")

    updated_cells = replace_links_in_markdown(nb.cells, os.path.dirname(nb._filename), mock_links_replacement)
    assert len(updated_cells) == 1
    assert updated_cells[0].cell_type == "markdown"
    assert updated_cells[0].source == "<a href='Link to main_notebook.ipynb'>Link to the main notebook</a>"


def test_replace_images_in_markdown_via_html_tag_double_quotes(
    root_directory: str, open_notebook: typing.Callable[[str, str], nbformat.NotebookNode],
    mock_links_replacement: typing.Dict[str, typing.Optional[str]]
) -> None:
    """Test replacement of links in markdown notebook containing only a defined via an html tag with double quotes."""
    nb = open_notebook("replace_links_in_markdown", "html_link_double_quotes")

    updated_cells = replace_links_in_markdown(nb.cells, os.path.dirname(nb._filename), mock_links_replacement)
    assert len(updated_cells) == 1
    assert updated_cells[0].cell_type == "markdown"
    assert updated_cells[0].source == '<a href="Link to main_notebook.ipynb">Link to the main notebook</a>'


def test_replace_links_in_markdown_with_a_code_cell(
    root_directory: str, open_notebook: typing.Callable[[str, str], nbformat.NotebookNode],
    mock_links_replacement: typing.Dict[str, typing.Optional[str]]
) -> None:
    """Test replacement of links in a notebook containing both markdown and code."""
    nb = open_notebook("replace_links_in_markdown", "link_and_code")

    updated_cells = replace_links_in_markdown(nb.cells, os.path.dirname(nb._filename), mock_links_replacement)
    assert len(updated_cells) == 2
    assert updated_cells[0].cell_type == "markdown"
    assert updated_cells[0].source == "[Link to the main notebook](Link to main_notebook.ipynb)"
    assert updated_cells[1] == nb.cells[1]


def test_replace_links_in_markdown_main(
    root_directory: str, open_notebook: typing.Callable[[str, str, str], nbformat.NotebookNode],
    publisher: PublishOnBaseClass
) -> None:
    """Test replacement of links when running the module as a script."""
    data_directory = os.path.join(root_directory, "tests", "data")
    nb_pattern = os.path.join("replace_links_in_markdown", "*.ipynb")
    main_notebook_pattern = nb_pattern.replace("*", "main_notebook")
    test_notebook_pattern = nb_pattern.replace("*", "markdown_link")

    with tempfile.TemporaryDirectory(dir=data_directory) as tmp_data_directory:
        os.mkdir(os.path.dirname(os.path.join(tmp_data_directory, nb_pattern)))
        shutil.copyfile(
            os.path.join(data_directory, main_notebook_pattern),
            os.path.join(tmp_data_directory, main_notebook_pattern))
        shutil.copyfile(
            os.path.join(data_directory, test_notebook_pattern),
            os.path.join(tmp_data_directory, test_notebook_pattern))
        replace_links_in_markdown_main(tmp_data_directory, nb_pattern, "colab", publisher)

        updated_nb = open_notebook(
            os.path.dirname(test_notebook_pattern), os.path.basename(test_notebook_pattern).replace(".ipynb", ""),
            tmp_data_directory)
        assert len(updated_nb.cells) == 1
        assert updated_nb.cells[0].cell_type == "markdown"
        if isinstance(publisher, PublishOnArtifact):
            assert updated_nb.cells[0].source == "[Link to the main notebook](main_notebook.ipynb)"
        elif isinstance(publisher, PublishOnDrive):
            assert updated_nb.cells[0].source == (
                "[Link to the main notebook]"
                "(https://colab.research.google.com/drive/1lccx0xSlkAsX53sK0KboPWSW6kzqWG6Z)")
        elif isinstance(publisher, PublishOnGitHub):
            assert updated_nb.cells[0].source == (
                "[Link to the main notebook]"
                "(https://colab.research.google.com/github/fem-on-colab/open-in-colab-workflow/blob/open-in-colab/"
                "replace_links_in_markdown/main_notebook.ipynb)")
        else:
            raise RuntimeError("Invalid publisher")
