"""Module for semseg prediction container and data handler"""
from dataclasses import dataclass
from os.path import basename, splitext
from typing import List, Optional

import numpy as np
from fsspec import AbstractFileSystem
from fsspec.implementations.local import LocalFileSystem

from niceml.mlcomponents.resultanalyzers.tensors.tensordataiterators import (
    TensordataIterator,
)
from niceml.utilities.ioutils import list_dir, read_image


@dataclass
class SemSegPredictionContainer:
    """Contains information about maximum prediction of an image"""

    max_prediction_idxes: np.ndarray
    max_prediction_values: np.ndarray
    image_id: Optional[str] = None


class SemSegDataIterator(TensordataIterator):
    """Data Iterator for SemSeg"""

    def __init__(
        self,
        supported_extensions: Optional[List[str]] = None,
        prediction_suffix: str = "_pred",
    ):
        if supported_extensions is None:
            self.supported_extensions = [".png", ".jpg", ".jpeg", ".tiff", ".bmp"]
        self.data: Optional[dict] = None
        self.prediction_suffix = prediction_suffix
        self.file_system: Optional[AbstractFileSystem] = None

    def open(self, path: str, file_system: Optional[AbstractFileSystem] = None):
        self.file_system = file_system or LocalFileSystem()
        files = [
            x
            for x in list_dir(
                path, recursive=True, return_full_path=True, file_system=file_system
            )
            if splitext(x)[1] in self.supported_extensions
            and self.prediction_suffix in x
        ]
        self.data = {}
        for cur_file in files:
            lens_id = basename(cur_file.split(self.prediction_suffix)[0])
            self.data[lens_id] = cur_file

    def __iter__(self):
        return iter(self.data)

    def __getitem__(self, image_id: str) -> SemSegPredictionContainer:
        if self.data is None or self.file_system is None:
            raise Exception("Data or file_system shouldn't be None")
        cur_file: str = self.data[image_id]
        image = read_image(cur_file, file_system=self.file_system)
        array = np.array(image)
        max_values = array[:, :, 0] / 255
        max_indices = array[:, :, 1]
        return SemSegPredictionContainer(
            image_id=image_id,
            max_prediction_idxes=max_indices,
            max_prediction_values=max_values,
        )
