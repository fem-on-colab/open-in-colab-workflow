# Copyright (C) 2021-2022 by the FEM on Colab authors
#
# This file is part of FEM on Colab-related actions.
#
# SPDX-License-Identifier: MIT
"""Convert a string representing a list of packages."""

import typing


def packages_str_to_lists(packages_str: str) -> typing.Tuple[
        typing.List[str], typing.List[str], typing.List[str], typing.List[str]]:
    """Convert a newline separated string formatted as package_name_and_version@package_url$package_import."""
    packages_name = list()
    packages_version = list()
    packages_url = list()
    packages_import = list()
    if packages_str != "":
        for package_str in packages_str.split("\n"):
            split_at_dollar = package_str.split("$")
            assert len(split_at_dollar) in (1, 2)
            if len(split_at_dollar) == 1:
                package_name_version_url = split_at_dollar[0]
                package_import = ""
            elif len(split_at_dollar) == 2:
                package_name_version_url = split_at_dollar[0]
                package_import = split_at_dollar[1]
            split_at_at = package_name_version_url.split("@")
            assert len(split_at_at) in (1, 2, 3)
            if len(split_at_at) == 1:
                package_name_version = split_at_at[0]
                package_url = ""
            elif len(split_at_at) == 2:
                package_name_version = split_at_at[0]
                package_url = split_at_at[1]
            elif len(split_at_at) == 3:
                package_name_version = split_at_at[0]
                package_url = "@".join(split_at_at[1:])
            package_name = package_name_version
            for operator in ("==", ">=", ">", "<=", "<"):
                if operator in package_name:
                    split_at_operator = package_str.split(operator)
                    assert len(split_at_operator) in (1, 2)
                    package_name = split_at_operator[0]
            package_version = package_name_version[len(package_name):]
            packages_name.append(package_name)
            packages_version.append(package_version)
            packages_url.append(package_url)
            if package_import == "":
                packages_import.append(package_name)
            else:
                packages_import.append(package_import)
    return packages_name, packages_version, packages_url, packages_import
