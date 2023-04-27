"""Module for NmsFilter"""
from typing import List

import numpy as np
from attrs import define

from niceml.utilities.boundingboxes.bboxconversion import convert_to_ullr, convert_to_xywh
from niceml.utilities.boundingboxes.filtering.predictionfilter import PredictionFilter
from niceml.utilities.ioumatrix import compute_iou_matrix


@define
class NmsFilter(PredictionFilter):  # pylint: disable=too-few-public-methods
    """Applies non-maximum suppression (nms) filtering to predictions"""

    iou_threshold: float = 0.5
    score_threshold: float = 0.5
    coordinates_count: int = 4

    def filter(self, prediction_array_xywh: np.ndarray) -> np.ndarray:
        return non_maximum_suppression(
            prediction_array_xywh=prediction_array_xywh,
            iou_threshold=self.iou_threshold,
            coordinates_count=self.coordinates_count,
            score_threshold=self.score_threshold,
            class_count=self.output_class_count,
        )


def non_maximum_suppression(  # pylint: disable=too-many-locals
    prediction_array_xywh: np.ndarray,
    iou_threshold: float,
    coordinates_count: int,
    class_count: int,
    score_threshold: float = 0.5,
) -> np.ndarray:
    """
    Filters the box predictions to get the most relevant boxes according to given parameters
    Args:
        prediction_array_xywh: Array of prediction boxes in format [x,y,width,height]
        iou_threshold: IOU threshold for boxes to keep
        coordinates_count: Number of coordinates in prediction array
        class_count: Number of classes in prediction array
        score_threshold: Prediction score threshold for predictions to keep

    Returns:
        Array of prediction boxes to keep
    """
    prediction_array_ullr = convert_to_ullr(prediction_array_xywh)

    max_class_array = np.argmax(
        prediction_array_ullr[:, coordinates_count : coordinates_count + class_count],
        axis=1,
    )
    max_score = np.max(
        prediction_array_ullr[:, coordinates_count : coordinates_count + class_count],
        axis=1,
    )

    prediction_array_ullr = prediction_array_ullr[max_score > score_threshold, :]
    max_class_array = max_class_array[max_score > score_threshold]
    max_score = max_score[max_score > score_threshold]

    sorted_scores_idxes = max_score.argsort()[::-1]
    prediction_array_ullr = prediction_array_ullr[sorted_scores_idxes]
    max_class_array = max_class_array[sorted_scores_idxes]

    out_bboxes: List[np.ndarray] = []
    for cur_class in range(class_count):
        cur_class_idxes = max_class_array == cur_class
        class_prediction_array_ullr = prediction_array_ullr[cur_class_idxes]

        if len(class_prediction_array_ullr) == 0:
            continue
        iou_mat = compute_iou_matrix(
            class_prediction_array_ullr, class_prediction_array_ullr
        )
        used_box_idxes = set()
        for cur_row_idx in range(iou_mat.shape[0]):
            if cur_row_idx in used_box_idxes:
                continue

            cur_cluster_idxes = np.argwhere(iou_mat[cur_row_idx, :] > iou_threshold)[
                :, 0
            ].tolist()
            used_box_idxes.update(cur_cluster_idxes)
            out_bboxes.append(
                class_prediction_array_ullr[cur_row_idx, :][np.newaxis, :]
            )

    if len(out_bboxes) == 0:
        return np.empty(shape=(0, prediction_array_ullr.shape[1]))
    out_bbox_array_ullr = np.concatenate(out_bboxes, axis=0)
    return convert_to_xywh(out_bbox_array_ullr)
