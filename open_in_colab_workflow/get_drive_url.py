# Copyright (C) 2021-2022 by the FEM on Colab authors
#
# This file is part of FEM on Colab-related actions.
#
# SPDX-License-Identifier: MIT
"""Get the URL that a file will have on Google Drive."""

import os
import typing

import docker

from open_in_colab_workflow.get_rclone_env import get_rclone_env


def get_drive_url(relative_path: str, drive_root_directory: str) -> typing.Optional[str]:
    """Get the URL that a file will have on Google Drive."""
    try:
        url = _get_url_with_rclone(relative_path, drive_root_directory)
    except docker.errors.ContainerError:
        url = None
    return url


def _get_url_with_rclone(relative_path: str, drive_root_directory: str) -> str:
    """
    Run a temporary rclone docker image to get the URL of a file on Google Drive.

    This function may raise a docker ContainerError if the file is not present on Google Drive.
    Such error should be handled by the caller.
    """
    rclone_env = get_rclone_env()
    client = docker.from_env()
    url = client.containers.run(
        "rclone/rclone", f"-q link colab:{os.path.join(drive_root_directory, relative_path)}",
        environment=rclone_env, remove=True
    ).decode("utf-8").strip("\n")
    assert "\n" not in url
    return url
