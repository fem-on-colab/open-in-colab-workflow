# Copyright (C) 2021-2026 by the FEM on Colab authors
#
# This file is part of FEM on Colab-related actions.
#
# SPDX-License-Identifier: MIT
"""Determine the source of the bookes."""

import abc
import sys


class SourceFromBaseClass(abc.ABC):
    """Base class for three possible source_from options."""

    @abc.abstractmethod
    def __str__(self) -> str:  # pragma: no cover
        """Print private attributes as attribute_name=attribute_value, one attribute per line."""
        pass


class SourceFromDrive(SourceFromBaseClass):
    """Store Google Drive source and its root directory."""

    def __init__(self, drive_root_directory: str) -> None:
        self.drive_root_directory = drive_root_directory

    def __str__(self) -> str:
        """Print private attributes as attribute_name=attribute_value, one attribute per line."""
        return f"""source=drive
drive_root_directory={self.drive_root_directory}"""


class SourceFromGitHub(SourceFromBaseClass):
    """Store GitHub repository source and its branch."""

    def __init__(self, repository: str, branch: str) -> None:
        self.repository = repository
        self.branch = branch

    def __str__(self) -> str:
        """Print private attributes as attribute_name=attribute_value, one attribute per line."""
        return f"""source=github
repository={self.repository}
branch={self.branch}"""


def source_from(source_from_str: str) -> SourceFromBaseClass:
    """Transform a string containing the source options to its corresponding class."""
    if source_from_str.startswith("drive"):
        source, drive_root_directory = source_from_str.split("@")
        assert source == "drive"
        return SourceFromDrive(drive_root_directory)
    elif source_from_str.startswith("github"):
        source, repository, branch = source_from_str.split("@")
        assert source == "github"
        return SourceFromGitHub(repository, branch)
    else:  # pragma: no cover
        raise RuntimeError("Invalid source_from attribute")


if __name__ == "__main__":  # pragma: no cover
    assert len(sys.argv) in (1, 2)
    if len(sys.argv) == 1:
        source = source_from("github@caller-repository@caller-branch")
    elif len(sys.argv) == 2:
        source = source_from(sys.argv[1])
    print(source)
