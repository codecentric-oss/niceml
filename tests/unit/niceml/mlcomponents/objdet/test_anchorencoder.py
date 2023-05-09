# pylint: disable=duplicate-code
import time
from typing import List

import numpy as np
import pytest

from niceml.mlcomponents.objdet.anchorencoding import (
    AnchorEncoder,
    OptimizedAnchorEncoder,
    SimpleAnchorEncoder,
)
from niceml.mlcomponents.objdet.anchorgenerator import AnchorGenerator
from niceml.utilities.boundingboxes.bboxlabeling import ObjDetInstanceLabel
from niceml.utilities.boundingboxes.boundingbox import (
    IGNORE_MASK_VALUE,
    NEGATIVE_MASK_VALUE,
    POSITIVE_MASK_VALUE,
    BoundingBox,
)
from niceml.utilities.imagesize import ImageSize


@pytest.fixture
def box_variance() -> List[float]:
    box_variance = [0.1, 0.1, 0.2, 0.2]
    return box_variance


@pytest.mark.parametrize(
    "encoder_class,gt_idxes",
    [
        (SimpleAnchorEncoder, [10, 586, 7560, 93540]),
        (OptimizedAnchorEncoder, [10, 586, 7560, 93540]),
        (SimpleAnchorEncoder, []),
        (OptimizedAnchorEncoder, []),
    ],
)
def test_anchor_featuremap_generation(
    encoder_class, gt_idxes: List[int], box_variance: List[float]
):  # pylint: disable=too-many-locals
    anchor_gen = AnchorGenerator()
    image_size = ImageSize(1024, 1024)
    aspect_ratios: List[float] = [0.5, 1, 2.0]
    anchor_scales: List[float] = [1.0, 1.25, 1.6]
    scale = 8
    base_area_side = 4
    num_classes = 2

    anchor_list: List[BoundingBox] = anchor_gen.gen_anchors_for_featuremap(
        image_size=image_size,
        scale=scale,
        anchor_scales=anchor_scales,
        aspect_ratios=aspect_ratios,
        base_area_side=base_area_side,
    )

    gt_labels: List[ObjDetInstanceLabel] = [
        ObjDetInstanceLabel(
            class_name="",
            bounding_box=anchor_list[gt_idx],
            class_index=idx % num_classes,
        )
        for idx, gt_idx in enumerate(gt_idxes)
    ]

    encoder: AnchorEncoder = encoder_class()
    cur = time.time()
    encoding_array = encoder.encode_anchors(
        anchor_list=anchor_list,
        gt_labels=gt_labels,
        num_classes=num_classes,
        box_variance=box_variance,
    )
    print(f"Time: {time.time() - cur:0.4f}s")

    count_pos = np.sum(encoding_array[:, 4] == POSITIVE_MASK_VALUE)
    count_ignore = np.sum(encoding_array[:, 4] == IGNORE_MASK_VALUE)
    count_negative = np.sum(encoding_array[:, 4] == NEGATIVE_MASK_VALUE)
    assert count_pos >= len(gt_idxes)
    assert count_ignore >= len(gt_idxes)
    assert count_negative > 0.9 * len(anchor_list)
    assert encoding_array.shape == (len(anchor_list), 4 + 1 + num_classes)

    negative_sum = np.sum(
        encoding_array[encoding_array[:, 4] == NEGATIVE_MASK_VALUE, 5:]
    )
    assert negative_sum == 0
