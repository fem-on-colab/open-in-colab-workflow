# Copyright (C) 2021-2026 by the FEM on Colab authors
#
# This file is part of FEM on Colab-related actions.
#
# SPDX-License-Identifier: MIT
"""Replace local markdown links with links to cloud notebooks."""

import copy
import os
import sys

import nbformat

from open_in_cloud_workflow.glob_files import glob_files
from open_in_cloud_workflow.glob_links import glob_links
from open_in_cloud_workflow.publish_on import (
    publish_on,
    PublishOnBaseClass,
    PublishOnDrive,
)
from open_in_cloud_workflow.upload_files_to_google_drive import (
    upload_files_to_google_drive,
)


def replace_links_in_markdown(
    nb_cells: list[nbformat.NotebookNode],
    links_replacement: dict[str, str | None],
) -> list[nbformat.NotebookNode]:
    """Replace local markdown links with links to cloud notebooks."""
    add_quotes_or_parentheses = (
        lambda text: '"' + text + '"',
        lambda text: "'" + text + "'",
        lambda text: "(" + text + ")",
    )
    updated_nb_cells = list()
    for cell in nb_cells:
        if cell.cell_type == "markdown":
            updated_cell = copy.deepcopy(cell)
            for local_link, cloud_link in links_replacement.items():
                assert cloud_link is not None
                for preprocess in add_quotes_or_parentheses:
                    updated_cell.source = updated_cell.source.replace(
                        preprocess(local_link),
                        preprocess(cloud_link),
                    )
            updated_nb_cells.append(updated_cell)
        else:
            updated_nb_cells.append(cell)
    return updated_nb_cells


def __main__(  # noqa: N807
    work_dir: str,
    nb_pattern: str,
    cloud_provider: str,
    publisher: str | PublishOnBaseClass,
) -> None:
    """Replace links in notebooks that match the provided pattern."""
    if not isinstance(publisher, PublishOnBaseClass):  # pragma: no cover
        assert isinstance(publisher, str)
        publisher = publish_on(publisher)

    links_replacement = glob_links(
        work_dir, nb_pattern, cloud_provider, publisher
    )
    if isinstance(publisher, PublishOnDrive):
        # Google Drive links are None for files added by the current commit.
        # Force an upload to obtain a valid link
        local_files_with_none_link = [
            os.path.relpath(local_link, work_dir)
            for (local_link, cloud_link) in links_replacement.items()
            if cloud_link is None
        ]
        if len(local_files_with_none_link) > 0:  # pragma: no cover
            for local_link in local_files_with_none_link:
                print(
                    os.path.relpath(local_link, work_dir)
                    + " will be created anew"
                )
            local_files_with_none_link_str = "\n".join(
                local_files_with_none_link
            )
            upload_files_to_google_drive(
                work_dir,
                local_files_with_none_link_str,
                publisher.drive_root_directory,
            )
            links_replacement.update(
                glob_links(
                    work_dir,
                    local_files_with_none_link_str,
                    cloud_provider,
                    publisher,
                )
            )
    for local_link, cloud_link in links_replacement.items():
        assert cloud_link is not None
        print(os.path.relpath(local_link, work_dir) + " -> " + cloud_link)

    for nb_filename in glob_files(work_dir, nb_pattern):
        with open(nb_filename) as f:
            nb = nbformat.read(f, as_version=4)
        nb_dirname = os.path.dirname(nb_filename)
        nb_links_replacement = {
            os.path.relpath(os.path.join(work_dir, key), nb_dirname): value
            for key, value in links_replacement.items()
        }
        nb.cells = replace_links_in_markdown(nb.cells, nb_links_replacement)
        with open(nb_filename, "w") as f:
            nbformat.write(nb, f)


if __name__ == "__main__":  # pragma: no cover
    assert len(sys.argv) == 5
    __main__(*sys.argv[1:])
