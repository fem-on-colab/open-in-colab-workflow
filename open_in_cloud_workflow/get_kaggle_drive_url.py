# Copyright (C) 2021-2026 by the FEM on Colab authors
#
# This file is part of FEM on Colab-related actions.
#
# SPDX-License-Identifier: MIT
"""Get the URL that a file will have on Kaggle when hosted on Google Drive."""


from open_in_cloud_workflow.get_drive_url import get_drive_url


def get_kaggle_drive_url(relative_path: str, drive_root_directory: str) -> str | None:
    """Get the URL that a file will have on Kaggle when hosted on Google Drive."""
    drive_url = get_drive_url(relative_path, drive_root_directory)
    if drive_url is not None:
        return drive_url.replace(
            "https://drive.google.com/open?id=",
            "https://kaggle.com/kernels/welcome?src=https://drive.google.com/uc?id=")
    else:
        return None
