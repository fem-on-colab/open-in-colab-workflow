# Copyright (C) 2021-2022 by the FEM on Colab authors
#
# This file is part of FEM on Colab-related actions.
#
# SPDX-License-Identifier: MIT
"""Replace images with their base64 representation."""

import copy
import os
import typing

import nbformat


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
