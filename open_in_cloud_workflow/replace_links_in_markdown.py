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

from open_in_cloud_workflow.glob_files import glob_files
from open_in_cloud_workflow.glob_links import glob_links
from open_in_cloud_workflow.publish_on import publish_on, PublishOnBaseClass, PublishOnDrive
from open_in_cloud_workflow.upload_files_to_google_drive import upload_files_to_google_drive


def replace_links_in_markdown(
    nb_cells: typing.List[nbformat.NotebookNode], nb_dir: str,
    links_replacement: typing.Dict[str, typing.Optional[str]]
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
                assert colab_link is not None
                for preprocess in add_quotes_or_parentheses:
                    updated_cell.source = updated_cell.source.replace(
                        preprocess(os.path.relpath(local_link, nb_dir)),  # type: ignore[no-untyped-call]
                        preprocess(colab_link))  # type: ignore[no-untyped-call]
            updated_nb_cells.append(updated_cell)
        else:
            updated_nb_cells.append(cell)
    return updated_nb_cells


def __main__(work_dir: str, nb_pattern: str, publisher: typing.Union[str, PublishOnBaseClass]) -> None:
    """Replace links in every notebook in the work directory matching the prescribed pattern."""
    if not isinstance(publisher, PublishOnBaseClass):  # pragma: no cover
        assert isinstance(publisher, str)
        publisher = publish_on(publisher)

    links_replacement = glob_links(work_dir, nb_pattern, publisher)
    if isinstance(publisher, PublishOnDrive):
        # The Google Drive publisher returns colab links equal to None for any file added by the current commit.
        # Force an upload to obtain a valid link
        local_files_with_none_link = [
            os.path.relpath(local_link, work_dir)
            for (local_link, colab_link) in links_replacement.items() if colab_link is None
        ]
        if len(local_files_with_none_link) > 0:  # pragma: no cover
            for local_link in local_files_with_none_link:
                print(os.path.relpath(local_link, work_dir) + " will be created anew")
            local_files_with_none_link_str = "\n".join(local_files_with_none_link)
            upload_files_to_google_drive(work_dir, local_files_with_none_link_str, publisher.drive_root_directory)
            links_replacement.update(glob_links(work_dir, local_files_with_none_link_str, publisher))
    for (local_link, colab_link) in links_replacement.items():
        assert colab_link is not None
        print(os.path.relpath(local_link, work_dir) + " -> " + colab_link)

    for nb_filename in glob_files(work_dir, nb_pattern):
        with open(nb_filename, "r") as f:
            nb = nbformat.read(f, as_version=4)  # type: ignore[no-untyped-call]
        nb.cells = replace_links_in_markdown(nb.cells, os.path.dirname(nb_filename), links_replacement)
        with open(nb_filename, "w") as f:
            nbformat.write(nb, f)  # type: ignore[no-untyped-call]


if __name__ == "__main__":  # pragma: no cover
    assert len(sys.argv) == 4
    __main__(*sys.argv[1:])
