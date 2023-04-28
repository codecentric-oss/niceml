"""Module for SemSegTargetTransformer"""
from typing import List

import numpy as np

from niceml.data.datadescriptions.inputdatadescriptions import InputImageDataDescription
from niceml.data.datadescriptions.outputdatadescriptions import OutputImageDataDescription
from niceml.data.datainfos.semsegdatainfo import SemSegData
from niceml.mlcomponents.targettransformer.targettransformer import NetTargetTransformer
from niceml.utilities.commonutils import check_instance
from niceml.utilities.imagesize import ImageSize
from niceml.utilities.masks.maskdownscale import get_downscaled_masked_histogram


class SemSegTargetTransformer(NetTargetTransformer):
    """transforms classification net targets for Lens Defect SemSeg"""

    def __init__(self, default_value: int = 255):
        self.default_value = default_value

    def get_net_targets(self, data_list: List[SemSegData]) -> np.ndarray:
        output_array = np.array(
            [
                self.get_single_target(semseg_data=semseg_data)
                for semseg_data in data_list
            ]
        )
        return output_array

    def get_single_target(self, semseg_data: SemSegData) -> np.ndarray:
        """returns mask array of one lens"""
        out_dd: OutputImageDataDescription = check_instance(
            self.data_description, OutputImageDataDescription
        )
        input_dd: InputImageDataDescription = check_instance(
            self.data_description, InputImageDataDescription
        )
        input_image_size: ImageSize = input_dd.get_input_image_size()
        output_image_size: ImageSize = out_dd.get_output_image_size()
        class_count: int = out_dd.get_output_channel_count()
        mask_image = semseg_data.mask_image
        output_array = np.zeros(out_dd.get_output_tensor_shape())
        if out_dd.get_output_image_size().np_array_has_same_size(mask_image):
            output_array[
                mask_image != self.default_value,
                mask_image[mask_image < class_count],
            ] = 1
        else:
            ds_masked_hist = get_downscaled_masked_histogram(
                mask_image=mask_image,
                num_classes=class_count,
                default_value=self.default_value,
                ds_factor=int(input_image_size.get_division_factor(output_image_size)),
            )
            output_array[ds_masked_hist > 0] = 1
        return output_array
