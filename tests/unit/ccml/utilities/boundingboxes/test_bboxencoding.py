import numpy as np
import pytest
from numpy.testing import assert_almost_equal

from niceml.utilities.boundingboxes.bboxencoding import decode_boxes, encode_boxes
from niceml.utilities.boundingboxes.boundingbox import BoundingBox


@pytest.mark.parametrize(
    "anchor_box_coords,gt_box_coords",
    [
        ((0, 0, 10, 10), (5, 5, 5, 5)),
        ((0, 0, 20, 20), (10, 0.0, 30, 20)),
        ((50, 50, 20, 30), (50, 50, 20, 30)),
    ],
)
def test_bbox_encode_decode(anchor_box_coords: tuple, gt_box_coords: tuple):
    anchor_box = BoundingBox(*anchor_box_coords)
    gt_box = BoundingBox(*gt_box_coords)
    box_variance = (0.1, 0.1, 0.2, 0.2)

    encoded_values = anchor_box.encode(gt_box, box_variance)
    decoded_box = anchor_box.decode(encoded_values, box_variance)

    assert decoded_box == gt_box


@pytest.mark.parametrize(
    "anchor_box_coords_list,gt_box_coords_list",
    [
        (
            [(0, 0, 10, 10), (0, 0, 20, 20), (50, 50, 20, 30)],
            [(5, 5, 5, 5), (10, 0.0, 30, 20), (50, 50, 20, 30)],
        )
    ],
)
def test_bbox_array_encode_decode(
    anchor_box_coords_list: tuple, gt_box_coords_list: tuple
):
    anchor_box_list = [
        BoundingBox(*anchor_box_coords) for anchor_box_coords in anchor_box_coords_list
    ]
    gt_box_list = [BoundingBox(*gt_box_coords) for gt_box_coords in gt_box_coords_list]
    box_variance = np.array((0.1, 0.1, 0.2, 0.2))
    box: BoundingBox
    anchor_array = np.array([box.get_absolute_xywh() for box in anchor_box_list])
    gt_box_array = np.array([box.get_absolute_xywh() for box in gt_box_list])

    encoded_array = encode_boxes(anchor_array, gt_box_array, box_variance)
    decoded_array = decode_boxes(
        anchor_array, encoded_array, box_variances=box_variance
    )

    assert_almost_equal(gt_box_array, decoded_array)
