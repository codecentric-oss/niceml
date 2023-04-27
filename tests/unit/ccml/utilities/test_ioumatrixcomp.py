"""test for ioumatrix"""
# pylint: disable=duplicate-code
from math import isclose
from typing import List

import numpy as np
import pytest

from niceml.mlcomponents.objdet.anchorgenerator import AnchorGenerator
from niceml.utilities.boundingboxes.bboxconversion import (
    bbox_list_to_ullr_array,
    compute_target_gt_array,
)
from niceml.utilities.boundingboxes.bboxlabeling import ObjDetInstanceLabel
from niceml.utilities.boundingboxes.boundingbox import (
    IGNORE_MASK_VALUE,
    NEGATIVE_MASK_VALUE,
    POSITIVE_MASK_VALUE,
    BoundingBox,
    split_bounding_boxes,
)
from niceml.utilities.imagesize import ImageSize
from niceml.utilities.ioumatrix import compute_iou_matrix, compute_iou_matrix_optimized


@pytest.mark.parametrize(
    "first_split_list,second_split_list",
    [
        ([5, 10, 15], [7, 12, 14]),
        ([5, 8, 20, 40], [4, 9, 25, 50, 65]),
    ],
)
def test_compute_optimized_iou_mat(
    first_split_list: List[int], second_split_list: List[int]
):
    surrounding_box: BoundingBox = BoundingBox(0, 0, 1200, 1000)

    bbox_list_1: List[BoundingBox] = []
    for count in first_split_list:
        bbox_list_1 += split_bounding_boxes(surrounding_box, count, count)

    bbox_list_2 = []
    for count in second_split_list:
        bbox_list_2 += split_bounding_boxes(surrounding_box, count, count)

    bbox_array_1 = bbox_list_to_ullr_array(bbox_list_1)
    bbox_array_2 = bbox_list_to_ullr_array(bbox_list_2)

    # start = time.time()
    iou_mat_normal = compute_iou_matrix(bbox_array_1, bbox_array_2)
    # end1 = time.time()

    # time1 = end1 - start
    iou_mat_optimized = compute_iou_matrix_optimized(bbox_array_1, bbox_array_2)
    # time2 = time.time() - end1

    # assert time1 > time2, "Expected the optimized version to be faster"

    np.array_equal(iou_mat_optimized.toarray(), iou_mat_normal)


def test_compute_iou_matrix():  # pylint: disable=too-many-locals
    box_variance = (0.1, 0.1, 0.2, 0.2)
    anchor_gen = AnchorGenerator()
    image_size = ImageSize(1024, 1024)
    aspect_ratios: List[float] = [0.5, 1, 2.0]
    anchor_scales: List[float] = [1.0, 1.25, 1.6]
    box_variance = np.array(box_variance)
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

    gt_idxes = [10, 586, 7560, 93540]
    gt_labels: List[ObjDetInstanceLabel] = [
        ObjDetInstanceLabel(
            class_name="",
            bounding_box=anchor_list[gt_idx],
            class_index=idx % num_classes,
        )
        for idx, gt_idx in enumerate(gt_idxes)
    ]

    gt_boxes = [x.bounding_box for x in gt_labels]
    class_index_list = [x.class_index for x in gt_labels]

    anchor_array = bbox_list_to_ullr_array(anchor_list)
    gt_array = bbox_list_to_ullr_array(gt_boxes)
    iou_matrix = compute_iou_matrix(anchor_array, gt_array)
    assert iou_matrix.shape == (len(anchor_list), len(gt_idxes))
    assert iou_matrix.dtype == float
    assert isclose(np.max(iou_matrix), 1.0)
    assert np.min(iou_matrix) == 0.0

    target_array = compute_target_gt_array(
        anchor_array,
        gt_array,
        iou_matrix,
        box_variances=box_variance,
        class_index_array=np.array(class_index_list),
        num_classes=num_classes,
    )

    assert target_array.shape == (len(anchor_list), 4 + 1 + num_classes)
    assert np.max(target_array[:, 5]) == 1.0
    assert np.max(target_array[:, 6]) == 1.0

    pos_mask = target_array[:, 4] == POSITIVE_MASK_VALUE
    neg_mask = target_array[:, 4] == NEGATIVE_MASK_VALUE
    ign_mask = target_array[:, 4] == IGNORE_MASK_VALUE

    pos_mask_values = target_array[pos_mask]
    assert np.max(pos_mask_values[:, 5:]) == 1.0

    neg_mask_values = target_array[neg_mask]
    assert np.max(neg_mask_values[:, 5:]) == 0.0

    ign_mask_values = target_array[ign_mask]
    assert np.max(ign_mask_values[:, 5:]) == 0.0
