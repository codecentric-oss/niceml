"""Module for functions regarding bounding box encoding"""
import numpy as np


def encode_boxes(
    anchor_boxes_xywh: np.ndarray, gt_boxes_xywh: np.ndarray, box_variances: np.ndarray
) -> np.ndarray:

    """
    Encodes the anchor boxes to a numpy array

    Args:
        anchor_boxes_xywh: Anchor boxes in x,y,width,height format
        gt_boxes_xywh: Ground truth boxes in x,y,width,height format
        box_variances: Box variance to scale by

    Returns:
        A scaled and encoded box as a numpy array of shape (num_anchors, 4)
    """
    enc0 = (gt_boxes_xywh[:, 0] - anchor_boxes_xywh[:, 0]) / anchor_boxes_xywh[:, 2]
    enc1 = (gt_boxes_xywh[:, 1] - anchor_boxes_xywh[:, 1]) / anchor_boxes_xywh[:, 3]
    enc2 = np.where(
        gt_boxes_xywh[:, 2] / anchor_boxes_xywh[:, 2] > 0,
        np.log(gt_boxes_xywh[:, 2] / anchor_boxes_xywh[:, 2]),
        0,
    )
    enc3 = np.where(
        gt_boxes_xywh[:, 3] / anchor_boxes_xywh[:, 3] > 0,
        np.log(gt_boxes_xywh[:, 3] / anchor_boxes_xywh[:, 3]),
        0,
    )
    encoded_array = np.concatenate(
        (
            enc0[:, np.newaxis],
            enc1[:, np.newaxis],
            enc2[:, np.newaxis],
            enc3[:, np.newaxis],
        ),
        axis=1,
    )
    encoded_array = encoded_array / box_variances

    return encoded_array


def decode_boxes(
    anchor_boxes_xywh: np.ndarray,
    encoded_array_xywh: np.ndarray,
    box_variances: np.ndarray,
) -> np.ndarray:

    """
    Decodes the incoming array to target boxes

    Args:
        anchor_boxes_xywh: Anchor boxes in x,y,width,height format
        encoded_array_xywh: Encoded boxes in x,y,width,height format
        box_variances: Box variance to scale by

    Returns:
        The decoded boxes x,y,width,height format
    """
    x_pos = (
        encoded_array_xywh[:, 0] * box_variances[0] * anchor_boxes_xywh[:, 2]
    ) + anchor_boxes_xywh[:, 0]
    y_pos = (
        encoded_array_xywh[:, 1] * box_variances[1] * anchor_boxes_xywh[:, 3]
    ) + anchor_boxes_xywh[:, 1]
    width = (
        np.exp(encoded_array_xywh[:, 2] * box_variances[2]) * anchor_boxes_xywh[:, 2]
    )
    height = (
        np.exp(encoded_array_xywh[:, 3] * box_variances[3]) * anchor_boxes_xywh[:, 3]
    )

    return np.concatenate(
        (
            x_pos[:, np.newaxis],
            y_pos[:, np.newaxis],
            width[:, np.newaxis],
            height[:, np.newaxis],
        ),
        axis=1,
    )
