# Copyright (C) 2021-2022 by the FEM on Colab authors
#
# This file is part of FEM on Colab-related actions.
#
# SPDX-License-Identifier: MIT
"""Definition of fixtures used by more than one file."""

import os
import typing

import nbformat
import pytest

from open_in_colab_workflow.publish_on import publish_on, PublishOnArtifact, PublishOnDrive, PublishOnGitHub


@pytest.fixture
def root_directory() -> str:
    """Return the root directory of the repository."""
    return os.path.dirname(os.path.dirname(__file__))


@pytest.fixture
def open_notebook(root_directory: str) -> typing.Callable:
    """Return a fixture to open a local notebook."""
    def _(local_directory: str, filename: str) -> nbformat.NotebookNode:
        """Open notebook with nbformat."""
        filename = os.path.join(root_directory, "tests", "data", local_directory, filename + ".ipynb")
        with open(filename, "r") as f:
            nb = nbformat.read(f, as_version=4)
        nb._filename = filename
        return nb
    return _


@pytest.fixture
def publish_on_artifact() -> PublishOnArtifact:
    """Return an artifact publisher."""
    return publish_on("artifact@open-in-colab")


@pytest.fixture
def publish_on_drive() -> PublishOnDrive:
    """Return a Google Drive publisher."""
    return publish_on("drive@GitHub/open_in_colab_workflow")


@pytest.fixture
def publish_on_github() -> PublishOnGitHub:
    """Return a GitHub publisher."""
    return publish_on("github@fem-on-colab/open-in-colab-workflow@open-in-colab")
