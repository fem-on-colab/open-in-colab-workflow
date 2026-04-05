# Copyright (C) 2021-2026 by the FEM on Colab authors
#
# This file is part of FEM on Colab-related actions.
#
# SPDX-License-Identifier: MIT
"""Collect absolute paths of files matching at least one pattern."""

import glob
import os


def glob_files(work_dir: str, pattern: str) -> set[str]:
    """Collect absolute paths of files matching at least one pattern."""
    assert work_dir.startswith(os.sep), (
        "Please provide the absolute path of the work directory."
    )
    return set().union(
        *[
            {
                f
                for f in glob.glob(
                    os.path.join(work_dir, pattern_), recursive=True
                )
            }
            for pattern_ in pattern.strip("\n").split("\n")
        ]
    )
