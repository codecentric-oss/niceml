from typing import List, Tuple

import numpy as np
import pytest

from niceml.utilities.colorutils import Color
from niceml.utilities.instancelabelmatching import get_kind_of_label_match
from niceml.utilities.semseg.semseginstancelabeling import SemSegInstanceLabel
from tests.unit.niceml.utilities.semseg.testutils import get_random_semseg_mask


@pytest.mark.parametrize(
    "image_shape,square_width,square_height,amount_pred_label,amount_gt_label,"
    "pred_class_label_list,pred_class_index_list,gt_class_label_list,"
    "gt_class_index_list,iou_threshold,matching_results,seed",
    [
        (
            (20, 20),
            8,
            8,
            1,
            2,
            ["1"],
            [1],
            ["1", "2"],
            [1, 2],
            0.5,
            [(True, Color.YELLOW), (True, Color.RED), (False, None)],
            96,
        ),
        (
            (10, 10),
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
            (20, 20),
            8,
            8,
            1,
            2,
            ["1"],
            [1],
            ["1", "1"],
            [1, 1],
            0.5,
            [(True, Color.GREEN), (True, Color.RED), (False, None)],
            96,
        ),
        (
            (14, 14),
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
            (14, 14),
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
    ],
)
def test_get_kind_of_error_mask_matching(
    image_shape: Tuple[int, int],
    square_width: int,
    square_height: int,
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

    pred_label_list: List[SemSegInstanceLabel] = []

    gt_label_list: List[SemSegInstanceLabel] = []

    for pred_label_idx in range(amount_pred_label):
        semseg_label_mask, _ = get_random_semseg_mask(
            image_shape=image_shape,
            random_generator=random_generator,
            class_list=[str(pred_class_index_list[pred_label_idx])],
            square_width=square_width,
            square_height=square_height,
        )

        pred_label = SemSegInstanceLabel(
            mask=semseg_label_mask,
            class_name=pred_class_label_list[pred_label_idx],
            class_index=pred_class_index_list[pred_label_idx],
        )
        pred_label_list.append(pred_label)

    for gt_label_idx in range(amount_gt_label):
        gt_mask, _ = get_random_semseg_mask(
            image_shape=image_shape,
            random_generator=random_generator,
            class_list=[str(gt_class_label_list[gt_label_idx])],
            square_width=square_width,
            square_height=square_height,
        )

        gt_label = SemSegInstanceLabel(
            mask=gt_mask,
            class_name=gt_class_label_list[gt_label_idx],
            class_index=gt_class_index_list[gt_label_idx],
        )

        gt_label_list.append(gt_label)

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
