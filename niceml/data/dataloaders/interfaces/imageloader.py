"""Module for abstract ImageLoader"""
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Optional

import numpy as np

from niceml.utilities.imagesize import ImageSize


class ImageLoader(ABC):
    """Abstract implementation of ImageLoader"""

    @abstractmethod
    def __call__(
        self, filepath: str, target_size: Optional[ImageSize] = None
    ) -> np.ndarray:
        pass

    @staticmethod
    def is_image(path: str) -> bool:
        """checks if file from filepath is an image"""
        img_path = Path(path)
        return img_path.is_file() and img_path.name.split(".")[-1] in [
            "jpg",
            "png",
            "tiff",
            "tif",
            "bmp",
            "jpeg",
        ]
