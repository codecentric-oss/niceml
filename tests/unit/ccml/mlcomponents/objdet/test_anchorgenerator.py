from math import isclose
from typing import List

from niceml.mlcomponents.objdet.anchorgenerator import (
    AnchorGenerator,
    calculate_anchor_width_height_list,
)
from niceml.utilities.boundingboxes.boundingbox import BoundingBox
from niceml.utilities.imagesize import ImageSize


def test_calculate_anchor_width_height_list():
    aspect_ratios: List[float] = [0.5, 1, 2.0]
    anchor_scales: List[float] = [1.0, 1.25, 1.6]
    area: float = 32 * 32
    width_height_list = calculate_anchor_width_height_list(
        aspect_ratios, anchor_scales, area
    )
    idx = 0

    for _ in aspect_ratios:
        for cur_scale in anchor_scales:
            width, height = width_height_list[idx]
            idx += 1
            assert isclose(width * height, area * (cur_scale**2))


def test_anchor_featuremap_generation():
    anchor_gen = AnchorGenerator()
    image_size = ImageSize(1024, 1024)
    aspect_ratios: List[float] = [0.5, 1, 2.0]
    anchor_scales: List[float] = [1.0, 1.25, 1.6]
    scale = 8
    base_area_side = 4

    anchor_list: List[BoundingBox] = anchor_gen.gen_anchors_for_featuremap(
        image_size=image_size,
        scale=scale,
        anchor_scales=anchor_scales,
        aspect_ratios=aspect_ratios,
        base_area_side=base_area_side,
    )
    assert len(anchor_list) == image_size.width * image_size.height / (
        scale**2
    ) * len(aspect_ratios) * len(anchor_scales)

    target_area = (base_area_side * scale) ** 2
    for anchor_scale, bbox in zip(anchor_scales, anchor_list):
        assert isclose(bbox.get_absolute_area(), (anchor_scale**2) * target_area)

    first_bbox = anchor_list[0]
    second_bbox = anchor_list[len(anchor_scales) * len(aspect_ratios)]

    # This checks that the anchors are generated in the same way as tf.reshape
    # would do it
    assert first_bbox.y_pos == second_bbox.y_pos
    assert first_bbox.x_pos < second_bbox.x_pos
