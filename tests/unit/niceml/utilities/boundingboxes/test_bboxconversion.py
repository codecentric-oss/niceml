from typing import List, Tuple, Union

import numpy as np
import pytest
from numpy.testing import assert_almost_equal

from niceml.utilities.boundingboxes.bboxconversion import (
    bounding_box_from_absolute_cxcywh,
    convert_to_ullr,
    convert_to_xywh,
    shift_bbox_by_percentage,
    to_relative_bbox_values,
)
from niceml.utilities.boundingboxes.boundingbox import BoundingBox
from niceml.utilities.imagesize import ImageSize


@pytest.mark.parametrize(
    "input_coordinates,target_coordinates,image_size",
    [
        (
            (108, 108, 148, 148),
            (0.421875, 0.421875, 0.578125, 0.578125),
            ImageSize(256, 256),
        ),
        (
            (108, 108, 148, 148),
            (0.36, 0.421875, 0.49333333333333335, 0.578125),
            ImageSize(300, 256),
        ),
        (
            (108, 108, 148, 148),
            (0.421875, 0.36, 0.578125, 0.49333333333333335),
            ImageSize(256, 300),
        ),
    ],
)
def test_to_relative_bbox_values(
    input_coordinates: tuple, target_coordinates: tuple, image_size: ImageSize
):
    bounding_box_values = to_relative_bbox_values(
        input_coordinates, img_size=image_size
    )

    assert bounding_box_values == target_coordinates


@pytest.mark.parametrize(
    "bbox_val,percentage,axis,direction,target_pos",
    [
        ((100, 100, 30, 30), 0.2, 0, 0, (100, 80)),
        ((100, 100, 30, 30), 0.2, 0, 1, (100, 120)),
        ((100, 100, 30, 30), 0.2, 1, 0, (80.00, 100.00)),
        ((100, 100, 30, 30), 0.2, 1, 1, (120.00, 100.00)),
        ((100, 100, 30, 30), 0.2, [0, 1], [0, 0], (80.00, 80.00)),
        ((100, 100, 30, 30), 0.2, [0, 1], [0, 1], (120.00, 80.00)),
        ((100, 100, 30, 30), 0.2, [0, 1], [1, 0], (80.00, 120.00)),
        ((100, 100, 30, 30), 0.2, [0, 1], [1, 1], (120.00, 120.00)),
    ],
)
def test_shift_bbox_by_percentage(
    bbox_val: Tuple[float, float, float, float],
    percentage: float,
    axis: Union[List[int], int],
    direction: Union[List[int], int],
    target_pos: Tuple[int],
):
    shifted_bbox = shift_bbox_by_percentage(
        bbox_coords=bbox_val, percentage=percentage, axis=axis, direction=direction
    )

    assert shifted_bbox.x_pos == target_pos[0]
    assert shifted_bbox.y_pos == target_pos[1]


@pytest.mark.parametrize(
    "target_coordinates,input_coordinates,image_size",
    [
        (
            (0.421875, 0.421875, 0.5, 0.5),
            (108, 108, 128, 128),
            ImageSize(256, 256),
        ),
        ((0.36, 0.421875, 0.3, 0.25), (108, 108, 90, 64), ImageSize(300, 256)),
    ],
)
def test_bounding_box_to_absolute_ullr(
    target_coordinates: tuple, input_coordinates: tuple, image_size: ImageSize
):
    input_bounding_box = BoundingBox(*input_coordinates)

    pred_target_coordinates = input_bounding_box.get_relative_xywh(img_size=image_size)

    assert pred_target_coordinates == target_coordinates


@pytest.mark.parametrize(
    "target_coordinates,input_coordinates,image_size",
    [
        (
            (0.421875, 0.421875, 0.15625, 0.15625),
            (108, 108, 40, 40),
            ImageSize(256, 256),
        ),
        ((0.36, 0.421875, 0.3, 0.15625), (108, 108, 90, 40), ImageSize(300, 256)),
        ((0.421875, 0.36, 0.15625, 0.3), (108, 108, 40, 90), ImageSize(256, 300)),
    ],
)
def test_bounding_box_to_absolute_xywh(
    target_coordinates: tuple, input_coordinates: tuple, image_size: ImageSize
):
    input_bounding_box = BoundingBox(*input_coordinates)

    pred_target_coordinates = input_bounding_box.get_relative_xywh(image_size)

    assert pred_target_coordinates == target_coordinates


@pytest.mark.parametrize(
    "bbox_coords,target_coords",
    [
        ((100, 330, 50, 60), (75, 300, 50, 60)),
        ((100, 100, 50, 50), (75, 75, 50, 50)),
    ],
)
def test_bounding_box_from_absolute_cxcywh(bbox_coords: tuple, target_coords: tuple):
    bbox: BoundingBox = bounding_box_from_absolute_cxcywh(*bbox_coords)
    assert target_coords == bbox.get_absolute_xywh()


@pytest.mark.parametrize(
    "box_coords_list",
    [
        [
            (0, 0, 10, 10),
            (150, 80, 25, 25),
            (0, 0, 20, 20),
            (10, 0.0, 30, 20),
            (50, 50, 20, 30),
            (50, 50, 20, 30),
        ]
    ],
)
def test_bbox_array_conversion(box_coords_list: List[tuple]):
    box_list = [BoundingBox(*x) for x in box_coords_list]
    box: BoundingBox
    xywh_array = np.array([box.get_absolute_xywh() for box in box_list])
    ullr_array = np.array([box.get_absolute_ullr() for box in box_list])
    converted_xywh = convert_to_xywh(ullr_array)
    assert_almost_equal(converted_xywh, xywh_array)
    converted_ullr = convert_to_ullr(converted_xywh)
    assert_almost_equal(converted_ullr, ullr_array)
