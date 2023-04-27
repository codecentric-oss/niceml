"""Module for ThresholdFilter"""  # QUEST: still used?
from typing import Optional

import numpy as np
from attrs import define

from niceml.utilities.boundingboxes.filtering.predictionfilter import PredictionFilter


@define
class ThresholdFilter(PredictionFilter):  # pylint: disable=too-few-public-methods
    """Removes all predictions lower than score_threshold"""

    score_threshold: float = 0.5
    coordinates_count: int = 4
    max_output_count: Optional[int] = None

    def filter(self, prediction_array_xywh: np.ndarray) -> np.ndarray:
        """
        Filters the prediction in array according to given filter conditions
        Args:
            prediction_array_xywh: prediction array in format [y,x,width,height]

        Returns:
            filtered prediction array
        """
        scores = prediction_array_xywh[
            :, self.coordinates_count : self.coordinates_count + self.output_class_count
        ]
        max_vals = np.max(scores, axis=1)
        filtered_array = prediction_array_xywh[max_vals >= self.score_threshold, :]
        if (
            self.max_output_count is None
            or filtered_array.shape[0] <= self.max_output_count
        ):
            return filtered_array
        max_vals = max_vals[max_vals >= self.score_threshold]
        sorted_scores_idxes = max_vals.argsort()[::-1][: self.max_output_count]
        return filtered_array[sorted_scores_idxes, :]
