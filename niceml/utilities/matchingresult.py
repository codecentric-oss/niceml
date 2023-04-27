"""Module for abstract MatchingResult class"""

from abc import ABC
from typing import List, Optional, Set

from attr import define

from niceml.utilities.instancelabeling import InstanceLabel


@define
class MatchingResult(ABC):
    """Abstract class to calculate precision (per class) and recall (per class)
    based on `true_pos`, `false_pos` and `false_neg` instance labels

    Parameters:
        true_pos: true_positives = List of correctly predicted instance labels
            (prediction = ground truth)
        false_pos: false_positives = List of instance labels that were found too much
            (prediction, but no ground truth)
        false_neg: false_negatives = List of instance labels that were not found correctly
            (ground truth, but no prediction)
    """

    true_pos: List[InstanceLabel]
    false_pos: List[InstanceLabel]
    false_neg: List[InstanceLabel]

    def __add__(self, other: "MatchingResult") -> "MatchingResult":
        """Adds two MatchingResult objects"""
        return MatchingResult(
            true_pos=self.true_pos + other.true_pos,
            false_pos=self.false_pos + other.false_pos,
            false_neg=self.false_neg + other.false_neg,
        )

    def calculate_precision(self) -> float:
        """Calculates the precision"""
        if len(self.true_pos) == 0:
            return 0.0
        return len(self.true_pos) / (len(self.true_pos) + len(self.false_pos))

    def calculate_recall(self) -> float:
        """Calculates the recall"""
        if len(self.true_pos) == 0:
            return 0.0
        return len(self.true_pos) / (len(self.true_pos) + len(self.false_neg))

    def get_containing_class_names(self) -> Set[str]:
        """Returns all class names of the true positives, false positives and false negatives"""
        return {
            label.class_name
            for label in self.true_pos + self.false_pos + self.false_neg
        }

    def calculate_per_class_recall(
        self, target_classes: Optional[List[str]] = None
    ) -> dict:
        """Calculates the recall per target class"""
        cls_recall_dict = {}
        try:
            if target_classes is None:
                class_names = self.get_containing_class_names()
            else:
                class_names = set(target_classes)

            for class_name in class_names:
                true_pos = [
                    label for label in self.true_pos if label.class_name == class_name
                ]
                false_neg = [
                    label for label in self.false_neg if label.class_name == class_name
                ]
                if len(true_pos) + len(false_neg) != 0:
                    cls_recall_dict[class_name] = len(true_pos) / (
                        len(true_pos) + len(false_neg)
                    )
                else:
                    cls_recall_dict[class_name] = 0.0

            return cls_recall_dict

        except AttributeError as error:
            raise Exception(  # pylint: disable=broad-except
                f"{error} - label should contain ObjDetInstanceLabel and BoundingBox"
            ) from error

    def calculate_per_class_precision(
        self, target_classes: Optional[Set[str]] = None
    ) -> dict:
        """Calculates the precision per class"""
        cls_precision_dict = {}
        try:
            if target_classes is None:
                class_names = self.get_containing_class_names()
            else:
                class_names = target_classes

            for class_name in class_names:
                true_pos = [
                    label for label in self.true_pos if label.class_name == class_name
                ]
                false_pos = [
                    label for label in self.false_pos if label.class_name == class_name
                ]
                if (len(true_pos) + len(false_pos)) != 0:
                    cls_precision_dict[class_name] = len(true_pos) / (
                        len(true_pos) + len(false_pos)
                    )
                else:
                    cls_precision_dict[class_name] = 0.0

            return cls_precision_dict

        except AttributeError as error:
            # pylint: disable=broad-exception-raised
            raise Exception(
                f"{error} - label should contain ObjDetInstanceLabel and BoundingBox"
            ) from error


def match_detection_prediction_and_gt(
    pred_labels: List[InstanceLabel],
    gt_labels: List[InstanceLabel],
    matching_iou: float = 0.5,
) -> MatchingResult:
    """
    Matches regions of predictions to ground truth label regions and checks
    if the ground truth label could be found by minimum one prediction.
    Not matching ground truth labels are counted as false negative.
    Not matching predictions are counted as false positives.
    The sum of false negative and true positive is the amount
    of ground truth labels

    Args:
        pred_labels: prediction labels (bounding box or mask)
        gt_labels:  ground truth labels (bounding box or mask)
        matching_iou: Minimum iou for region matching

    Returns:
        MatchingResult with true_pos, false_pos and false_neg
    """

    matched_pred_labels: Set[int] = set()
    classification_true_pos_list: List[InstanceLabel] = []
    classification_false_pos_list: List[InstanceLabel] = []
    classification_false_neg_list: List[InstanceLabel] = []

    for cur_gt_label in gt_labels:
        cur_gt_true_pos = False
        for pred_idx, cur_pred_label in enumerate(pred_labels):
            cur_iou = cur_gt_label.calc_iou(cur_pred_label)

            if cur_iou > matching_iou:
                matched_pred_labels.add(pred_idx)
                cur_gt_true_pos = True

        if cur_gt_true_pos:
            classification_true_pos_list.append(cur_gt_label)
        else:
            classification_false_neg_list.append(cur_gt_label)

    missed_pred_label_idxes = [
        index for index in range(len(pred_labels)) if index not in matched_pred_labels
    ]
    for index in missed_pred_label_idxes:
        cur_pred_label = pred_labels[index]
        classification_false_pos_list.append(cur_pred_label)

    return MatchingResult(
        true_pos=classification_true_pos_list,
        false_pos=classification_false_pos_list,
        false_neg=classification_false_neg_list,
    )


def match_classification_prediction_and_gt(
    pred_labels: List[InstanceLabel],
    gt_labels: List[InstanceLabel],
    matching_iou: float = 0.5,
) -> MatchingResult:
    """
    Matches region and class of predictions to ground truth labels and checks
    if the ground truth label could be found by minimum one prediction.
    Not matching ground truth labels are counted as false negative.
    Not matching predictions are counted as false positives.
    The sum of false negative and true positive is the amount
    of ground truth labels

    Args:
        pred_labels: prediction labels (bounding box or mask)
        gt_labels:  ground truth labels (bounding box or mask)
        matching_iou: Minimum iou for region matching

    Returns:
        MatchingResult with true_pos, false_pos and false_neg
    """

    matched_pred_labels: Set[int] = set()
    classification_true_pos_list: List[InstanceLabel] = []
    classification_false_pos_list: List[InstanceLabel] = []
    classification_false_neg_list: List[InstanceLabel] = []

    for cur_gt_label in gt_labels:
        cur_gt_true_pos = False
        for pred_idx, cur_pred_label in enumerate(pred_labels):
            cur_iou = cur_gt_label.calc_iou(cur_pred_label)

            if (
                cur_iou > matching_iou
                and cur_pred_label.class_name == cur_gt_label.class_name
            ):
                matched_pred_labels.add(pred_idx)
                cur_gt_true_pos = True

        if cur_gt_true_pos:
            classification_true_pos_list.append(cur_gt_label)
        else:
            classification_false_neg_list.append(cur_gt_label)

    missed_pred_label_idxes = [
        index for index in range(len(pred_labels)) if index not in matched_pred_labels
    ]
    for index in missed_pred_label_idxes:
        cur_pred_label = pred_labels[index]
        classification_false_pos_list.append(cur_pred_label)

    return MatchingResult(
        true_pos=classification_true_pos_list,
        false_pos=classification_false_pos_list,
        false_neg=classification_false_neg_list,
    )
