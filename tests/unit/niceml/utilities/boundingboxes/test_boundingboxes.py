from math import isclose
from typing import List, Optional

import pytest

from niceml.utilities.boundingboxes.bboxconversion import bbox_list_to_ullr_array
from niceml.utilities.boundingboxes.boundingbox import (
    BoundingBox,
    get_bounding_box_attributes,
    get_surrounding_bounding_box,
    split_bounding_boxes,
)


@pytest.mark.parametrize(
    "bbox1,bbox2,do_intersect",
    [
        ((0, 0, 10, 10), (5, 5, 20, 20), True),
        ((0, 0, 10, 10), (15, 5, 20, 20), False),
        ((0, 0, 10, 10), (5, 15, 20, 20), False),
    ],
)
def test_do_bboxes_intersect(bbox1: tuple, bbox2: tuple, do_intersect: bool):
    bounding_box_1 = BoundingBox(*bbox1)
    bounding_box_2 = BoundingBox(*bbox2)
    assert bounding_box_1.do_intersect(bounding_box_2) == do_intersect


@pytest.mark.parametrize(
    "bbox1,bbox2,intersect_box",
    [
        ((0, 0, 0.1, 0.1), (0.05, 0.03, 0.2, 0.2), (0.05, 0.03, 0.05, 0.07)),
        ((0, 0, 0.1, 0.1), (0.15, 0.05, 0.2, 0.2), None),
        ((0, 0, 0.1, 0.1), (0.05, 0.15, 0.2, 0.2), None),
        ((0.5, 0.5, 0.2, 0.3), (0.5, 0.5, 0.2, 0.3), (0.5, 0.5, 0.2, 0.3)),
    ],
)
def test_cal_bboxes_intersect(
    bbox1: tuple, bbox2: tuple, intersect_box: Optional[tuple]
):
    bounding_box_1 = BoundingBox(*bbox1)
    bounding_box_2 = BoundingBox(*bbox2)

    pred_intersect_box = bounding_box_1.get_intersection(bounding_box_2)
    if intersect_box is None:
        assert pred_intersect_box is None
    else:
        assert BoundingBox(*intersect_box) == pred_intersect_box


@pytest.mark.parametrize(
    "bbox1,bbox2,iou_value",
    [
        ((0, 0, 10, 10), (5, 5, 5, 5), 0.25),
        ((0, 0, 20, 20), (10, 0.0, 30, 20), 0.25),
        ((0, 0, 10, 10), (15, 5, 20, 20), 0.0),
        ((0, 0, 10, 10), (5, 15, 20, 20), 0.0),
        ((50, 50, 20, 30), (50, 50, 20, 30), 1.0),
    ],
)
def test_cal_iou(bbox1: tuple, bbox2: tuple, iou_value: float):
    bounding_box_1 = BoundingBox(*bbox1)
    bounding_box_2 = BoundingBox(*bbox2)
    assert isclose(bounding_box_1.calc_iou(bounding_box_2), iou_value)


@pytest.mark.parametrize(
    "bbox,x_boxes,y_boxes",
    [(BoundingBox(0, 0, 100, 100), 10, 10), (BoundingBox(50, 25, 250, 125), 5, 10)],
)
def test_split_boundingboxes(bbox: BoundingBox, x_boxes: int, y_boxes: int):
    bbox_list = split_bounding_boxes(bbox, x_boxes, y_boxes)

    assert sum((x.get_absolute_area() for x in bbox_list)) == bbox.get_absolute_area()
    assert all((bbox.do_intersect(x) for x in bbox_list))
    assert all((isclose(bbox.width / x_boxes, x.width) for x in bbox_list))
    assert all((isclose(bbox.height / y_boxes, x.height) for x in bbox_list))


@pytest.mark.parametrize(
    "bbox,x_boxes,y_boxes",
    [(BoundingBox(0, 0, 100, 100), 10, 10), (BoundingBox(50, 25, 250, 125), 5, 10)],
)
def test_get_surrounding_boundingbox(bbox: BoundingBox, x_boxes: int, y_boxes: int):
    bbox_list = split_bounding_boxes(bbox, x_boxes, y_boxes)
    bbox_array = bbox_list_to_ullr_array(bbox_list)
    surrounding_bbox = get_surrounding_bounding_box(bbox_array)
    assert bbox == surrounding_bbox
    surrounding_bbox = get_surrounding_bounding_box(bbox_array, bbox_array)
    assert bbox == surrounding_bbox


@pytest.mark.parametrize(
    "bounding_box,results",
    [(BoundingBox(0, 0, 0, 0), ["x_pos", "y_pos", "width", "height"])],
)
def test_get_bounding_box_attributes(bounding_box: BoundingBox, results: List[str]):
    bbox_attributes = get_bounding_box_attributes()

    assert bbox_attributes == results


@pytest.mark.parametrize(
    "bounding_box,axis,direction,shift_by,result_bounding_box",
    [
        (BoundingBox(0, 0, 0, 0), 0, 1, 10, BoundingBox(10, 0, 0, 0)),
        (BoundingBox(10, 0, 0, 0), 0, 0, 10, BoundingBox(0, 0, 0, 0)),
        (BoundingBox(10, 10, 0, 0), 1, 0, 10, BoundingBox(10, 0, 0, 0)),
        (BoundingBox(0, 0, 0, 0), 1, 1, 10, BoundingBox(0, 10, 0, 0)),
    ],
)
def test_shift(
    bounding_box: BoundingBox,
    axis: int,
    direction: int,
    shift_by: int,
    result_bounding_box: BoundingBox,
):
    bounding_box.shift(axis=axis, direction=direction, shift_by=shift_by)

    assert bounding_box == result_bounding_box


@pytest.mark.parametrize(
    "bounding_box,scale,result_bounding_box",
    [
        (BoundingBox(10, 10, 5, 5), 0.5, BoundingBox(5, 5, 2, 2)),
        (BoundingBox(10, 10, 5, 5), 1.5, BoundingBox(15, 15, 8, 8)),
    ],
)
def test_scale(
    bounding_box: BoundingBox, scale: float, result_bounding_box: BoundingBox
):
    scaled_bbox = bounding_box.scale(scale)

    assert scaled_bbox == result_bounding_box
