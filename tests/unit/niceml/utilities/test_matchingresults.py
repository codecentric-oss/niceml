from typing import List

import pytest

from niceml.utilities.boundingboxes.bboxlabeling import ObjDetInstanceLabel
from niceml.utilities.boundingboxes.boundingbox import BoundingBox
from niceml.utilities.instancelabeling import InstanceLabel
from niceml.utilities.matchingresult import (
    MatchingResult,
    match_classification_prediction_and_gt,
    match_detection_prediction_and_gt,
)


@pytest.fixture
def four_disjunkt_instance_labels() -> List[InstanceLabel]:
    """Fixture for four dijunkt instance labels"""

    return [
        ObjDetInstanceLabel(
            class_name="p1",
            class_index=0,
            active=True,
            bounding_box=BoundingBox(0, 0, 10, 10),
        ),
        ObjDetInstanceLabel(
            class_name="c1",
            class_index=1,
            active=True,
            bounding_box=BoundingBox(15, 0, 10, 10),
        ),
        ObjDetInstanceLabel(
            class_name="c1",
            class_index=1,
            active=True,
            bounding_box=BoundingBox(0, 15, 10, 10),
        ),
        ObjDetInstanceLabel(
            class_name="c1",
            class_index=1,
            active=True,
            bounding_box=BoundingBox(15, 15, 10, 10),
        ),
    ]


@pytest.fixture
def one_surrounding_instance_labels() -> List[InstanceLabel]:
    """Fixture for one surrounding instance label"""
    return [
        ObjDetInstanceLabel(
            class_name="c1",
            class_index=1,
            active=True,
            bounding_box=BoundingBox(0, 0, 30, 30),
        ),
    ]


@pytest.fixture
def one_upper_left_instance_label() -> List[InstanceLabel]:
    """Fixture for one upper left instance label"""
    return [
        ObjDetInstanceLabel(
            class_name="c1",
            class_index=1,
            active=True,
            bounding_box=BoundingBox(0, 0, 12, 12),
        ),
    ]


def test_matching_case1(
    four_disjunkt_instance_labels: List[InstanceLabel],
    one_surrounding_instance_labels: List[InstanceLabel],
):
    """
    Case1:

    true_pos + false_neg = count of gt labels

    match_classification_prediction_and_gt:
    true_pos: 1
    false_pos: 1
    false_neg: 0

    match_detection_prediction_and_gt
    true_pos: 1
    false_pos: 0
    false_neg: 0
    """

    gt_labels = one_surrounding_instance_labels
    pred_labels = four_disjunkt_instance_labels

    match_result_classification: MatchingResult = (
        match_classification_prediction_and_gt(
            gt_labels=gt_labels,
            pred_labels=pred_labels,
            matching_iou=0.0,
        )
    )

    assert len(match_result_classification.true_pos) == 1
    assert len(match_result_classification.false_pos) == 1
    assert len(match_result_classification.false_neg) == 0

    match_result_detection: MatchingResult = match_detection_prediction_and_gt(
        gt_labels=gt_labels,
        pred_labels=pred_labels,
        matching_iou=0.0,
    )

    assert len(match_result_detection.true_pos) == 1
    assert len(match_result_detection.false_pos) == 0
    assert len(match_result_detection.false_neg) == 0


def test_matching_case2(
    four_disjunkt_instance_labels: List[InstanceLabel],
    one_surrounding_instance_labels: List[InstanceLabel],
):
    """
    Case2:

    true_pos + false_neg = count of gt labels

    match_classification_prediction_and_gt:
    true_pos: 3
    false_pos: 0
    false_neg: 1

    match_detection_prediction_and_gt
    true_pos: 4
    false_pos: 0
    false_neg: 0

    """

    gt_labels = four_disjunkt_instance_labels
    pred_labels = one_surrounding_instance_labels

    match_result_classification: MatchingResult = (
        match_classification_prediction_and_gt(
            gt_labels=gt_labels,
            pred_labels=pred_labels,
            matching_iou=0.0,
        )
    )

    assert len(match_result_classification.true_pos) == 3
    assert len(match_result_classification.false_pos) == 0
    assert len(match_result_classification.false_neg) == 1

    match_result_detection: MatchingResult = match_detection_prediction_and_gt(
        gt_labels=gt_labels,
        pred_labels=pred_labels,
        matching_iou=0.0,
    )

    assert len(match_result_detection.true_pos) == 4
    assert len(match_result_detection.false_pos) == 0
    assert len(match_result_detection.false_neg) == 0


def test_matching_case3(
    four_disjunkt_instance_labels: List[InstanceLabel],
    one_upper_left_instance_label: List[InstanceLabel],
):
    """
    Case3:

    true_pos + false_neg = count of gt labels

    match_classification_prediction_and_gt:
    true_pos: 0
    false_pos: 1
    false_neg: 4

    match_detection_prediction_and_gt
    true_pos: 1
    false_pos: 0
    false_neg: 3


    """

    gt_labels = four_disjunkt_instance_labels
    pred_labels = one_upper_left_instance_label

    match_result_classification: MatchingResult = (
        match_classification_prediction_and_gt(
            gt_labels=gt_labels,
            pred_labels=pred_labels,
            matching_iou=0.0,
        )
    )

    assert len(match_result_classification.true_pos) == 0
    assert len(match_result_classification.false_pos) == 1
    assert len(match_result_classification.false_neg) == 4

    match_result_detection: MatchingResult = match_detection_prediction_and_gt(
        gt_labels=gt_labels,
        pred_labels=pred_labels,
        matching_iou=0.0,
    )

    assert len(match_result_detection.true_pos) == 1
    assert len(match_result_detection.false_pos) == 0
    assert len(match_result_detection.false_neg) == 3


def test_matching_case4(
    four_disjunkt_instance_labels: List[InstanceLabel],
    one_upper_left_instance_label: List[InstanceLabel],
):
    """
    Case4:

    true_pos + false_neg = count of gt labels

    match_classification_prediction_and_gt:
    true_pos: 0
    false_pos: 4
    false_neg: 1

    match_detection_prediction_and_gt
    true_pos: 1
    false_pos: 3
    false_neg: 0


    """

    gt_labels = one_upper_left_instance_label
    pred_labels = four_disjunkt_instance_labels

    match_result_classification: MatchingResult = (
        match_classification_prediction_and_gt(
            gt_labels=gt_labels,
            pred_labels=pred_labels,
            matching_iou=0.0,
        )
    )

    assert len(match_result_classification.true_pos) == 0
    assert len(match_result_classification.false_pos) == 4
    assert len(match_result_classification.false_neg) == 1

    match_result_detection: MatchingResult = match_detection_prediction_and_gt(
        gt_labels=gt_labels,
        pred_labels=pred_labels,
        matching_iou=0.0,
    )

    assert len(match_result_detection.true_pos) == 1
    assert len(match_result_detection.false_pos) == 3
    assert len(match_result_detection.false_neg) == 0
