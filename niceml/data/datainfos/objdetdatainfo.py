"""Module for ObjDetDataInfo"""
from dataclasses import dataclass
from typing import List

import numpy as np

from niceml.data.datainfos.imagedatainfo import ImageDataInfo
from niceml.utilities.boundingboxes.bboxlabeling import ObjDetInstanceLabel


@dataclass
class ObjDetDataInfo(ImageDataInfo):
    """Contains all information for object detection"""

    labels: List[ObjDetInstanceLabel]
    class_count_in_dataset: int

    def get_identifier(self) -> str:
        if isinstance(self.image_location, dict):
            return self.image_location["uri"]

        return self.image_location.uri

    def get_info_dict(self) -> dict:
        info_dict = dict(filepath=self.get_identifier(), label_count=len(self.labels))
        info_dict.update(
            {f"class_{idx:04d}": 0 for idx in range(self.class_count_in_dataset)}
        )

        for curr_label in self.labels:
            info_dict[f"class_{curr_label.class_index:04d}"] += 1

        return info_dict


@dataclass
class ObjDetData:
    """Dataclass containing object detection data"""

    image: np.ndarray
    labels: List[ObjDetInstanceLabel]
