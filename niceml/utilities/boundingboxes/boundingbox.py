"""Module for BoundingBox and corresponding methods"""
from math import exp, isclose, log
from typing import List, Optional, Tuple, Union

import numpy as np
from attr import define, fields

from niceml.utilities.imagesize import ImageSize

IGNORE_MASK_VALUE = 1.0
NEGATIVE_MASK_VALUE = 2.0
POSITIVE_MASK_VALUE = 3.0


@define
class BoundingBox:
    """Class to represent a bounding box and its methods"""

    x_pos: float  # QUEST: center coordinates?
    y_pos: float
    width: float
    height: float

    def __repr__(self) -> str:
        """Returns BoundingBox parameters as string"""
        return (
            f"BBox(x:{self.x_pos:0.2f} y:{self.y_pos:0.2f} "
            f"w:{self.width:0.2f} h:{self.height:0.2f})"
        )

    def get_absolute_xywh(
        self, convert_to_int: bool = False
    ) -> Union[Tuple[float, float, float, float], Tuple[int, int, int, int]]:
        """Returns a tuple in pixel coords: (x, y, w, h) as float or int values"""
        if convert_to_int:
            return int(self.x_pos), int(self.y_pos), int(self.width), int(self.height)
        return self.x_pos, self.y_pos, self.width, self.height

    def get_absolute_ullr(
        self, convert_to_int: bool = False
    ) -> Union[Tuple[float, float, float, float], Tuple[int, int, int, int]]:
        """Returns a tuple of upper-left and lower-right coordinates (x_upper_left,
        y_upper_left, x_lower_right, y_lower_right) as float or int values"""
        if convert_to_int:
            return (
                int(self.x_pos),
                int(self.y_pos),
                int(self.x_pos + self.width),
                int(self.y_pos + self.height),
            )

        return (
            self.x_pos,
            self.y_pos,
            self.x_pos + self.width,
            self.y_pos + self.height,
        )

    def get_relative_xywh(
        self, img_size: ImageSize
    ) -> Tuple[float, float, float, float]:
        """Returns a tuple with relative coordinates (x,y,width,height)"""
        return get_scaled_values(self.get_absolute_xywh(), img_size)

    def get_relative_ullr(
        self, img_size: ImageSize
    ) -> Tuple[float, float, float, float]:
        """Returns a tuple with relative upper-left and lower-right coordinates
        (x_ul,y_ul,x_lr,y_lr)"""
        return get_scaled_values(self.get_absolute_ullr(), img_size)

    def get_absolute_area(self) -> float:
        """Returns bounding box area (= width * height)"""
        return self.width * self.height

    def get_relative_area(self, image_size: ImageSize) -> float:
        """Returns the absolute bounding box area in pixels"""
        return self.get_absolute_area() / (image_size.width * image_size.height)

    def __eq__(self, other: "BoundingBox"):
        """Checks if two BoundingBoxes are the (nearly) same"""
        if isinstance(other, BoundingBox):
            return (
                isclose(self.x_pos, other.x_pos)
                and isclose(self.y_pos, other.y_pos)
                and isclose(self.width, other.width)
                and isclose(self.height, other.height)
            )

        return False

    def do_intersect(self, other: "BoundingBox") -> bool:
        """Checks whether two bounding boxes do intersect"""
        b1_left, b1_top, b1_right, b1_bottom = self.get_absolute_ullr()
        b2_left, b2_top, b2_right, b2_bottom = other.get_absolute_ullr()
        return not (
            b2_left > b1_right
            or b2_right < b1_left
            or b2_top > b1_bottom
            or b2_bottom < b1_top
        )

    def get_intersection(self, other: "BoundingBox") -> Optional["BoundingBox"]:
        """Calculates the intersection bounding box"""
        if not self.do_intersect(other):
            return None
        b1_left, b1_top, b1_right, b1_bottom = self.get_absolute_ullr()
        b2_left, b2_top, b2_right, b2_bottom = other.get_absolute_ullr()

        intersect_left = max(b1_left, b2_left)
        intersect_top = max(b1_top, b2_top)
        intersect_bottom = min(b1_bottom, b2_bottom)
        intersect_right = min(b1_right, b2_right)

        return bounding_box_from_ullr(
            intersect_left, intersect_top, intersect_right, intersect_bottom
        )

    def calc_iou(self, other: "BoundingBox") -> float:
        """Calculates the iou between the two bounding boxes"""
        if not isinstance(other, BoundingBox):
            raise TypeError(f"other is not type BoundingBox but {type(other)}")

        try:
            inter_area: float = self.get_intersection(other).get_absolute_area()
            # Calculates the Union area by using Formula: Union(A,B) = A + B - Inter(A,B)
            union_area = (
                self.get_absolute_area() + other.get_absolute_area() - inter_area
            )
            return inter_area / union_area
        except AttributeError:
            return 0

    def encode(
        self,
        gt_bbox: "BoundingBox",
        box_variance: List[float],
    ) -> List[float]:
        """Encodes the anchor(self) with a ground truth box to net targets"""
        # QUEST: better docstring?
        if not isinstance(gt_bbox, BoundingBox):
            raise TypeError(f"other is not type BoundingBox but {type(gt_bbox)}")

        x_pos = (gt_bbox.x_pos - self.x_pos) / self.width
        y_pos = (gt_bbox.y_pos - self.y_pos) / self.height
        width = log(gt_bbox.width / self.width)
        height = log(gt_bbox.height / self.height)
        x_pos /= box_variance[0]
        y_pos /= box_variance[1]
        width /= box_variance[2]
        height /= box_variance[3]

        return [x_pos, y_pos, width, height]

    def decode(
        self,
        predicted_values: List[float],
        box_variance: List[float],
    ) -> "BoundingBox":
        """Decodes the predicted net values to a bounding box"""
        x_pos = (predicted_values[0] * box_variance[0] * self.width) + self.x_pos
        y_pos = (predicted_values[1] * box_variance[1] * self.height) + self.y_pos
        width = exp(predicted_values[2] * box_variance[2]) * self.width
        height = exp(predicted_values[3] * box_variance[3]) * self.height

        return BoundingBox(x_pos=x_pos, y_pos=y_pos, width=width, height=height)

    def shift(self, axis: int, shift_by: int, direction: int):
        """
        Shifts a bounding box on a given axis by `shift_by`

        Args:
            axis: Axis on which to be shifted (0: X-Axis, 1: Y-Axis).
            shift_by: Shift value in pixels
            direction: Direction to be shifted (0: left if axis is 0,
                up if axis is 1; 1: right if axis is 0, down if axis is 1)
        """

        if axis == 0:
            if direction == 0:
                self.x_pos -= shift_by
            else:
                self.x_pos += shift_by
        elif direction == 0:
            self.y_pos -= shift_by
        else:
            self.y_pos += shift_by

    def scale(self, scale: float) -> "BoundingBox":
        """
        Scales a bounding box (x_pos, y_pos, width, height) by a given scale factor.

        scale:
        Args:
            scale: Factor to scale the bounding box by

        Returns:
            Scaled BoundingBox
        """
        x_pos = round(self.x_pos * scale)
        y_pos = round(self.y_pos * scale)
        width = round(self.width * scale)
        height = round(self.height * scale)

        return BoundingBox(x_pos, y_pos, width, height)


def get_bounding_box_attributes() -> List[str]:
    """
    Returns a list with the names of the attributes of the bounding box class

    Returns:
        List of strings with the names of the BoundingBox attributes
    """
    # pylint: disable=not-an-iterable
    return [field.name for field in fields(BoundingBox)]


def split_bounding_boxes(
    bounding_box: BoundingBox, x_boxes: int, y_boxes: int
) -> List[BoundingBox]:
    """
    Splits the bounding_box in smaller boxes covering the same area

    Args:
        bounding_box: BoundingBox to be split
        x_boxes: Number of boxes to split the bounding box into along the x-axis
        y_boxes: Number of boxes to split the bounding box into along the y-axis
    Returns:
        A list of bounding boxes
    """
    assert x_boxes >= 1 and y_boxes >= 1
    new_width: float = bounding_box.width / x_boxes
    new_height: float = bounding_box.height / y_boxes
    bbox_list: List[BoundingBox] = []
    for x_idx in range(x_boxes):
        for y_idx in range(y_boxes):
            bbox = BoundingBox(
                bounding_box.x_pos + x_idx * new_width,
                bounding_box.y_pos + y_idx * new_height,
                new_width,
                new_height,
            )
            bbox_list.append(bbox)
    return bbox_list


def get_surrounding_bounding_box(*bbox_arrays: np.ndarray) -> BoundingBox:
    """
    Finds the surrounding bounding box from the given bounding box arrays which are in ullr format.
    The surrounding bounding box is defined as the smallest possible rectangle that contains all
    the inputted boxes.

    Args:
        bbox_arrays: Variable number of bounding box arrays
    Returns:
        BoundingBox that surrounds all of the given bounding boxes
    """
    coordinates = []
    for bbox_ar in bbox_arrays:
        x_min = np.min(bbox_ar[:, 0])
        y_min = np.min(bbox_ar[:, 1])
        x_max = np.max(bbox_ar[:, 2])
        y_max = np.max(bbox_ar[:, 3])

        coordinates.append([x_min, y_min, x_max, y_max])

    coordinates_array = np.array(coordinates)

    x_min = np.min(coordinates_array[:, 0])
    y_min = np.min(coordinates_array[:, 1])
    x_max = np.max(coordinates_array[:, 2])
    y_max = np.max(coordinates_array[:, 3])

    return bounding_box_from_ullr(x_min, y_min, x_max, y_max)


def bounding_box_from_ullr(
    left: float, top: float, right: float, bottom: float
) -> BoundingBox:
    """Returns a bounding box from given ullr coordinates"""
    return BoundingBox(left, top, right - left, bottom - top)


def get_scaled_values(
    values: tuple, image_size: ImageSize
) -> Tuple[float, float, float, float]:
    """Scales the values with the image size from pixel to relative"""
    img_size_list = [image_size.width, image_size.height]

    # noinspection PyTypeChecker
    return tuple(
        value / img_size_list[idx % 2]
        for value, idx in zip(
            values,
            range(4),
        )
    )
