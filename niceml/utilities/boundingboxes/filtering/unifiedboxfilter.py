"""Module for UnifiedBoxFilter"""  # QUEST: still used?
from typing import List

import numpy as np
from attrs import define

from niceml.utilities.boundingboxes.bboxconversion import convert_to_ullr, convert_to_xywh
from niceml.utilities.boundingboxes.filtering.predictionfilter import PredictionFilter
from niceml.utilities.ioumatrix import compute_iou_matrix


# pylint:disable = duplicate-code
@define
class UnifiedBoxFilter(PredictionFilter):
    """Combines overlapping bounding boxes with the same class to
    one unified box with combined border coordinates."""

    score_threshold: float = 0.5
    iou_threshold: float = 0.5
    box_coordinates: int = 4

    def filter(  # pylint: disable=too-many-locals
        self, prediction_array_xywh: np.ndarray
    ) -> np.ndarray:
        """
        Filters bounding boxes of prediction array according to given filter conditions
        Args:
            prediction_array_xywh: prediction array in format [y,x,width,height]

        Returns:
            filtered prediction array
        """
        prediction_array_ullr = convert_to_ullr(prediction_array_xywh)

        max_class_array = np.argmax(
            prediction_array_ullr[
                :, self.box_coordinates : self.box_coordinates + self.output_class_count
            ],
            axis=1,
        )
        max_score = np.max(
            prediction_array_ullr[
                :, self.box_coordinates : self.box_coordinates + self.output_class_count
            ],
            axis=1,
        )

        prediction_array_ullr = prediction_array_ullr[
            max_score > self.score_threshold, :
        ]
        max_class_array = max_class_array[max_score > self.score_threshold]
        max_score = max_score[max_score > self.score_threshold]

        sorted_scores_idxes = max_score.argsort()[::-1]
        prediction_array_ullr = prediction_array_ullr[sorted_scores_idxes]
        max_class_array = max_class_array[sorted_scores_idxes]

        out_bboxes: List[np.ndarray] = []
        for cur_class in range(self.output_class_count):
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

                cur_cluster_idxes = np.argwhere(
                    iou_mat[cur_row_idx, :] > self.iou_threshold
                )[:, 0].tolist()
                used_box_idxes.update(cur_cluster_idxes)

                cur_cluster_prediction_array = class_prediction_array_ullr[
                    cur_cluster_idxes, :
                ]

                ul_corners = np.min(cur_cluster_prediction_array[:, :2], axis=0)
                lr_corners = np.max(cur_cluster_prediction_array[:, 2:4], axis=0)
                predictions = np.max(
                    cur_cluster_prediction_array[
                        :,
                        self.box_coordinates : self.box_coordinates
                        + self.output_class_count,
                    ],
                    axis=0,
                )
                additional_info = class_prediction_array_ullr[
                    cur_row_idx, self.box_coordinates + self.output_class_count :
                ]
                cur_cluster_bbox = np.concatenate(
                    [ul_corners, lr_corners, predictions, additional_info]
                )
                out_bboxes.append(cur_cluster_bbox[np.newaxis, :])
        if len(out_bboxes) == 0:
            return np.empty(shape=(0, prediction_array_ullr.shape[1]))
        out_bbox_array_ullr = np.concatenate(out_bboxes, axis=0)
        return convert_to_xywh(out_bbox_array_ullr)
