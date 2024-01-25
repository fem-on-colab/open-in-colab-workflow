# Copyright (C) 2021-2024 by the FEM on Colab authors
#
# This file is part of FEM on Colab-related actions.
#
# SPDX-License-Identifier: MIT
"""Get the URL that a file will have on Google Drive."""

import os
import subprocess

from open_in_cloud_workflow.get_rclone_env import get_rclone_env


def get_drive_url(relative_path: str, drive_root_directory: str) -> str | None:
    """Get the URL that a file will have on Google Drive."""
    try:
        return subprocess.run(
            f"rclone -q link drive:{os.path.join(drive_root_directory, relative_path)}".split(" "),
            capture_output=True, check=True, env=get_rclone_env()).stdout.decode("utf-8").strip("\n")
    except subprocess.CalledProcessError:  # pragma: no cover
        return None
