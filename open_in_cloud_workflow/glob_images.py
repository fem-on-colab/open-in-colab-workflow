# Copyright (C) 2021-2022 by the FEM on Colab authors
#
# This file is part of FEM on Colab-related actions.
#
# SPDX-License-Identifier: MIT
"""Look for images in the work directory, and compute their base64 representation."""

import base64
import io
import os
import subprocess
import typing

from open_in_cloud_workflow.glob_files import glob_files


def glob_images(work_dir: str) -> typing.Dict[str, str]:
    """Look for images in the work directory, and compute their base64 representation."""
    images_as_base64 = dict()
    image_convert: typing.List[str]
    for (image_ext, image_convert) in (  # type: ignore[assignment]
        ("png", []),
        ("jpg", ["convert {image_file} {image_file_png}"]),
        ("svg",
         ["inkscape -e {image_file_png} {image_file}", "inkscape --export-filename={image_file_png} {image_file}"])
    ):
        for image_file in glob_files(work_dir, os.path.join("**", f"*.{image_ext}")):
            image_prefix, _ = os.path.splitext(image_file)
            image_file_png = image_prefix + ".png"
            if not os.path.isfile(image_file_png):
                for image_convert_ in image_convert:
                    try:
                        subprocess.check_call(
                            image_convert_.format(image_file=image_file, image_file_png=image_file_png).split(" "),
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                    except subprocess.CalledProcessError:  # pragma: no cover
                        pass
                    else:
                        break
                else:  # pragma: no cover
                    raise RuntimeError(f"Image conversion failed for {image_file}")
            assert image_file not in images_as_base64
            images_as_base64[image_file] = _to_base64(image_file_png)
    return images_as_base64


def _to_base64(image_file: str) -> str:
    """Convert the PNG image to its base64 representation."""
    assert image_file.endswith(".png")
    with io.open(image_file, "rb") as f:
        image_content = base64.b64encode(f.read()).decode("utf-8")
    return "data:image/png;base64," + image_content
