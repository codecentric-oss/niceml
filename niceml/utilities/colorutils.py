"""Module for all color functions and variables"""
from enum import Enum
from typing import List, Tuple

import numpy as np


class Color(tuple, Enum):
    """Enum for RGB color tuples used for visualization"""

    RED = (255, 0, 0)
    BLUE = (0, 0, 255)
    GREEN = (0, 255, 0)
    YELLOW = (250, 237, 39)
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    DARK_PURPLE = (147, 139, 161)


COLORS: List[Tuple[float, float, float]] = [
    (0.12156862745098039, 0.4666666666666667, 0.7058823529411765),
    (0.6823529411764706, 0.7803921568627451, 0.9098039215686274),
    (1.0, 0.4980392156862745, 0.054901960784313725),
    (1.0, 0.7333333333333333, 0.47058823529411764),
    (0.17254901960784313, 0.6274509803921569, 0.17254901960784313),
    (0.596078431372549, 0.8745098039215686, 0.5411764705882353),
    (0.8392156862745098, 0.15294117647058825, 0.1568627450980392),
    (1.0, 0.596078431372549, 0.5882352941176471),
    (0.5803921568627451, 0.403921568627451, 0.7411764705882353),
    (0.7725490196078432, 0.6901960784313725, 0.8352941176470589),
    (0.5490196078431373, 0.33725490196078434, 0.29411764705882354),
    (0.7686274509803922, 0.611764705882353, 0.5803921568627451),
    (0.8901960784313725, 0.4666666666666667, 0.7607843137254902),
    (0.9686274509803922, 0.7137254901960784, 0.8235294117647058),
    (0.4980392156862745, 0.4980392156862745, 0.4980392156862745),
    (0.7803921568627451, 0.7803921568627451, 0.7803921568627451),
    (0.7372549019607844, 0.7411764705882353, 0.13333333333333333),
    (0.8588235294117647, 0.8588235294117647, 0.5529411764705883),
    (0.09019607843137255, 0.7450980392156863, 0.8117647058823529),
    (0.6196078431372549, 0.8549019607843137, 0.8980392156862745),
]


def get_color_array(classes_array: List) -> np.ndarray:
    """
    Returns an array with colors for each class

    Args:
        classes_array: List of classes to generate colors for

    Returns:
        Array of one color per class
    """
    color_list = [get_color(color) for color in classes_array]
    return np.array(color_list)


def get_color(idx: int) -> Tuple[float, float, float]:
    """returns a color tuple with len 3 for a color between 0 and 1"""
    return COLORS[idx % len(COLORS)]


def get_color_uint(idx: int) -> Tuple[int, int, int]:
    """returns a color tuple with len 3 for a color between 0 and 255"""
    color = [int(x * 255) for x in get_color(idx)]
    return tuple(color)


def get_color_array_uint() -> np.ndarray:
    """returns a color array with shape (len(COLORS),3) with values between
    0 and 255"""
    color_list = [get_color(idx) for idx in range(len(COLORS))]
    color_array = np.array(color_list)
    color_array = (color_array * 255).astype(np.uint8)
    return color_array
