"""Module of the MaskInstance that represents an error instance derived from a prediction mask"""

from dataclasses import dataclass
from typing import List

import numpy as np

from niceml.data.datadescriptions.outputdatadescriptions import OutputImageDataDescription
from niceml.mlcomponents.resultanalyzers.instancefinders.instancecontour import (
    InstanceContour,
)
from niceml.utilities.semseg.semseginstancelabeling import SemSegInstanceLabel


@dataclass
class MaskInstance:
    """Dataclass with infos about an error (instance) found on a predicted image."""

    mask: np.ndarray
    instance_contours: List[InstanceContour]
    instance_class_idx: int

    def to_semseg_instance_label(
        self, data_description: OutputImageDataDescription
    ) -> List[SemSegInstanceLabel]:
        """
        Transform this `MaskInstance` into a `SemSegInstanceLabel`
        Args:
            data_description: Data description to get the class name of `self.instance_class_idx`

        Returns:
            Created `SemSegInstanceLabel`
        """
        if self.instance_class_idx is None:
            raise ValueError("self.instance_class_idx is None")

        instance_labels = [
            SemSegInstanceLabel(
                class_name=data_description.get_output_channel_names()[
                    self.instance_class_idx
                ],
                class_index=self.instance_class_idx,
                mask=error.get_contour_mask(
                    target_shape=data_description.get_output_image_size()
                ),
            )
            for error in self.instance_contours
        ]
        return instance_labels
