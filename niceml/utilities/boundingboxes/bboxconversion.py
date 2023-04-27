"""Module for bounding box conversion functions"""
from typing import List, Tuple, Union

import numpy as np

from niceml.utilities.boundingboxes.bboxencoding import encode_boxes
from niceml.utilities.boundingboxes.boundingbox import (
    IGNORE_MASK_VALUE,
    NEGATIVE_MASK_VALUE,
    POSITIVE_MASK_VALUE,
    BoundingBox,
)
from niceml.utilities.imagesize import ImageSize


def bbox_list_to_ullr_array(bbox_list: List[BoundingBox]) -> np.ndarray:
    """Converts a list of bounding boxes to a numpy array with (left, top, right, bottom)"""
    ullr_list = [bbox.get_absolute_ullr() for bbox in bbox_list]
    return np.array(ullr_list)


def convert_to_xywh(boxes: np.ndarray) -> np.ndarray:
    """
    Changes the box format from the format [left, top, right, bottom] to [upper left x,
    upper left y, width and height].

    Args:
        boxes: A tensor of rank 2 or higher with a shape of `(num_boxes, 4)` representing
            bounding boxes where each box is of the format `[left, top, right, bottom]`.

    Returns:
        Converted bounding boxes with shape same as that of boxes.
    """
    xys = boxes[:, :2]
    widths = boxes[:, 2] - boxes[:, 0]
    heights = boxes[:, 3] - boxes[:, 1]

    return np.concatenate(
        [xys, widths[:, np.newaxis], heights[:, np.newaxis], boxes[:, 4:]], axis=1
    )


def convert_to_ullr(boxes: np.ndarray):
    """Changes the box format from [x, y, width, height] to corner coordinates [xmin, ymin, xmax, ymax]

    Args:
        boxes: A tensor of rank 2 or higher with a shape of `( num_boxes, 4)`
            representing bounding boxes where each box is of the format
            `[x, y, width, height]`.

    Returns:
        converted boxes with shape same as that of boxes.
    """
    return np.concatenate(
        [boxes[:, :2], boxes[:, :2] + boxes[:, 2:4], boxes[:, 4:]], axis=1
    )


def compute_target_gt_array(  # pylint: disable=too-many-arguments,too-many-locals
    anchor_boxes: np.ndarray,
    gt_boxes: np.ndarray,
    iou_matrix: np.ndarray,
    box_variances: np.ndarray,
    class_index_array: np.ndarray,
    num_classes: int,
    match_iou: float = 0.5,
    ignore_iou: float = 0.4,
) -> np.ndarray:
    """
    Computes the np.array which is used as a target for the net training

    Args:
        anchor_boxes: n x 4 array with anchors in ullr format
        gt_boxes: m x 4 array with gt boxes in ullr format
        iou_matrix: n x m matrix with corresponding iou values
        box_variances: array with 4 values for scaling
        class_index_array: array with length m with gt class indices
        num_classes: number of classes as int
        match_iou: float value between zero and one to define when
            two bounding boxes are matching
        ignore_iou: bounding boxes with an iou between ignore_iou and match_iou are ignored

    Returns:
        Returns a vector with length 4 + 1 + num_classes.
        The first four digits are the encoded bounding box coordinates,
        then comes the mask value (POSITIVE,NEGATIVE,IGNORE) and finally
        a target class list representing the corresponding class label of the bounding box.

    """
    anchor_gt_indexes = np.argmax(iou_matrix, axis=1)
    iou_maxes = np.max(iou_matrix, axis=1)

    mask_array = np.zeros((anchor_boxes.shape[0],))
    positive_targets = iou_maxes >= match_iou
    negative_targets = iou_maxes <= ignore_iou

    ignore_targets = np.logical_not(np.logical_or(positive_targets, negative_targets))
    mask_array[positive_targets] = POSITIVE_MASK_VALUE
    mask_array[negative_targets] = NEGATIVE_MASK_VALUE
    mask_array[ignore_targets] = IGNORE_MASK_VALUE

    target_class_array = class_index_array[anchor_gt_indexes]
    # to one hot encoding
    target_class_array = np.eye(num_classes)[target_class_array, :]
    target_class_array[negative_targets, :] = 0.0
    target_class_array[ignore_targets, :] = 0.0

    anchor_boxes_xywh = convert_to_xywh(anchor_boxes)
    gt_boxes_xywh = convert_to_xywh(gt_boxes)
    anchor_gt_targets = gt_boxes_xywh[anchor_gt_indexes, :]
    encoded_boxes = encode_boxes(anchor_boxes_xywh, anchor_gt_targets, box_variances)
    return np.concatenate(
        (encoded_boxes, mask_array[:, np.newaxis], target_class_array), axis=1
    )


def shift_bbox_by_percentage(
    bbox_coords: Tuple[float, float, float, float],
    percentage: float,
    axis: Union[List[int], int],
    direction: Union[List[int], int],
):
    """
    Shifts a bounding box to a direction by a given percentage of the bounding box
    Args:
        bbox_coords: Bounding box coordinates to be shifted
        percentage: Percentage of the bounding box to shift by
        axis: Perform shift on y-axis [0], on x-axis [1] or on both [0,1]
        direction: Shift direction;

            UP if direction == 0 and axis == 0;
            DOWN if direction == 1 and axis == 0;
            LEFT if direction == 0 and axis == 1;
            RIGHT if direction == 1 and axis == 1;

            If axis is a list (0,1) the direction has to be a list too.
            In this case the first position of the direction list is on x
            and the second position is the shift at y.

    Returns:
        Shifted bounding box
    """
    shifted_bbox = BoundingBox(*bbox_coords)
    if isinstance(axis, int):
        if isinstance(direction, list):
            raise ValueError(
                f"If only a single axis is passed ({axis}), the direction has to be an int too."
            )
        if axis == 0:
            shifted_bbox = shift_y_axis(
                bbox=shifted_bbox, direction=direction, percentage=percentage
            )
        else:
            shifted_bbox = shift_x_axis(
                bbox=shifted_bbox, direction=direction, percentage=percentage
            )
    else:
        shifted_bbox = shift_y_axis(
            bbox=shifted_bbox, direction=direction[0], percentage=percentage
        )
        shifted_bbox = shift_x_axis(
            bbox=shifted_bbox, direction=direction[1], percentage=percentage
        )
    return shifted_bbox


def shift_y_axis(bbox: BoundingBox, direction: int, percentage: float) -> BoundingBox:
    """
    Shifts a bounding box on the y-axis in a specified direction by percentage of that bounding box.

    Args:
        bbox: bounding box to be shifted
        direction: the direction of the shift (0 = left, 1 = right)
        percentage: Percentage of the bounding box to shift by

    Returns:
        Shifted bounding box
    """

    if direction == 0:
        bbox.y_pos = int(bbox.y_pos * (1 - percentage))
    else:
        bbox.y_pos = int(bbox.y_pos * (1 + percentage))

    return bbox


def shift_x_axis(bbox: BoundingBox, direction: int, percentage: float) -> BoundingBox:
    """
    Shifts a bounding box on x-axis in a specified direction by percentage of that bounding box.

    Args:
        bbox: bounding box to be shifted
        direction: the direction of the shift (0 = up, 1 = down)
        percentage: Percentage of the bounding box to shift by

    Returns:
        Shifted bounding box
    """

    if direction == 0:
        bbox.x_pos = int(bbox.x_pos * (1 - percentage))
    else:
        bbox.x_pos = int(bbox.x_pos * (1 + percentage))
    return bbox


def bounding_box_from_absolute_cxcywh(
    cx_pixel: float,
    cy_pixel: float,
    width_pixel: float,
    height_pixel: float,
) -> BoundingBox:
    """Returns a bounding box from absolute center coordinates [x,y,width,height] in pixels"""
    left = cx_pixel - width_pixel / 2
    top = cy_pixel - height_pixel / 2
    return BoundingBox(left, top, width_pixel, height_pixel)


def to_relative_bbox_values(
    values: Tuple[int, int, int, int], img_size: ImageSize
) -> Tuple[float, float, float, float]:
    """Converts absolute image coordinates to relative image coordinates based on image size"""
    img_size_list = [img_size.width, img_size.height]

    # noinspection PyTypeChecker
    return tuple(
        float(value / img_size_list[idx % 2])
        for value, idx in zip(
            values,
            range(4),
        )
    )


def dict_to_bounding_box(data) -> Union[BoundingBox, None]:
    """Creates an BoundingBox from a dict"""
    if data is None:
        return None
    return data if isinstance(data, BoundingBox) else BoundingBox(**data)
