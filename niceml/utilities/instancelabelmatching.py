"""Module for instance label matching"""

from typing import List, Tuple

from niceml.utilities.colorutils import Color
from niceml.utilities.instancelabeling import (
    InstanceLabel,
    get_kind_of_instance_label_match,
)


def get_kind_of_label_match(
    pred_label_list: List[InstanceLabel],
    gt_label_list: List[InstanceLabel],
    hide_gt_over_thresh: bool = True,
    iou_threshold: float = 0.5,
) -> Tuple[List[InstanceLabel], List[InstanceLabel]]:
    """
    Creates a list of InstanceLabels for prediction labels and ground truth labels.
    Based on the iou of the prediction label (mask or bbox) and
    the ground truth label (=gt; mask or bbox), the labels are given a color and
    are active or not. Red = gt label with no matching prediction label;
    Blue = prediction label with no matching gt label; Green = prediction label which
    matched at least one gt label in position and class; Yellow = prediction label
    which matched at least one gt label in position but not in class.

    Args:
        pred_label_list: label list of the prediction labels
        gt_label_list: label list of the ground truth labels
        hide_gt_over_thresh: flag to hide the ground truth labels if the ground truth label
            have an iou >= `iou_threshold` with a prediction label
        iou_threshold: threshold to determine kind of match by iou

    Returns:
        List of InstanceLabel for prediction labels and ground truth labels
    """

    if len(pred_label_list) == 0:
        for gt_label in gt_label_list:
            gt_label.active = True
            gt_label.color = Color.RED
    else:
        for pred_label in pred_label_list:
            if len(gt_label_list) == 0:
                pred_label.color = Color.BLUE
                pred_label.active = True
            for gt_label in gt_label_list:

                iou = pred_label.calc_iou(other=gt_label)

                pred_label, gt_label = get_kind_of_instance_label_match(
                    pred_label=pred_label,
                    gt_label=gt_label,
                    iou=iou,
                    iou_threshold=iou_threshold,
                    hide_gt_over_thresh=hide_gt_over_thresh,
                )

    return pred_label_list, gt_label_list
