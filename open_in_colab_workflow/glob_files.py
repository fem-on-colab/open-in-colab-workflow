# Copyright (C) 2021-2022 by the FEM on Colab authors
#
# This file is part of FEM on Colab-related actions.
#
# SPDX-License-Identifier: MIT
"""Get absolute path of all files in the work directory which match at least one patterns."""

import glob
import os
import typing


def glob_files(work_dir: str, pattern: str) -> typing.Set[str]:
    """Get absolute path of all files in the work directory which match at least one pattern."""
    pattern = pattern.split("\n")
    return set().union(*[
        {f for f in glob.glob(os.path.join(work_dir, pattern_), recursive=True)} for pattern_ in pattern
    ])
