"""Module for InstanceLabel"""
from abc import ABC, abstractmethod
from typing import Optional, Tuple

from attr import define

from niceml.utilities.colorutils import Color


@define
class InstanceLabel(ABC):  # pylint: disable =too-few-public-methods
    """Abstract class representing an instance of a found object. Additionally,
    this class is used for visualization purpose"""

    class_name: str
    class_index: Optional[int] = None
    color: Tuple[int] = None
    active: bool = None

    @abstractmethod
    def scale_label(self, scale_factor: float) -> "InstanceLabel":
        """
        Scales an instance label by a given `scale_factor`

        Args:
            scale_factor: Factor to scale the instance label by

        Returns:
            Scaled instance of this InstanceLabel
        """

    @abstractmethod
    def calc_iou(self, other: "InstanceLabel") -> float:
        """
        Calculates the IOU of two given `InstanceLabel`s

        Args:
            other: InstanceLabel to calculate the IOU for

        Returns:
            Calculated IOU
        """


def get_kind_of_instance_label_match(  # QUEST: move to 'instancelabelmatching'?
    pred_label: InstanceLabel,
    gt_label: InstanceLabel,
    iou: float,
    iou_threshold: float,
    hide_gt_over_thresh: bool,
) -> Tuple[InstanceLabel, InstanceLabel]:
    """
    Defines color and activation of `pred_label` and `gt_label`
    based on an `iou` and an `iou_threshold`. Red = gt label with no matching prediction label;
    Blue = prediction label with no matching gt label; Green = prediction label which
    matched at least one gt label in position and class; Yellow = prediction label
    which matched at least one gt label in position but not in class.

    Args:
        pred_label: Prediction instance label
        gt_label: Ground truth instance label
        iou: Iou of `pred_label` and `gt_label`
        iou_threshold: Threshold to decide which color and activation should be
            used for the prediction and ground truth instance labels
        hide_gt_over_thresh: Flag to hide the `gt_label` if the `iou` is above the `iou_threshold`

    Returns:
        Updated `pred_label` and `gt_label` including
        color and activation for instance label visualization
    """

    if iou >= iou_threshold:
        # pylint:disable=simplifiable-if-expression
        if pred_label.color != Color.GREEN:
            if pred_label.class_index != gt_label.class_index:
                pred_label.color = Color.YELLOW
            else:
                pred_label.color = Color.GREEN

        if not hide_gt_over_thresh:
            gt_label.active = True
            gt_label.color = Color.RED
        else:
            gt_label.active = False

    else:
        if pred_label.color not in (Color.GREEN, Color.YELLOW):
            pred_label.color = Color.BLUE

        if gt_label.active is None or gt_label.active:
            gt_label.active = True
            gt_label.color = Color.RED

    pred_label.active = True
    return pred_label, gt_label
