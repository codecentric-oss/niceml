"""Module for the input and target transformers used for object detection"""

from typing import List

import numpy as np

from niceml.data.datadescriptions.outputdatadescriptions import (
    OutputObjDetDataDescription,
)
from niceml.data.datainfos.objdetdatainfo import ObjDetData
from niceml.mlcomponents.objdet.anchorencoding import AnchorEncoder
from niceml.mlcomponents.objdet.anchorgenerator import AnchorGenerator
from niceml.mlcomponents.targettransformer.targettransformer import (
    NetInputTransformer,
    NetTargetTransformer,
)


class ObjDetTargetTransformer(NetTargetTransformer):
    """Target transformer for object detection"""

    def __init__(
        self, anchor_generator: AnchorGenerator, anchor_encoder: AnchorEncoder
    ):
        self.anchor_encoder = anchor_encoder
        self.anchor_generator = anchor_generator
        self.anchors = None

    def get_net_targets(self, data_list: List[ObjDetData]) -> np.ndarray:

        if self.anchors is None:
            if isinstance(self.data_description, OutputObjDetDataDescription):
                self.anchors = self.anchor_generator.generate_anchors(
                    self.data_description
                )
            else:
                raise TypeError(
                    "data_description must be an instance of OutputObjDetDataDescription"
                )

        target_list = [
            self.anchor_encoder.encode_anchors(
                anchor_list=self.anchors,
                gt_labels=curr_obj_data.labels,
                num_classes=self.data_description.get_output_class_count(),
                box_variance=self.data_description.get_box_variance(),
            )
            for curr_obj_data in data_list
        ]
        return np.array(target_list)
