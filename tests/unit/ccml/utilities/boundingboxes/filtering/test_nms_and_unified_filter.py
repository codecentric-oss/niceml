import numpy as np
import pytest

from niceml.data.datadescriptions.objdetdatadescription import ObjDetDataDescription
from niceml.utilities.boundingboxes.bboxconversion import (
    bbox_list_to_ullr_array,
    convert_to_xywh,
)
from niceml.utilities.boundingboxes.boundingbox import BoundingBox, split_bounding_boxes
from niceml.utilities.boundingboxes.filtering.nmsfilter import NmsFilter
from niceml.utilities.boundingboxes.filtering.predictionfilter import PredictionFilter
from niceml.utilities.boundingboxes.filtering.unifiedboxfilter import UnifiedBoxFilter
from niceml.utilities.imagesize import ImageSize

SCORE_THRESHOLD = 0.25


@pytest.mark.parametrize(
    "prediction_filter",
    [
        UnifiedBoxFilter(score_threshold=SCORE_THRESHOLD, iou_threshold=0.05),
        NmsFilter(score_threshold=SCORE_THRESHOLD, iou_threshold=0.3),
    ],
)
def test_nms_and_unifiedfilter(prediction_filter: PredictionFilter):
    score_thres = SCORE_THRESHOLD
    rng = np.random.default_rng(seed=123)
    classes = ["0", "1"]
    img_size = ImageSize(100, 100)
    data_description = ObjDetDataDescription(
        featuremap_scales=[8, 16, 32, 64, 128],
        classes=classes,
        input_image_size=img_size,
        anchor_aspect_ratios=[1, 0.5, 2.0],
        anchor_scales=[1, 1.25, 1.6],
        anchor_base_area_side=4,
        box_variance=[1.0, 1.0, 2.0, 2.0],
    )

    prediction_filter.initialize(data_description)

    class_count = 2
    surrounding_box: BoundingBox = BoundingBox(0, 0, 100, 100)

    bbox_list_1 = split_bounding_boxes(surrounding_box, 10, 10)
    pred_1_array = np.zeros((10 * 10, class_count))
    for cur_pred_idx in range(pred_1_array.shape[0]):
        rnd_num = (rng.random() / 2) + 0.5
        assert rnd_num > score_thres
        pred_1_array[cur_pred_idx, cur_pred_idx % 2] = rnd_num

    bbox_list_2 = split_bounding_boxes(surrounding_box, 10, 20)
    pred_2_array = np.zeros((20 * 10, class_count))
    for cur_pred_idx in range(pred_2_array.shape[0]):
        pred_2_array[cur_pred_idx, (cur_pred_idx // 2) % 2] = rng.random() / 2

    bbox_array_1 = convert_to_xywh(bbox_list_to_ullr_array(bbox_list_1))
    bbox_array_2 = convert_to_xywh(bbox_list_to_ullr_array(bbox_list_2))

    pred_1_array = np.concatenate([bbox_array_1, pred_1_array], axis=1)
    pred_2_array = np.concatenate([bbox_array_2, pred_2_array], axis=1)

    pred_array = np.concatenate([pred_1_array, pred_2_array], axis=0)
    pred_array = np.concatenate(
        [pred_array, np.arange(pred_array.shape[0])[:, np.newaxis]], axis=1
    )

    filtered_array = prediction_filter.filter(pred_array)

    assert np.min(filtered_array[:, 2:4]) == 10.0
    assert filtered_array.shape[1] == 7
    assert filtered_array.shape[0] == 100
