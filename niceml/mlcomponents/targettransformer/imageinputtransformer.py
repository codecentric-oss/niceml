"""Module for ImageInputTransformer"""
from typing import Any, List, Optional

import numpy as np

from niceml.data.datadescriptions.datadescription import DataDescription
from niceml.mlcomponents.targettransformer.targettransformer import NetInputTransformer


class ImageInputTransformer(NetInputTransformer):
    """Input transformer for object detection"""

    def __init__(
        self,
        image_attr_name: str = "image",
        data_description: Optional[DataDescription] = None,
    ):
        super().__init__(data_description=data_description)
        self.image_attr_name = image_attr_name

    def get_net_inputs(self, data_list: List[Any]) -> np.ndarray:
        return np.array(
            [
                np.array(getattr(curr_obj_data, self.image_attr_name))
                for curr_obj_data in data_list
            ]
        )
