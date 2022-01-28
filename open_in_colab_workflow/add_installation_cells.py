# Copyright (C) 2021-2022 by the FEM on Colab authors
#
# This file is part of FEM on Colab-related actions.
#
# SPDX-License-Identifier: MIT
"""Add installation cells on top of the notebook."""

import copy
import sys
import typing

import nbformat

from open_in_colab_workflow.get_fem_on_colab_installation_cell_code import get_fem_on_colab_installation_cell_code
from open_in_colab_workflow.get_pip_installation_cell_code import get_pip_installation_cell_code
from open_in_colab_workflow.glob_files import glob_files
from open_in_colab_workflow.packages_str_to_lists import packages_str_to_lists


def add_installation_cells(
    nb_cells: typing.List[nbformat.NotebookNode], fem_on_colab_packages_str: str, pip_packages_str: str
) -> typing.Tuple[typing.List[nbformat.NotebookNode], typing.List[int]]:
    """Add installation cells on top of the notebook, and return updated notebook content and list of insertions."""
    (fem_on_colab_packages_name, fem_on_colab_packages_version, fem_on_colab_packages_url,
        fem_on_colab_packages_import) = packages_str_to_lists(fem_on_colab_packages_str)
    (pip_packages_name, pip_packages_version, pip_packages_url,
        pip_packages_import) = packages_str_to_lists(pip_packages_str)

    packages_name = fem_on_colab_packages_name + pip_packages_name
    packages_install_code = [
        get_fem_on_colab_installation_cell_code(package_name, package_version, package_url, package_import)
        for (package_name, package_version, package_url, package_import) in zip(
            fem_on_colab_packages_name, fem_on_colab_packages_version, fem_on_colab_packages_url,
            fem_on_colab_packages_import)
    ] + [
        get_pip_installation_cell_code(package_name, package_version, package_url, package_import)
        for (package_name, package_version, package_url, package_import) in zip(
            pip_packages_name, pip_packages_version, pip_packages_url, pip_packages_import)
    ]
    packages_import = fem_on_colab_packages_import + pip_packages_import

    actually_imported_packages = {package_import: False for package_import in packages_import}
    for package_import in packages_import:
        for cell in nb_cells:
            if cell.cell_type == "code":
                if f"import {package_import}" in cell.source or f"from {package_import}" in cell.source:
                    actually_imported_packages[package_import] = True
                    break

    first_code_cell_position = 0
    for cell in nb_cells:
        if cell.cell_type == "code":
            break
        else:
            first_code_cell_position += 1

    updated_nb_cells = copy.deepcopy(nb_cells)
    new_cells_position = list()
    for (package_name, package_install_code, package_import) in zip(
            packages_name, packages_install_code, packages_import):
        if actually_imported_packages[package_import]:
            package_install_cell = nbformat.v4.new_code_cell(package_install_code)
            package_install_cell.id = package_name.replace(" ", "_") + "_install"
            updated_nb_cells.insert(first_code_cell_position, package_install_cell)
            new_cells_position.append(first_code_cell_position)
            first_code_cell_position += 1
    return updated_nb_cells, new_cells_position


if __name__ == "__main__":  # pragma: no cover
    assert len(sys.argv) == 5
    work_dir = sys.argv[1]
    nb_pattern = sys.argv[2]
    fem_on_colab_packages = sys.argv[3]
    pip_packages = sys.argv[4]

    for nb_filename in glob_files(work_dir, nb_pattern):
        with open(nb_filename, "r") as f:
            nb = nbformat.read(f, as_version=4)
        nb.cells, _ = add_installation_cells(nb.cells, fem_on_colab_packages, pip_packages)
        with open(nb_filename, "w") as f:
            nbformat.write(nb, f)
