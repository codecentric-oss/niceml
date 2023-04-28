"""Module for TensorIou TensorMetric"""
from os import makedirs
from os.path import isdir, join

import numpy as np
import pyximport

from niceml.data.datadescriptions.semsegdatadescritption import SemSegDataDescription
from niceml.data.datainfos.semsegdatainfo import SemSegData
from niceml.mlcomponents.resultanalyzers.tensors.tensormetric import TensorMetric

pyximport.install(setup_args={"include_dirs": np.get_include()})
# pylint: disable=import-error,wrong-import-position,no-name-in-module
from niceml.mlcomponents.resultanalyzers.tensors.cytensoriou import cy_calc_iou


class TensorIoU(TensorMetric):
    """TensorMetric for calculating the IoU"""

    def __init__(
        self,
        key: str,
        threshold: float = 0.5,
    ):
        super().__init__(key)
        self.threshold = threshold
        self.data_description = None
        self.intersection_sum = None
        self.union_sum = None

    def start_analysis(self):
        self.data_description: SemSegDataDescription = (
            self.exp_context.instantiate_datadescription_from_yaml()
        )
        store_folder = join(self.output_folder, self.dataset_name)
        if not isdir(store_folder):
            makedirs(store_folder)

    def analyse_datapoint(
        self,
        data_key: str,
        data_predicted,
        data_loaded: SemSegData,
        additional_data: dict,
        **kwargs,
    ):
        data_predicted: np.ndarray
        gt_array: np.ndarray = data_loaded.mask_image.astype(float)
        if self.intersection_sum is None or self.union_sum is None:
            self.intersection_sum: np.ndarray = np.zeros(gt_array.shape[2])
            self.union_sum: np.ndarray = np.zeros(gt_array.shape[2])
        intersect, union = cy_calc_iou(data_predicted, gt_array, self.threshold)
        self.intersection_sum += intersect
        self.union_sum += union

    def get_final_metric(self) -> dict:
        class_iou = self.intersection_sum / self.union_sum
        mean_iou = float(np.mean(class_iou))
        iou_dict = dict(mean_iou=mean_iou)
        for idx, name in enumerate(self.data_description.get_class_names()):
            iou_dict[f"iou_{name}"] = float(class_iou[idx])

        return iou_dict
