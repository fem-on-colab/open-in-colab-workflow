# Copyright (C) 2021-2022 by the FEM on Colab authors
#
# This file is part of FEM on Colab-related actions.
#
# SPDX-License-Identifier: MIT
"""Replace images with their base64 representation."""

import copy
import os
import sys
import typing

import nbformat

from open_in_colab_workflow.glob_files import glob_files
from open_in_colab_workflow.glob_images import glob_images


def replace_images_in_markdown(
    nb_cells: typing.List[nbformat.NotebookNode], nb_dir: str, images_as_base64: typing.Dict[str, str]
) -> typing.List[nbformat.NotebookNode]:
    """Replace images with their base64 representation, and return the updated cells."""
    updated_nb_cells = list()
    for cell in nb_cells:
        if cell.cell_type == "markdown":
            updated_cell = copy.deepcopy(cell)
            for (image_file, base64) in images_as_base64.items():
                updated_cell.source = updated_cell.source.replace(os.path.relpath(image_file, nb_dir), base64)
            updated_nb_cells.append(updated_cell)
        else:
            updated_nb_cells.append(cell)
    return updated_nb_cells


if __name__ == "__main__":  # pragma: no cover
    assert len(sys.argv) == 3
    work_dir = sys.argv[1]
    nb_pattern = sys.argv[2]

    images_as_base64 = glob_images(work_dir)

    for nb_filename in glob_files(work_dir, nb_pattern):
        with open(nb_filename, "r") as f:
            nb = nbformat.read(f, as_version=4)
        nb.cells = replace_images_in_markdown(nb.cells, os.path.dirname(nb_filename), images_as_base64)
        with open(nb_filename, "w") as f:
            nbformat.write(nb, f)
