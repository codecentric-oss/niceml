import numpy as np

from niceml.data.datadescriptions.objdetdatadescription import ObjDetDataDescription
from niceml.utilities.boundingboxes.filtering.thresholdfilter import ThresholdFilter
from niceml.utilities.imagesize import ImageSize


def test_thresholdfilter():
    th_filter = ThresholdFilter(score_threshold=0.5)
    classes = ["0", "1", "2"]
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
    th_filter.initialize(data_description)
    pred_mat_list = [
        [0, 0, 0, 0, 0.5, 0.2, 0.3],
        [1, 1, 1, 1, 0.2, 0.2, 0.2],
        [2, 2, 2, 2, 0.3, 0.3, 0.6],
    ]
    pred_mat = np.array(pred_mat_list)
    filtered_mat = th_filter.filter(pred_mat)
    assert filtered_mat.shape == (2, 7)


def test_thresholdfilter_with_max_count():
    th_filter = ThresholdFilter(score_threshold=0.5, max_output_count=3)
    classes = ["0", "1", "2"]
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
    th_filter.initialize(data_description)
    pred_mat_list = [
        [0, 0, 0, 0, 0.7, 0.2, 0.3],
        [1, 1, 1, 1, 0.2, 0.2, 0.2],
        [2, 2, 2, 2, 0.3, 0.3, 0.6],
        [3, 3, 3, 3, 0.3, 0.3, 0.6],
        [4, 4, 4, 4, 0.7, 0.3, 0.25],
        [5, 5, 5, 5, 0.1, 0.1, 0.8],
    ]
    pred_mat = np.array(pred_mat_list)
    filtered_mat = th_filter.filter(pred_mat)
    assert filtered_mat.shape == (3, 7)
    assert np.min(np.max(filtered_mat[:, 4:], axis=1)) >= 0.7
