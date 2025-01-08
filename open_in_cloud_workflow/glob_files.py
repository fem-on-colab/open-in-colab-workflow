# Copyright (C) 2021-2025 by the FEM on Colab authors
#
# This file is part of FEM on Colab-related actions.
#
# SPDX-License-Identifier: MIT
"""Get absolute path of all files in the work directory which match at least one patterns."""

import glob
import os


def glob_files(work_dir: str, pattern: str) -> set[str]:
    """Get absolute path of all files in the work directory which match at least one pattern."""
    assert work_dir.startswith(os.sep), "Please provide the absolute path of the work directory."
    patterns = pattern.strip("\n").split("\n")
    return set().union(*[
        {f for f in glob.glob(os.path.join(work_dir, pattern_), recursive=True)} for pattern_ in patterns
    ])
