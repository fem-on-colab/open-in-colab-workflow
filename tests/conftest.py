# Copyright (C) 2021-2026 by the FEM on Colab authors
#
# This file is part of FEM on Colab-related actions.
#
# SPDX-License-Identifier: MIT
"""Definition of fixtures used by more than one file."""

import os
import typing

import _pytest.fixtures
import nbformat
import pytest

from open_in_cloud_workflow.publish_on import (
    publish_on, PublishOnArtifact, PublishOnBaseClass, PublishOnDrive, PublishOnGitHub)


@pytest.fixture
def root_directory() -> str:
    """Return the root directory of the repository."""
    return os.path.dirname(os.path.dirname(__file__))


@pytest.fixture
def open_notebook(root_directory: str) -> typing.Callable[[str, str, str | None], nbformat.NotebookNode]:
    """Return a fixture to open a local notebook."""
    def _(  local_directory: str, filename: str, data_directory: str | None = None) -> nbformat.NotebookNode:
        """Open notebook with nbformat."""
        if data_directory is None:
            data_directory = os.path.join(root_directory, "tests", "data")
        filename = os.path.join(data_directory, local_directory, filename + ".ipynb")
        with open(filename) as f:
            nb = nbformat.read(f, as_version=4)  # type: ignore[no-untyped-call]
        return nb  # type: ignore[no-any-return]
    return _


@pytest.fixture
def publish_on_artifact() -> PublishOnArtifact:
    """Return an artifact publisher."""
    return publish_on("artifact@open-in-colab")  # type: ignore[return-value]


@pytest.fixture
def publish_on_drive() -> PublishOnDrive:
    """Return a Google Drive publisher."""
    return publish_on("drive@GitHub/open_in_colab_workflow")  # type: ignore[return-value]


@pytest.fixture
def publish_on_github() -> PublishOnGitHub:
    """Return a GitHub publisher."""
    return publish_on("github@fem-on-colab/open-in-colab-workflow@open-in-colab")  # type: ignore[return-value]


@pytest.fixture(params=["publish_on_artifact", "publish_on_drive", "publish_on_github"])
def publisher(request: _pytest.fixtures.SubRequest) -> PublishOnBaseClass:
    """Parameterize over publishers."""
    if request.param == "publish_on_drive" and "RCLONE_CONFIG_DRIVE_TOKEN" not in os.environ:
        pytest.skip("Missing rclone environment variables")
    return request.getfixturevalue(request.param)  # type: ignore[no-any-return]
