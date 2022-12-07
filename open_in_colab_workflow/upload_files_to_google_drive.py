# Copyright (C) 2021-2022 by the FEM on Colab authors
#
# This file is part of FEM on Colab-related actions.
#
# SPDX-License-Identifier: MIT
"""Upload all files matching at least one pattern to Google Drive."""

import subprocess
import sys

from open_in_colab_workflow.get_rclone_env import get_rclone_env
from open_in_colab_workflow.publish_on import publish_on, PublishOnDrive


def upload_files_to_google_drive(work_dir: str, pattern: str, drive_root_directory: str) -> None:
    """Upload all files matching at least one pattern to Google Drive."""
    for pattern_ in pattern.strip("\n").split("\n"):
        subprocess.check_call(
            f"rclone -q copy {work_dir} drive:{drive_root_directory} --include {pattern_}".split(" "),
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, env=get_rclone_env())


if __name__ == "__main__":  # pragma: no cover
    assert len(sys.argv) == 4
    work_dir = sys.argv[1]
    upload_pattern = sys.argv[2]
    publisher = publish_on(sys.argv[3])
    assert isinstance(publisher, PublishOnDrive)

    upload_files_to_google_drive(work_dir, upload_pattern, publisher.drive_root_directory)
