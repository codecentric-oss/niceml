"""Module for PredictionFilter"""
from abc import ABC, abstractmethod
from typing import List, Optional, Type, Union

import numpy as np
from attrs import asdict, define, fields

from niceml.data.datadescriptions.outputdatadescriptions import (
    OutputImageDataDescription,
    OutputObjDetDataDescription,
)


@define
class PredictionFilter(ABC):  # pylint: disable=too-few-public-methods
    """Class to filter predictions"""

    output_class_count: Optional[int] = None

    def initialize(
        self,
        data_description: Union[
            OutputObjDetDataDescription, OutputImageDataDescription
        ],
    ):
        """
        Initialization method for the prediction filter
        Args:
            data_description: `DataDescription` that can be used for initialization
        """
        if isinstance(data_description, OutputObjDetDataDescription):
            self.output_class_count = data_description.get_output_class_count()
        elif isinstance(data_description, OutputImageDataDescription):
            self.output_class_count = data_description.get_output_channel_count()
        else:
            raise TypeError(
                f"Object of class {type(data_description)} "
                f"is not instance of class: {OutputObjDetDataDescription} "
                f"or {OutputImageDataDescription}"
            )

    def to_dict(self) -> dict:
        """Creates a representation of itself as a dict"""
        filter_dict = asdict(self)
        filter_dict["pred_type"] = type(self).__name__
        return filter_dict

    @abstractmethod
    def filter(self, prediction_array_xywh: np.ndarray) -> np.ndarray:
        """
        Filters prediction arrays with corresponding class predictions
        Args:
            prediction_array_xywh: input predictions (n x (4 + num_classes))

        Returns:
            prediction_array_xywh: Filtered predictions (m x (4 + num_classes))
        """


def get_filter_attributes(  # QUEST: still used?
    filter_class: Type[PredictionFilter], ignore_attributes: Optional[List[str]] = None
):
    """
    Iterates the attributes of `filter_class` and returns it.
    Returns:
        list of the attributes of `filter_class` as a dict with `name` and `default` as keys
    """
    # pylint: disable=not-an-iterable
    ignore_attributes = ignore_attributes or []
    filter_attributes = []

    for field in fields(filter_class):
        if field.name not in ignore_attributes:
            filter_attribute = {"name": field.name, "default": 0.0, "step": None}

            if field.name in ["score_threshold", "iou_threshold"]:
                filter_attribute["default"] = 0.5

            if field.type == Union[int, None]:
                filter_attribute["step"] = 1
                filter_attribute["default"] = (
                    200 if field.name == "max_output_count" else 0
                )
            filter_attributes.append(filter_attribute)
    return filter_attributes
