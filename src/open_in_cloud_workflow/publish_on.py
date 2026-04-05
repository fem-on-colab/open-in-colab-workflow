# Copyright (C) 2021-2026 by the FEM on Colab authors
#
# This file is part of FEM on Colab-related actions.
#
# SPDX-License-Identifier: MIT
"""Determine where the notebooks should be published."""

import abc
import sys

from open_in_cloud_workflow.get_colab_drive_url import get_colab_drive_url
from open_in_cloud_workflow.get_colab_github_url import get_colab_github_url
from open_in_cloud_workflow.get_kaggle_drive_url import get_kaggle_drive_url
from open_in_cloud_workflow.get_kaggle_github_url import get_kaggle_github_url


class PublishOnBaseClass(abc.ABC):
    """Base class for three possible publish_on options."""

    @abc.abstractmethod
    def get_url(
        self, cloud_provider: str, relative_path: str
    ) -> str | None:  # pragma: no cover
        """Get the publisher URL associated with a relative path."""
        pass

    @abc.abstractmethod
    def __str__(self) -> str:  # pragma: no cover
        """Print private attributes, one `name=value` pair per line."""
        pass


class PublishOnArtifact(PublishOnBaseClass):
    """Store artifact publisher and its name."""

    def __init__(self, name: str) -> None:
        """Initialize the artifact publisher with its name."""
        self.name = name

    def get_url(self, cloud_provider: str, relative_path: str) -> str:
        """Throw an error."""
        raise RuntimeError(
            "This method should never be called: artifacts do not need URLs"
        )

    def __str__(self) -> str:
        """Print private attributes, one `name=value` pair per line."""
        return f"""publisher=artifact
name={self.name}"""


class PublishOnDrive(PublishOnBaseClass):
    """Store Google Drive publisher and its root directory."""

    def __init__(self, drive_root_directory: str) -> None:
        """Initialize the Google Drive publisher with its root directory."""
        self.drive_root_directory = drive_root_directory

    def get_url(self, cloud_provider: str, relative_path: str) -> str | None:
        """Get cloud URL for a file stored on Google Drive."""
        assert cloud_provider in ("colab", "kaggle")
        if cloud_provider == "colab":
            return get_colab_drive_url(relative_path, self.drive_root_directory)
        elif cloud_provider == "kaggle":
            return get_kaggle_drive_url(
                relative_path, self.drive_root_directory
            )
        else:  # pragma: no cover
            raise RuntimeError("Invalid cloud provider")

    def __str__(self) -> str:
        """Print private attributes, one `name=value` pair per line."""
        return f"""publisher=drive
drive_root_directory={self.drive_root_directory}"""


class PublishOnEmpty(PublishOnBaseClass):
    """Store empty publisher."""

    def __init__(self) -> None:
        """Initialize the empty publisher."""
        pass

    def get_url(self, cloud_provider: str, relative_path: str) -> str:
        """Throw an error."""
        raise RuntimeError(
            "This method should never be called: empty publisher never "
            "publishes anything and thus does not need URLs"
        )

    def __str__(self) -> str:
        """Print private attributes, one `name=value` pair per line."""
        return "publisher=empty"


class PublishOnGitHub(PublishOnBaseClass):
    """Store GitHub repository publisher and its branch."""

    def __init__(self, repository: str, branch: str) -> None:
        """Initialize the GitHub publisher with repository and branch."""
        self.repository = repository
        self.branch = branch

    def get_url(self, cloud_provider: str, relative_path: str) -> str:
        """Get cloud URL for a file stored on GitHub."""
        assert cloud_provider in ("colab", "kaggle")
        if cloud_provider == "colab":
            return get_colab_github_url(
                relative_path, self.repository, self.branch
            )
        elif cloud_provider == "kaggle":
            return get_kaggle_github_url(
                relative_path, self.repository, self.branch
            )
        else:  # pragma: no cover
            raise RuntimeError("Invalid cloud provider")

    def __str__(self) -> str:
        """Print private attributes, one `name=value` pair per line."""
        return f"""publisher=github
repository={self.repository}
branch={self.branch}"""


def publish_on(publish_on_str: str) -> PublishOnBaseClass:
    """Parse publishing options and return the corresponding class."""
    if len(publish_on_str) == 0:
        return PublishOnEmpty()
    elif publish_on_str.startswith("artifact"):
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
    else:  # pragma: no cover
        raise RuntimeError("Invalid publish_on attribute")


if __name__ == "__main__":  # pragma: no cover
    assert len(sys.argv) == 2
    publisher = publish_on(sys.argv[1])
    print(publisher)
