"""Module for TargetTransformerClassification"""
from typing import List

import numpy as np
from sklearn.preprocessing import MultiLabelBinarizer

from niceml.data.datadescriptions.datadescription import DataDescription
from niceml.data.datadescriptions.outputdatadescriptions import (
    OutputVectorDataDescription,
)
from niceml.data.datainfos.clsdatainfo import ClsData
from niceml.mlcomponents.targettransformer.targettransformer import NetTargetTransformer
from niceml.utilities.commonutils import check_instance


class TargetTransformerClassification(NetTargetTransformer):
    """NetTargetTransformer for Classification"""

    def __init__(self):
        super().__init__()
        self.use_binary: bool = False
        self.multi_label_binarizer = None

    def initialize(self, data_description: DataDescription):
        super().initialize(data_description)
        vector_output_data_description = check_instance(
            data_description, OutputVectorDataDescription
        )
        self.use_binary = (  # pylint: disable=attribute-defined-outside-init
            vector_output_data_description.get_output_size() == 1
        )
        self.multi_label_binarizer: MultiLabelBinarizer = (
            MultiLabelBinarizer(  # pylint: disable=attribute-defined-outside-init
                classes=list(range(vector_output_data_description.get_output_size()))
            )
        )

    def get_net_targets(self, data_list: List[ClsData]) -> np.ndarray:
        cur_cls_data: ClsData
        index_list = [cur_cls_data.get_index_list() for cur_cls_data in data_list]

        if self.use_binary:
            target_array = np.array(index_list, dtype=np.double)
        else:
            target_array = self.multi_label_binarizer.fit_transform(index_list).astype(
                np.double
            )
        return target_array
