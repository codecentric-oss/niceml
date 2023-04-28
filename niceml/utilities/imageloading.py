"""Module for image loading"""
from os.path import basename, join
from tempfile import TemporaryDirectory
from typing import Optional

import cv2
import numpy as np
from fsspec import AbstractFileSystem
from fsspec.implementations.local import LocalFileSystem
from PIL import Image

from niceml.utilities.imagesize import ImageSize


def load_img_uint8(
    image_path: str,
    file_system: Optional[AbstractFileSystem] = None,
    target_image_size: Optional[ImageSize] = None,
    interpolation: int = cv2.INTER_LINEAR,
) -> np.ndarray:
    """
    Loads an image from arbitrary source ('file_system') and returns an uint8 np.ndarray

    Args:
        image_path: Path of image file to load
        file_system: Allow the function to be used with different file systems; default = local
        target_image_size: Target size of loaded image
        interpolation: Interpolation of resizing

    Returns:
        Loaded image object with target size in uint8 format
    """
    file_system: AbstractFileSystem = file_system or LocalFileSystem()
    try:
        with file_system.open(image_path) as fs_file:
            image = Image.open(fs_file).copy()
        np_array = np.array(image)
        if np_array.dtype == bool:
            np_array = np_array.astype(np.uint8)
            np_array *= 255
    except OSError:
        with TemporaryDirectory() as tmp_dir:
            tmp_file = join(tmp_dir, basename(image_path))
            file_system.get_file(image_path, tmp_file)
            np_array = cv2.imread(tmp_file)  # pylint: disable=no-member
    if target_image_size is not None and not target_image_size.np_array_has_same_size(
        np_array
    ):
        np_array = cv2.resize(
            np_array, target_image_size.to_numpy_shape(), interpolation=interpolation
        )
    return np_array


class ImgShapeError(Exception):
    """Error when the image has the wrong shape"""


def convert_to_3channel_img(input_img: np.ndarray) -> np.ndarray:  # QUEST: still used?
    """
    Converts an image (as np.ndarray) to a one with 3 channels

    Args:
        input_img: image object as np.ndarray

    Returns:
        image as np.ndarray with 3 channels
    """
    if len(input_img.shape) not in [2, 3]:
        raise ImgShapeError(
            f"Image cannot be broadcast to a " f"3 channel image: {input_img.shape}"
        )

    if len(input_img.shape) == 2:
        return np.concatenate([input_img[:, :, np.newaxis]] * 3, axis=2)

    if input_img.shape[2] == 3:
        return input_img

    if input_img.shape[2] == 1:
        return np.concatenate([input_img] * 3, axis=2)

    raise ImgShapeError(
        f"Image cannot be broadcast to a " f"3 channel image: {input_img.shape}"
    )
