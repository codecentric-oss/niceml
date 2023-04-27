"""Module for ImageInputTransformer"""
from typing import Any, List

import numpy as np

from niceml.mlcomponents.targettransformer.targettransformer import NetInputTransformer


class ImageInputTransformer(NetInputTransformer):
    """Input transformer for object detection"""

    def __init__(self, image_attr_name: str = "image"):
        self.image_attr_name = image_attr_name

    def get_net_inputs(self, data_list: List[Any]) -> np.ndarray:
        return np.array(
            [
                np.array(getattr(curr_obj_data, self.image_attr_name))
                for curr_obj_data in data_list
            ]
        )
