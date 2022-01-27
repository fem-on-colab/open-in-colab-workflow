# Copyright (C) 2021-2022 by the FEM on Colab authors
#
# This file is part of FEM on Colab-related actions.
#
# SPDX-License-Identifier: MIT
"""Upload all files matching at least one pattern to Google Drive."""

import docker

from open_in_colab_workflow.get_rclone_env import get_rclone_env


def upload_files_to_google_drive(work_dir: str, pattern: str, drive_root_directory: str) -> None:
    """Upload all files matching at least one pattern to Google Drive."""
    for pattern_ in pattern.split("\n"):
        _upload_files_with_rclone(work_dir, pattern_, drive_root_directory)


def _upload_files_with_rclone(work_dir: str, pattern: str, drive_root_directory: str) -> None:
    """
    Run a temporary rclone docker image to upload a file on Google Drive.

    This function may raise a docker ContainerError if an error occurs during the upload.
    Such error should be handled by the caller.
    """
    rclone_env = get_rclone_env()
    volumes = {
        work_dir: {"bind": "/data", "mode": "ro"}
    }
    client = docker.from_env()
    client.containers.run(
        "rclone/rclone", f"-q copy /data colab:{drive_root_directory} --include {pattern}",
        environment=rclone_env, volumes=volumes, remove=True
    )
