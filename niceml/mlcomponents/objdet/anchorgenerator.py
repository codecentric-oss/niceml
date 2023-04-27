"""Module for the anchorgenerator"""
from math import sqrt
from typing import List, Tuple

from niceml.data.datadescriptions.outputdatadescriptions import (
    OutputObjDetDataDescription,
)
from niceml.utilities.boundingboxes.bboxconversion import (
    bounding_box_from_absolute_cxcywh,
)
from niceml.utilities.boundingboxes.boundingbox import BoundingBox
from niceml.utilities.imagesize import ImageSize


class AnchorGenerator:
    """Class for generating anchors for object detection"""

    def generate_anchors(
        self, data_description: OutputObjDetDataDescription
    ) -> List[BoundingBox]:
        """Generate anchors for all feature maps and appends them"""
        out_anchors = []
        for feature_map_scale in data_description.get_featuremap_scales():
            out_anchors += self.gen_anchors_for_featuremap(
                image_size=data_description.get_input_image_size(),
                scale=feature_map_scale,
                aspect_ratios=data_description.get_anchor_aspect_ratios(),
                anchor_scales=data_description.get_anchor_scales(),
                base_area_side=data_description.get_base_area_side(),
            )
        return out_anchors

    def gen_anchors_for_featuremap(  # pylint: disable=too-many-locals,too-many-arguments
        self,
        image_size: ImageSize,
        scale: int,
        aspect_ratios: List[float],
        anchor_scales: List[float],
        base_area_side: float,
    ) -> List[BoundingBox]:
        """Generates anchors for one featuremap"""

        steps_width = image_size.width // scale
        steps_height = image_size.height // scale
        area: float = (base_area_side * scale) ** 2

        width_height_list = calculate_anchor_width_height_list(
            aspect_ratios, anchor_scales, area
        )
        bbox_list: List[BoundingBox] = []
        for y_pos in range(steps_height):
            for x_pos in range(steps_width):
                center_x = (x_pos + 0.5) * scale
                center_y = (y_pos + 0.5) * scale
                for cur_width, cur_height in width_height_list:
                    bounding_box: BoundingBox = bounding_box_from_absolute_cxcywh(
                        center_x, center_y, cur_width, cur_height
                    )
                    bbox_list.append(bounding_box)
        return bbox_list


def calculate_anchor_width_height_list(
    aspect_ratios: List[float], anchor_scales: List[float], area: float
) -> List[Tuple[float, float]]:
    """calculates the widths and heights for one featuremap"""
    width_height_list = []
    for cur_ratio in aspect_ratios:
        anchor_height = sqrt(area / cur_ratio)
        anchor_width = area / anchor_height
        for cur_scale in anchor_scales:
            width_height_list.append(
                (anchor_width * cur_scale, anchor_height * cur_scale)
            )

    return width_height_list
