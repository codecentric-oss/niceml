"""Module for iou matrix computation functions"""
from math import sqrt
from typing import List, Union

import numpy as np
from scipy.sparse import csr_matrix

from niceml.utilities.boundingboxes.bboxconversion import bbox_list_to_ullr_array
from niceml.utilities.boundingboxes.boundingbox import (
    BoundingBox,
    get_surrounding_bounding_box,
    split_bounding_boxes,
)


def get_splitbox_count(element_count: int) -> int:
    """
    Returns the number of boxes to split one box into, where the number is at least 2,
    but not more than 8

    Args:
        element_count: Determine the number of elements in a box
    Returns:
        The number of boxes to split into
    """
    target = int(sqrt(element_count) / 300)
    return max(2, min(8, target))


def compute_iou_matrix_optimized(  # pylint: disable=too-many-locals  # QUEST: replace compute_iou_matrix?
    anchor_boxes: np.ndarray, gt_boxes: np.ndarray
) -> Union[csr_matrix, np.ndarray]:
    """
    Computes pairwise IOU matrix for two given sets of boxes.
    Computes the same iou matrix as `compute_iou_matrix` but especially
    for big matrices this function more efficient and user fewer memory.

    Args:
        anchor_boxes: A tensor with shape `(N, 4)` representing anchor bounding boxes
            where each box is of the format `[left, top, right, bottom]`.
        gt_boxes: A tensor with shape `(M, 4)` representing ground truth bounding boxes
            where each box is of the format `[left, top, right, bottom]`.

    Returns:
        pairwise IOU matrix with shape `(N, M)`, where the value at 'i'th row
        'j'th column holds the IOU between 'i'th box and 'j'th box from
        boxes1 and boxes2 respectively.
    """
    element_count = anchor_boxes.shape[0] * gt_boxes.shape[0]
    if element_count < 100000:
        return compute_iou_matrix(anchor_boxes, gt_boxes)

    surrounding_bbox = get_surrounding_bounding_box(anchor_boxes, gt_boxes)
    box_split_count = get_splitbox_count(element_count)
    bounding_box_split_list: List[BoundingBox] = split_bounding_boxes(
        surrounding_bbox, box_split_count, box_split_count
    )
    bounding_box_split_array = bbox_list_to_ullr_array(bounding_box_split_list)

    anchor_boxes_iou = compute_iou_matrix(anchor_boxes, bounding_box_split_array)
    gt_boxes_iou = compute_iou_matrix(gt_boxes, bounding_box_split_array)
    anchor_indexes = np.argwhere(anchor_boxes_iou > 0)
    gt_indexes = np.argwhere(gt_boxes_iou > 0)

    value_list = []

    for idx in range(len(bounding_box_split_list)):
        cur_anchor_indexes = anchor_indexes[anchor_indexes[:, 1] == idx, 0]
        cur_gt_indexes = gt_indexes[gt_indexes[:, 1] == idx, 0]
        cur_iou_mat = compute_iou_matrix(
            anchor_boxes[cur_anchor_indexes, :], gt_boxes[cur_gt_indexes, :]
        )
        cur_iou_indexes = np.argwhere(cur_iou_mat > 0)
        target_iou_values = cur_iou_mat[cur_iou_indexes[:, 0], cur_iou_indexes[:, 1]]
        target_anchor_indexes = cur_anchor_indexes[cur_iou_indexes[:, 0]]
        target_gt_indexes = cur_gt_indexes[cur_iou_indexes[:, 1]]

        value_list.append(
            np.concatenate(
                [
                    target_iou_values[np.newaxis, :],
                    target_anchor_indexes[np.newaxis, :],
                    target_gt_indexes[np.newaxis, :],
                ],
                axis=0,
            )
        )

    value_array = np.concatenate(value_list, axis=1)

    value_array = np.unique(value_array, axis=1)

    return csr_matrix(
        (value_array[0, :], (value_array[1, :], value_array[2, :])),
        shape=(anchor_boxes.shape[0], gt_boxes.shape[0]),
    )


# pylint: disable=too-many-locals
def compute_iou_matrix(anchor_boxes: np.ndarray, gt_boxes: np.ndarray) -> np.ndarray:
    """Computes pairwise IOU matrix for two given sets of boxes

    Args:
        anchor_boxes: A tensor with shape `(N, 4)` representing anchor bounding boxes
            where each box is of the format `[left, top, right, bottom]`.
        gt_boxes: A tensor with shape `(M, 4)` representing ground truth bounding boxes
            where each box is of the format `[left, top, right, bottom]`.

    Returns:
        pairwise IOU matrix with shape `(N, M)`, where the value at 'i'th row
        'j'th column holds the IOU between 'i'th box and 'j'th box from
        boxes1 and boxes2 respectively.
    """

    anchor_lefts = anchor_boxes[:, 0][:, np.newaxis]
    anchor_tops = anchor_boxes[:, 1][:, np.newaxis]
    anchor_rights = anchor_boxes[:, 2][:, np.newaxis]
    anchor_bottoms = anchor_boxes[:, 3][:, np.newaxis]

    anchor_areas = (anchor_rights - anchor_lefts) * (anchor_bottoms - anchor_tops)

    gt_lefts = gt_boxes[:, 0][np.newaxis, :]
    gt_tops = gt_boxes[:, 1][np.newaxis, :]
    gt_rights = gt_boxes[:, 2][np.newaxis, :]
    gt_bottoms = gt_boxes[:, 3][np.newaxis, :]

    gt_areas = (gt_rights - gt_lefts) * (gt_bottoms - gt_tops)

    intersect_lefts = np.maximum(anchor_lefts, gt_lefts)
    intersect_tops = np.maximum(anchor_tops, gt_tops)
    intersect_rights = np.minimum(anchor_rights, gt_rights)
    intersect_bottoms = np.minimum(anchor_bottoms, gt_bottoms)

    intersection_widths = np.maximum(0.0, intersect_rights - intersect_lefts)
    intersection_heights = np.maximum(0.0, intersect_bottoms - intersect_tops)

    intersection_areas = intersection_widths * intersection_heights

    union_areas = anchor_areas + gt_areas - intersection_areas
    intersection_areas = intersection_areas.astype(float)
    union_areas = union_areas.astype(float)
    iou_matrix = np.divide(
        intersection_areas,
        union_areas,
        out=np.zeros(shape=intersection_areas.shape, dtype=float),
        where=union_areas != 0.0,
    )
    return iou_matrix
