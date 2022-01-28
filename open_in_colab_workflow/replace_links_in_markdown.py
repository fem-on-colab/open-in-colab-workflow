# Copyright (C) 2021-2022 by the FEM on Colab authors
#
# This file is part of FEM on Colab-related actions.
#
# SPDX-License-Identifier: MIT
"""Replace links to local file in markdown with links to the corresponding Colab notebooks."""

import copy
import os
import sys
import typing

import nbformat

from open_in_colab_workflow.glob_files import glob_files
from open_in_colab_workflow.glob_links import glob_links
from open_in_colab_workflow.publish_on import publish_on, PublishOnDrive
from open_in_colab_workflow.upload_files_to_google_drive import upload_files_to_google_drive


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


if __name__ == "__main__":  # pragma: no cover
    assert len(sys.argv) == 4
    work_dir = sys.argv[1]
    nb_pattern = sys.argv[2]
    publisher = publish_on(sys.argv[3])

    links_replacement = glob_links(work_dir, nb_pattern, publisher)
    if isinstance(publisher, PublishOnDrive):
        # The Google Drive publisher returns colab links equal to None for any file added by the current commit.
        # Force an upload to obtain a valid link
        local_files_with_none_link = [
            os.path.relpath(local_link, work_dir)
            for (local_link, colab_link) in links_replacement.items() if colab_link is None
        ]
        if len(local_files_with_none_link) > 0:
            local_files_with_none_link = "\n".join(local_files_with_none_link)
            upload_files_to_google_drive(work_dir, local_files_with_none_link, publisher.drive_root_directory)
            links_replacement.update(glob_links(work_dir, local_files_with_none_link, publisher))
        for (local_link, colab_link) in links_replacement.items():
            assert colab_link is not None
            print(os.path.relpath(local_link, work_dir) + " -> " + colab_link)

    for nb_filename in glob_files(work_dir, nb_pattern):
        with open(nb_filename, "r") as f:
            nb = nbformat.read(f, as_version=4)
        nb.cells = replace_links_in_markdown(nb.cells, os.path.dirname(nb_filename), links_replacement)
        with open(nb_filename, "w") as f:
            nbformat.write(nb, f)
