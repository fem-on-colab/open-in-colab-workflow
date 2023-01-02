# Copyright (C) 2021-2023 by the FEM on Colab authors
#
# This file is part of FEM on Colab-related actions.
#
# SPDX-License-Identifier: MIT
"""Get links associated to every notebook in the work directory."""

import os
import typing

from open_in_cloud_workflow.glob_files import glob_files
from open_in_cloud_workflow.publish_on import PublishOnArtifact, PublishOnBaseClass, PublishOnDrive, PublishOnGitHub


def glob_links(
    work_dir: str, pattern: str, cloud_provider: str, publish_on: PublishOnBaseClass
) -> typing.Dict[str, typing.Optional[str]]:
    """Get links associated to every notebook matching a pattern in the work directory."""
    if isinstance(publish_on, PublishOnArtifact):
        # No link replacement is necessary
        return {}
    elif isinstance(publish_on, (PublishOnDrive, PublishOnGitHub)):
        links_replacement = dict()
        for local_file in glob_files(work_dir, pattern):
            links_replacement[local_file] = publish_on.get_url(cloud_provider, os.path.relpath(local_file, work_dir))
        return links_replacement
    else:  # pragma: no cover
        raise RuntimeError("Invalid publish_on attribute")
