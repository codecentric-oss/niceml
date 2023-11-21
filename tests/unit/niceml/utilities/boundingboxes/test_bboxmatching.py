from typing import List, Tuple

import numpy as np
import pytest

from niceml.utilities.boundingboxes.bboxlabeling import ObjDetInstanceLabel
from niceml.utilities.boundingboxes.boundingbox import BoundingBox, split_bounding_boxes
from niceml.utilities.colorutils import Color
from niceml.utilities.imagesize import ImageSize
from niceml.utilities.instancelabelmatching import get_kind_of_label_match
from niceml.utilities.matchingresult import (
    MatchingResult,
    match_classification_prediction_and_gt,
    match_detection_prediction_and_gt,
)
from tests.unit.niceml.data.conftest import get_random_bounding_box


def test_match_prediction_and_gt():
    surrounding_box: BoundingBox = BoundingBox(0, 0, 1200, 1000)

    bbox_predictions: List[BoundingBox] = split_bounding_boxes(surrounding_box, 4, 4)
    pred_instance_labels: List[ObjDetInstanceLabel] = [
        ObjDetInstanceLabel(
            class_name=f"{idx% 2}", class_index=idx % 2, bounding_box=box
        )
        for idx, box in enumerate(bbox_predictions)
    ]
    bbox_gts = split_bounding_boxes(surrounding_box, 4, 4)
    gt_instance_labels: List[ObjDetInstanceLabel] = [
        ObjDetInstanceLabel(
            class_name=f"{idx % 3}", class_index=idx % 3, bounding_box=box
        )
        for idx, box in enumerate(bbox_gts)
    ]

    classification_matching_result: MatchingResult = (
        match_classification_prediction_and_gt(
            pred_instance_labels[2:], gt_instance_labels[:-2]
        )
    )

    assert len(classification_matching_result.false_neg) == 10
    assert len(classification_matching_result.false_pos) == 10
    assert len(classification_matching_result.true_pos) == 4

    detection_matching_result: MatchingResult = match_detection_prediction_and_gt(
        pred_instance_labels[2:], gt_instance_labels[:-2]
    )

    assert len(detection_matching_result.false_neg) == 2
    assert len(detection_matching_result.false_pos) == 2
    assert len(detection_matching_result.true_pos) == 12


@pytest.mark.parametrize(
    "image_size,bbox_width,bbox_height,amount_pred_label,amount_gt_label,"
    "pred_class_label_list,pred_class_index_list,gt_class_label_list,"
    "gt_class_index_list,iou_threshold,matching_results,seed",
    [
        (
            ImageSize(14, 14),
            4,
            4,
            1,
            0,
            ["1"],
            [1],
            ["1", "1"],
            [1, 1],
            0.5,
            [(True, Color.BLUE)],
            96,
        ),
        (
            ImageSize(14, 14),
            4,
            4,
            0,
            2,
            ["1"],
            [1],
            ["1", "1"],
            [1, 1],
            0.5,
            [(True, Color.RED), (True, Color.RED)],
            96,
        ),
        (
            ImageSize(14, 14),
            4,
            4,
            1,
            2,
            ["1"],
            [1],
            ["1", "1"],
            [1, 1],
            0.5,
            [(True, Color.GREEN), (False, None), (True, Color.RED)],
            96,
        ),
        (
            ImageSize(10, 10),
            4,
            4,
            1,
            2,
            ["1"],
            [1],
            ["1", "1"],
            [1, 1],
            0.5,
            [(True, Color.BLUE), (True, Color.RED), (True, Color.RED)],
            27,
        ),
        (
            ImageSize(20, 20),
            7,
            7,
            1,
            2,
            ["1"],
            [1],
            ["2", "1"],
            [2, 1],
            0.5,
            [(True, Color.YELLOW), (False, None), (True, Color.RED)],
            96,
        ),
    ],
)
def test_get_kind_of_bbox_match(
    image_size: ImageSize,
    bbox_width: int,
    bbox_height: int,
    amount_pred_label: int,
    amount_gt_label: int,
    pred_class_label_list: List[str],
    pred_class_index_list: List[int],
    gt_class_label_list: List[str],
    gt_class_index_list: List[int],
    iou_threshold: float,
    matching_results: List[Tuple[bool, Color]],
    seed: int,
):  # pylint: disable = too-many-arguments, too-many-locals
    random_generator = np.random.default_rng(seed=seed)

    pred_label_list: List[ObjDetInstanceLabel] = []

    gt_label_list: List[ObjDetInstanceLabel] = []

    for pred_label_idx in range(amount_pred_label):
        bbox = get_random_bounding_box(
            img_size=image_size,
            random_generator=random_generator,
            bbox_width=bbox_width,
            bbox_height=bbox_height,
        )

        pred_label = ObjDetInstanceLabel(
            class_name=pred_class_label_list[pred_label_idx],
            class_index=pred_class_index_list[pred_label_idx],
            bounding_box=bbox,
        )

        pred_label_list.append(pred_label)

    for gt_label_idx in range(amount_gt_label):
        bbox = get_random_bounding_box(
            img_size=image_size,
            random_generator=random_generator,
            bbox_width=bbox_width,
            bbox_height=bbox_height,
        )

        pred_label = ObjDetInstanceLabel(
            class_name=gt_class_label_list[gt_label_idx],
            class_index=gt_class_index_list[gt_label_idx],
            bounding_box=bbox,
        )

        gt_label_list.append(pred_label)

    pred_result_list, gt_result_label_list = get_kind_of_label_match(
        pred_label_list=pred_label_list,
        gt_label_list=gt_label_list,
        iou_threshold=iou_threshold,
    )

    for pred_result_idx in range(amount_pred_label):
        assert (
            pred_result_list[pred_result_idx].active
            == matching_results[pred_result_idx][0]
        )
        assert (
            pred_result_list[pred_result_idx].color
            == matching_results[pred_result_idx][1]
        )
    for gt_label_idx in range(amount_gt_label):
        assert (
            gt_result_label_list[gt_label_idx].active
            == matching_results[amount_pred_label + gt_label_idx][0]
        )
        assert (
            gt_result_label_list[gt_label_idx].color
            == matching_results[amount_pred_label + gt_label_idx][1]
        )
