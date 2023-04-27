"""Module for the multichannel instance finder"""

from typing import Any, List, Optional

import numpy as np

from niceml.data.datainfos.datainfo import DataInfo
from niceml.mlcomponents.resultanalyzers.instancefinders.instancecontour import (
    InstanceContour,
)
from niceml.mlcomponents.resultanalyzers.instancefinders.instancefinder import (
    InstanceFinder,
)
from niceml.mlcomponents.resultanalyzers.instancefinders.maskinstance import MaskInstance
from niceml.mlcomponents.resultanalyzers.tensors.semsegdataiterator import (
    SemSegPredictionContainer,
)
from niceml.utilities.imageutils import (
    binarize_multichannel_image,
    find_contours_in_binary_image,
)


class MultiChannelInstanceFinder(InstanceFinder):
    """Instance finder for SemSeg predictions with more than one channel (classes)."""

    # pylint: disable = too-many-arguments
    def __init__(
        self,
        key: str = "multichannelinstancefinder",
        min_area: int = 10,
        max_area: int = 2000000,
        threshold: float = 0.5,
    ):
        super().__init__(
            key=key,
            min_area=min_area,
            max_area=max_area,
            threshold=threshold,
        )

    # pylint: disable = too-many-arguments
    def analyse_datapoint(
        self,
        data_key: str,
        data_predicted: SemSegPredictionContainer,
        data_loaded: Optional[DataInfo] = None,
        additional_data: Optional[dict] = None,
        dyn_threshold: Optional[float] = None,
        **kwargs,
    ) -> Optional[Any]:
        """extract information about multiple predicted errors
        (instances) from multichannel image.
        The dynamic threshold can be used to override the threshold"""

        dyn_threshold = dyn_threshold or self.threshold
        binarize_multichannel_images, _ = binarize_multichannel_image(
            image_index=data_predicted.max_prediction_idxes,
            image_scores=data_predicted.max_prediction_values,
            threshold=dyn_threshold,
        )
        mask_instances: List[MaskInstance] = []

        for class_idx, curr_binary_img in binarize_multichannel_images.items():
            instance_contours = find_contours_in_binary_image(
                binary_image=curr_binary_img.astype(np.uint8),
                min_area=self.min_area,
                max_area=self.max_area,
            )
            instance_contours = [
                InstanceContour(
                    contour=error_contour,
                    class_idx=int(float(class_idx)),
                )
                for error_contour in instance_contours
            ]
            mask_instance = MaskInstance(
                mask=curr_binary_img,
                instance_contours=instance_contours,
                instance_class_idx=int(float(class_idx)),
            )
            mask_instances.append(mask_instance)

        return mask_instances

    def get_final_metric(self) -> Optional[dict]:
        """returns empty dict"""
        return {}
