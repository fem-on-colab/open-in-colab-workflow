# Copyright (C) 2021-2025 by the FEM on Colab authors
#
# This file is part of FEM on Colab-related actions.
#
# SPDX-License-Identifier: MIT
"""Convert a string representing a list of packages."""



def packages_str_to_lists(packages_str: str) -> tuple[
        list[str], list[str], list[str], list[str], list[str],
        list[str], list[str]]:
    """
    Convert a newline separated string formatted with @, $, %, £ and € special characters.

    Full format is (without line breaks):
        package_name_and_version
        @package_url$package_import%package_dependent_imports
        £install_command_line_options€extra_commands_before_install.
    """
    packages_name = list()
    packages_version = list()
    packages_url = list()
    packages_import = list()
    packages_dependent_imports = list()
    packages_install_command_line_options = list()
    packages_extra_commands_before_install = list()
    if packages_str != "":
        for package_str in packages_str.strip("\n").split("\n"):
            split_at_euro = package_str.split("€")
            assert len(split_at_euro) in (1, 2)
            if len(split_at_euro) == 1:
                package_name_version_url_import_depimports_commandlineoptions = split_at_euro[0]
                package_extra_commands_before_install = ""
            elif len(split_at_euro) == 2:
                package_name_version_url_import_depimports_commandlineoptions = split_at_euro[0]
                package_extra_commands_before_install = split_at_euro[1]
            split_at_pound = package_name_version_url_import_depimports_commandlineoptions.split("£")
            assert len(split_at_pound) in (1, 2)
            if len(split_at_pound) == 1:
                package_name_version_url_import_depimports = split_at_pound[0]
                package_install_command_line_options = ""
            elif len(split_at_pound) == 2:
                package_name_version_url_import_depimports = split_at_pound[0]
                package_install_command_line_options = split_at_pound[1]
            split_at_percent = package_name_version_url_import_depimports.split("%")
            assert len(split_at_percent) in (1, 2)
            if len(split_at_percent) == 1:
                package_name_version_url_import = split_at_percent[0]
                package_dependent_imports = ""
            elif len(split_at_percent) == 2:
                package_name_version_url_import = split_at_percent[0]
                package_dependent_imports = split_at_percent[1]
            split_at_dollar = package_name_version_url_import.split("$")
            assert len(split_at_dollar) in (1, 2)
            if len(split_at_dollar) == 1:
                package_name_version_url = split_at_dollar[0]
                package_import = None
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
            for operator in ("==", ">=", ">", "<=", "<", "["):
                if operator in package_name:
                    split_at_operator = package_str.split(operator)
                    assert len(split_at_operator) in (1, 2)
                    package_name = split_at_operator[0]
            package_version = package_name_version[len(package_name):]
            packages_name.append(package_name)
            packages_version.append(package_version)
            packages_url.append(package_url)
            if package_import is None:
                packages_import.append(package_name)
            else:
                packages_import.append(package_import)
            packages_dependent_imports.append(package_dependent_imports)
            packages_install_command_line_options.append(package_install_command_line_options)
            packages_extra_commands_before_install.append(package_extra_commands_before_install)
    return (
        packages_name, packages_version, packages_url, packages_import, packages_dependent_imports,
        packages_install_command_line_options, packages_extra_commands_before_install
    )
