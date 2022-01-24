# Copyright (C) 2021-2022 by the FEM on Colab authors
#
# This file is part of FEM on Colab-related actions.
#
# SPDX-License-Identifier: MIT
"""Get absolute path of all notebooks in the work directory which match a pattern."""

import glob
import os
import typing


def glob_notebooks(work_dir: str, nb_pattern: str) -> typing.Set[str]:
    """Get absolute path of all notebooks in the work directory which match a pattern."""
    return {f for f in glob.glob(os.path.join(work_dir, nb_pattern), recursive=True)}
