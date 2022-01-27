# Copyright (C) 2021-2022 by the FEM on Colab authors
#
# This file is part of FEM on Colab-related actions.
#
# SPDX-License-Identifier: MIT
"""Determine where the notebooks should be published."""

import abc

from open_in_colab_workflow.get_colab_drive_url import get_colab_drive_url
from open_in_colab_workflow.get_colab_github_url import get_colab_github_url


class PublishOnBaseClass(abc.ABC):
    """Base class for three possible publish_on options."""

    @abc.abstractmethod
    def get_url(self, relative_path: str) -> str:
        """Get the URL used by this publisher and associated to a file at the provied relative path."""
        pass


class PublishOnArtifact(PublishOnBaseClass):
    """Store artifact publisher and its name."""

    def __init__(self, name: str) -> None:
        self.name = name

    def get_url(self, relative_path: str) -> str:
        """Throw an error."""
        raise RuntimeError("This method should never be called, as no URL is required when publishing to artifacts")


class PublishOnDrive(PublishOnBaseClass):
    """Store Google Drive publisher and its root directory."""

    def __init__(self, drive_root_directory: str) -> None:
        self.drive_root_directory = drive_root_directory

    def get_url(self, relative_path: str) -> str:
        """Get the URL used by Google Colab when the file at the provided relative path is stored on Google Drive."""
        return get_colab_drive_url(relative_path, self.drive_root_directory)


class PublishOnGitHub(PublishOnBaseClass):
    """Store GitHub repository publisher and its branch."""

    def __init__(self, repository: str, branch: str) -> None:
        self.repository = repository
        self.branch = branch

    def get_url(self, relative_path: str) -> str:
        """Get the URL used by Google Colab when the file at the provided relative path is stored on GitHub."""
        return get_colab_github_url(relative_path, self.repository, self.branch)


def publish_on(publish_on_str: str) -> PublishOnBaseClass:
    """Transform a string containing the publishing options to its corresponding class."""
    if publish_on_str.startswith("artifact"):
        publisher, name = publish_on_str.split("@")
        assert publisher == "artifact"
        return PublishOnArtifact(name)
    elif publish_on_str.startswith("drive"):
        publisher, drive_root_directory = publish_on_str.split("@")
        assert publisher == "drive"
        return PublishOnDrive(drive_root_directory)
    elif publish_on_str.startswith("github"):
        publisher, repository, branch = publish_on_str.split("@")
        assert publisher == "github"
        return PublishOnGitHub(repository, branch)
    else:
        raise RuntimeError("Invalid publish_on attribute")
