import numpy as np
import pytest

from niceml.utilities.boundingboxes.filtering.nmsfilter import non_maximum_suppression


@pytest.mark.parametrize(
    "box_predictions,iou_threshold",
    [
        (
            np.array(
                [
                    np.array(
                        [
                            0.423828125,
                            0.5927734375,
                            0.478515625,
                            0.6416015625,
                            0.36,
                            0.89,
                        ]
                    ),
                    np.array(
                        [0.413828125, 0.5827734375, 0.468515625, 0.6316015625, 0.2, 0.7]
                    ),
                    np.array(
                        [
                            0.433828125,
                            0.6027734375,
                            0.488515625,
                            0.6516015625,
                            0.29,
                            0.8,
                        ]
                    ),
                    np.array(
                        [0.404296875, 0.615234375, 0.44921875, 0.6455078125, 0.88, 0.35]
                    ),
                    np.array(
                        [0.394296875, 0.605234375, 0.43921875, 0.6355078125, 0.8, 0.29]
                    ),
                    np.array(
                        [0.414296875, 0.625234375, 0.45921875, 0.6555078125, 0.82, 0.27]
                    ),
                    np.array(
                        [0.556640625, 0.39453125, 0.61328125, 0.42578125, 0.91, 0.02]
                    ),
                    np.array(
                        [0.546640625, 0.38453125, 0.60328125, 0.41578125, 0.90, 0.03]
                    ),
                    np.array(
                        [0.566640625, 0.40453125, 0.62328125, 0.43578125, 0.89, 0.04]
                    ),
                ]
            ),
            0.3,
        )
    ],
)
def test_non_maximum_suppression(box_predictions, iou_threshold):
    coordinates_count = 4

    filtered_bbox = non_maximum_suppression(
        prediction_array_xywh=box_predictions,
        iou_threshold=iou_threshold,
        coordinates_count=coordinates_count,
        class_count=2,
    )

    best_bboxes = box_predictions[[0, 3, 6, 7, 8]]
    for bbox in filtered_bbox:
        assert bbox in best_bboxes
