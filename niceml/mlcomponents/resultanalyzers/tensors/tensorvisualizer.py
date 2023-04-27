"""Module for tensorvisualizer"""
from dataclasses import dataclass
from os.path import join
from typing import List

import numpy as np
from PIL import Image

from niceml.mlcomponents.resultanalyzers.tensors.tensormetric import TensorMetric


@dataclass
class ColorInfo:
    """ColorInfo used for visualization"""

    color: List[int]
    index: int
    threshold: float = 0.5


class TensorVisualizer(TensorMetric):
    """TensorMetric used for visualization e.g. SemSeg"""

    def __init__(self, key: str, colormap: List[dict]):
        super().__init__(key)
        color_list: List[ColorInfo] = [ColorInfo(**x) for x in colormap]
        c_info: ColorInfo
        self.colormap = {c_info.index: c_info.color for c_info in color_list}
        self.thresholds = {c_info.index: c_info.threshold for c_info in color_list}
        self.img_count = 0
        self.store_folder: str = ""

    def start_analysis(self):
        self.store_folder = join(self.output_folder, self.dataset_name)

    def analyse_datapoint(
        self,
        data_key: str,
        data_predicted,
        data_loaded,
        additional_data: dict,
        **kwargs,
    ):
        color_img = np.zeros(data_predicted.shape[0:2] + (3,), dtype=np.uint8)
        for cur_idx, threshold in self.thresholds.items():
            color_img[data_predicted[:, :, cur_idx] >= threshold, :] = self.colormap[
                cur_idx
            ]
        color_img = Image.fromarray(color_img)
        self.exp_context.write_image(
            color_img, join(self.store_folder, data_key + ".jpg")
        )
        self.img_count += 1

    def get_final_metric(self) -> dict:
        return dict(saved_images=self.img_count)
