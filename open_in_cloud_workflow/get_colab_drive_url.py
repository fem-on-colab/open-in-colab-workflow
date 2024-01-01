# Copyright (C) 2021-2024 by the FEM on Colab authors
#
# This file is part of FEM on Colab-related actions.
#
# SPDX-License-Identifier: MIT
"""Get the URL that a file will have on Google Colab when hosted on Google Drive."""

import typing

from open_in_cloud_workflow.get_drive_url import get_drive_url


def get_colab_drive_url(relative_path: str, drive_root_directory: str) -> typing.Optional[str]:
    """Get the URL that a file will have on Google Colab when hosted on Google Drive."""
    drive_url = get_drive_url(relative_path, drive_root_directory)
    if drive_url is not None:
        return drive_url.replace(
            "https://drive.google.com/open?id=", "https://colab.research.google.com/drive/")
    else:
        return None
