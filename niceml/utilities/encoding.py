"""Module for encoding files, data or arrays"""  # QUEST: still used?
import base64
from io import BytesIO
from typing import Optional, Union

import numpy as np
from fsspec import AbstractFileSystem
from fsspec.implementations.local import LocalFileSystem
from PIL import Image


def get_base64_from_file(
    filepath: str, filesystem: Optional[AbstractFileSystem] = None
) -> bytes:
    """Returns a file encoded as base64"""
    if filesystem is None:
        filesystem = LocalFileSystem()

    with filesystem.open(filepath, "rb") as target_file:
        encoded_string = base64.b64encode(target_file.read())

    return encoded_string


def base64_to_bytesio(encoded_data: Union[bytes, str]) -> BytesIO:
    """Returns a BytesIO stream of the decoded data"""
    # can be used with PIL.Image.open to get an image
    return BytesIO(base64.b64decode(encoded_data))


def numpy_to_base64(
    array: np.ndarray, format: str = "png"
) -> str:  # pylint: disable=redefined-builtin
    """Stores a numpy array as base 64. Only works with correct format restrictions."""
    pil_img = Image.fromarray(array)
    buff = BytesIO()
    pil_img.save(buff, format=format)
    return base64.b64encode(buff.getvalue()).decode("utf-8")
