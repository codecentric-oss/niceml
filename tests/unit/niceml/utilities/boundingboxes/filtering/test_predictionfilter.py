from typing import Type

import pytest

from niceml.utilities.boundingboxes.filtering.nmsfilter import NmsFilter
from niceml.utilities.boundingboxes.filtering.predictionfilter import (
    PredictionFilter,
    get_filter_attributes,
)
from niceml.utilities.boundingboxes.filtering.thresholdfilter import ThresholdFilter
from niceml.utilities.boundingboxes.filtering.unifiedboxfilter import UnifiedBoxFilter


@pytest.mark.parametrize(
    "filter_class,target_dict",
    [
        (
            ThresholdFilter,
            [
                {"name": "score_threshold", "default": 0.5, "step": None},
                {"name": "max_output_count", "default": 200, "step": 1},
            ],
        ),
        (
            NmsFilter,
            [
                {"name": "score_threshold", "default": 0.5, "step": None},
                {"name": "iou_threshold", "default": 0.5, "step": None},
            ],
        ),
        (
            UnifiedBoxFilter,
            [
                {"name": "score_threshold", "default": 0.5, "step": None},
                {"name": "iou_threshold", "default": 0.5, "step": None},
            ],
        ),
    ],
)
def test_get_filter_attributes(filter_class: Type[PredictionFilter], target_dict: dict):
    ignore_attributes = ["coordinates_count", "output_class_count", "box_coordinates"]

    filter_attributes = get_filter_attributes(
        filter_class=filter_class, ignore_attributes=ignore_attributes
    )
    for filter_attribute in filter_attributes:
        assert filter_attribute in target_dict
