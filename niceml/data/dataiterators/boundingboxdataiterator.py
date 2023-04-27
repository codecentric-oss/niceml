"""Module containing BoundingBoxIterator"""
from dataclasses import dataclass
from typing import List

import cattr
import numpy as np
from niceml.mlcomponents.resultanalyzers.tensors.tensordataiterators import (
    TensordataIterator,
)
from fsspec.implementations.local import LocalFileSystem

from niceml.utilities.boundingboxes.boundingbox import BoundingBox
from niceml.utilities.ioutils import read_parquet

NO_PREDICTIONS_DETECTION_VALUE = -1
DETECTION_INDEX_COLUMN_NAME = "detection_index"


@dataclass
class ObjDetPredictionContainer:
    """Container class for iterating over prediction data"""

    bounding_box: BoundingBox
    class_predictions: np.ndarray

    def to_array(self) -> np.ndarray:
        bbox_array = np.array(self.bounding_box.get_absolute_xywh())
        combined_array = np.concatenate([bbox_array, self.class_predictions])
        return combined_array


class BoundingBoxIterator(TensordataIterator):
    """Iterator for iterating over prediction data"""

    def __init__(self, parq_extension: str = ".parq"):
        self.parq_extension = parq_extension
        self.target_cols_prefix = "pred"
        self.data = None
        self.keys = None

    def open(self, path: str, file_system=None):
        file_system = file_system or LocalFileSystem()
        self.data = read_parquet(path + self.parq_extension, file_system=file_system)
        self.keys = list(self.data.iloc[:, 0].unique())

    def __iter__(self):
        if self.keys is None:
            raise Exception("Keys is None. open method needs to be called fist.")
        return iter(self.keys)

    def __getitem__(self, data_key: str) -> List[ObjDetPredictionContainer]:
        if self.data is None:
            raise Exception("Data is None. open method needs to be called fist.")
        prediction_container_list = []
        filtered_data = self.data[self.data.iloc[:, 0] == data_key]

        if (
            filtered_data[DETECTION_INDEX_COLUMN_NAME].iloc[0]
            == NO_PREDICTIONS_DETECTION_VALUE
        ):
            return []

        bounding_box_list = [
            cattr.structure(row, BoundingBox) for _, row in filtered_data.iterrows()
        ]
        class_prediction_cols = [
            x for x in self.data.columns if x.startswith(self.target_cols_prefix)
        ]
        class_predictions_array = filtered_data[class_prediction_cols].to_numpy()

        for bounding_box, class_predictions in zip(
            bounding_box_list, class_predictions_array
        ):
            prediction_container = ObjDetPredictionContainer(
                bounding_box=bounding_box,
                class_predictions=class_predictions,
            )
            prediction_container_list.append(prediction_container)
        return prediction_container_list
