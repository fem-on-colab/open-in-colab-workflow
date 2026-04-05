# Copyright (C) 2021-2026 by the FEM on Colab authors
#
# This file is part of FEM on Colab-related actions.
#
# SPDX-License-Identifier: MIT
"""Download all files matching at least one pattern to Google Drive."""

import subprocess
import sys

from open_in_cloud_workflow.get_rclone_env import get_rclone_env
from open_in_cloud_workflow.publish_on import publish_on, PublishOnDrive


def download_files_from_google_drive(
    work_dir: str, pattern: str, drive_root_directory: str
) -> None:
    """Download all files matching at least one pattern to Google Drive."""
    subprocess.check_call(
        (
            f"rclone -q sync drive:{drive_root_directory} {work_dir} "
            + " ".join(
                f"--include {pattern_}"
                for pattern_ in pattern.strip("\n").split("\n")
            )
        ).split(" "),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        env=get_rclone_env(),
    )


if __name__ == "__main__":  # pragma: no cover
    assert len(sys.argv) == 4
    work_dir = sys.argv[1]
    download_pattern = sys.argv[2]
    publisher = publish_on(sys.argv[3])
    assert isinstance(publisher, PublishOnDrive)

    download_files_from_google_drive(
        work_dir, download_pattern, publisher.drive_root_directory
    )
