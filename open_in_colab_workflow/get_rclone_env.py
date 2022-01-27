# Copyright (C) 2021-2022 by the FEM on Colab authors
#
# This file is part of FEM on Colab-related actions.
#
# SPDX-License-Identifier: MIT
"""Get rclone environment variables."""

import os
import typing


def get_rclone_env() -> typing.Dict[str, str]:
    """Get rclone environment variables."""
    return {
        "RCLONE_CONFIG_COLAB_TYPE": "drive",
        "RCLONE_CONFIG_COLAB_SCOPE": "drive",
        "RCLONE_CONFIG_COLAB_CLIENT_ID": os.environ["RCLONE_CONFIG_COLAB_CLIENT_ID"],
        "RCLONE_CONFIG_COLAB_CLIENT_SECRET": os.environ["RCLONE_CONFIG_COLAB_CLIENT_SECRET"],
        "RCLONE_CONFIG_COLAB_TOKEN": os.environ["RCLONE_CONFIG_COLAB_TOKEN"]
    }
