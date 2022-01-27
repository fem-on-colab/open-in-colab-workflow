# Copyright (C) 2021-2022 by the FEM on Colab authors
#
# This file is part of FEM on Colab-related actions.
#
# SPDX-License-Identifier: MIT
"""Replace links to local file in markdown with links to the corresponding Colab notebooks."""

import copy
import os
import typing

import nbformat


def replace_links_in_markdown(
    nb_cells: typing.List[nbformat.NotebookNode], nb_dir: str, links_replacement: typing.Dict[str, str]
) -> typing.List[nbformat.NotebookNode]:
    """Replace links to local file in markdown with links to the corresponding Colab notebooks."""
    add_quotes_or_parentheses = (
        lambda text: '"' + text + '"',
        lambda text: "'" + text + "'",
        lambda text: "(" + text + ")"
    )
    updated_nb_cells = list()
    for cell in nb_cells:
        if cell.cell_type == "markdown":
            updated_cell = copy.deepcopy(cell)
            for (local_link, colab_link) in links_replacement.items():
                for preprocess in add_quotes_or_parentheses:
                    updated_cell.source = updated_cell.source.replace(
                        preprocess(os.path.relpath(local_link, nb_dir)), preprocess(colab_link))
            updated_nb_cells.append(updated_cell)
        else:
            updated_nb_cells.append(cell)
    return updated_nb_cells
