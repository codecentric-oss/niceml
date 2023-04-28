"""Module for ObjDetDataDescription"""
from dataclasses import dataclass
from typing import List

from niceml.data.datadescriptions.inputdatadescriptions import InputImageDataDescription
from niceml.data.datadescriptions.outputdatadescriptions import (
    OutputObjDetDataDescription,
)
from niceml.utilities.imagesize import ImageSize


@dataclass
class ObjDetDataDescription(  # pylint: disable=too-many-instance-attributes
    OutputObjDetDataDescription, InputImageDataDescription
):
    """The default implementation for OutputObjDetDataDescription"""

    featuremap_scales: List[int]
    classes: List[str]  # QUEST: better naming?
    input_image_size: ImageSize
    anchor_scales: List[float]
    anchor_aspect_ratios: List[float]
    anchor_base_area_side: float  # QUEST: better naming?
    box_variance: List[float]
    input_channel_count: int = 3
    coordinates_count: int = 4

    def get_box_variance(self) -> List[float]:
        """Returns variance of bounding boxes"""
        return self.box_variance

    def get_anchorcount_for_scale(self, scale: int) -> int:
        """Calculates the anchor count for one feature map"""
        feature_width: int = self.input_image_size.width // scale
        feature_height: int = self.input_image_size.height // scale
        return feature_height * feature_width * self.get_anchorcount_per_feature()

    def get_coordinates_count(self) -> int:
        """Returns the number of coordinates of bounding boxes"""
        return self.coordinates_count

    def get_anchorcount_per_feature(self) -> int:
        """Returns the number of anchors per feature"""
        return len(self.anchor_scales) * len(self.anchor_aspect_ratios)

    def get_featuremap_scales(self) -> List[int]:
        """Returns the scale of feature maps"""
        return self.featuremap_scales

    def get_input_image_size(self) -> ImageSize:
        """Returns the size of the input image(s)"""
        return self.input_image_size

    def get_input_channel_count(self) -> int:
        """Returns the number of input channels"""
        return self.input_channel_count

    def get_anchor_aspect_ratios(self) -> List[float]:
        """Returns the aspect ratio of the anchors"""
        return self.anchor_aspect_ratios

    def get_anchor_scales(self) -> List[float]:
        """Returns the scale of the anchors"""
        return self.anchor_scales

    def get_base_area_side(self) -> float:
        """Returns the base area side of the anchors"""  # QUEST: what is this?
        return self.anchor_base_area_side

    def get_output_class_names(self) -> List[str]:
        """Returns the names of the output classes"""
        return self.classes
