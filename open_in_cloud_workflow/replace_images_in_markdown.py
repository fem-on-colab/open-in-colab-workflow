# Copyright (C) 2021-2025 by the FEM on Colab authors
#
# This file is part of FEM on Colab-related actions.
#
# SPDX-License-Identifier: MIT
"""Replace images with their base64 representation."""

import copy
import os
import sys

import nbformat

from open_in_cloud_workflow.glob_files import glob_files
from open_in_cloud_workflow.glob_images import glob_images


def replace_images_in_markdown(
    nb_cells: list[nbformat.NotebookNode], images_as_base64: dict[str, str]
) -> list[nbformat.NotebookNode]:
    """Replace images with their base64 representation, and return the updated cells."""
    updated_nb_cells = list()
    for cell in nb_cells:
        if cell.cell_type == "markdown":
            updated_cell = copy.deepcopy(cell)
            for (image_file, base64) in images_as_base64.items():
                updated_cell.source = updated_cell.source.replace(image_file, base64)
            updated_nb_cells.append(updated_cell)
        else:
            updated_nb_cells.append(cell)
    return updated_nb_cells


def __main__(work_dir: str, nb_pattern: str) -> None:  # noqa: N807
    """Replace images in every notebook in the work directory matching the prescribed pattern."""
    images_as_base64 = glob_images(work_dir)

    for nb_filename in glob_files(work_dir, nb_pattern):
        with open(nb_filename) as f:
            nb = nbformat.read(f, as_version=4)  # type: ignore[no-untyped-call]
        nb_dirname = os.path.dirname(nb_filename)
        nb_images_as_base64 = {
            os.path.relpath(os.path.join(work_dir, key), nb_dirname): value
            for key, value in images_as_base64.items()
        }
        nb.cells = replace_images_in_markdown(nb.cells, nb_images_as_base64)
        with open(nb_filename, "w") as f:
            nbformat.write(nb, f)  # type: ignore[no-untyped-call]


if __name__ == "__main__":  # pragma: no cover
    assert len(sys.argv) == 3
    __main__(*sys.argv[1:])
