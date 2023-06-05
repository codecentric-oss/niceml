"""Module for SemSegClassInfo and SemSegDataDescription"""
from dataclasses import dataclass
from typing import List

import numpy as np

from niceml.data.datadescriptions.inputdatadescriptions import InputImageDataDescription
from niceml.data.datadescriptions.outputdatadescriptions import (
    OutputImageDataDescription,
)
from niceml.utilities.imagesize import ImageSize


@dataclass
class SemSegClassInfo:
    """
    Class for (target or output) class information (name and color of mask image)

    Parameters:
        color: Color as list of three uint8 values (rgb) or -1 as any value. e.g. [-1, 255, -1]
            will look for 255 in the g-channel and ignore r- and b-channel.
        name: Name of the class
    """

    color: List[int]
    name: str


@dataclass
class SemSegDataDescription(InputImageDataDescription, OutputImageDataDescription):
    """
    DataDescription for SemSeg data

    Parameters:
       classes: List[SemSegClassInfo]
           Each entry is an initialized SemSegClassInfo, for which the name (str) and
           color (List[int]) must be present.
           The index in output array (third axis) is defined by the order of the classes list.
           Usually the color has to be a list of length 3 with uint8 values. The only exception
           is the usage of -1 as any value. e.g. [-1, 255, -1] will look for 255 in the g-channel
           and ignore r- and b-channel.
    """

    classes: List[SemSegClassInfo]
    input_image_size: ImageSize
    output_image_size: ImageSize
    channel_count: int = 3
    use_background_class: bool = False

    def get_input_image_size(self) -> ImageSize:
        """Returns the input size of the image(s)"""
        return self.input_image_size

    def get_output_channel_names(self) -> List[str]:
        """Returns the names of the output channels"""
        return [x.name for x in self.classes]

    def get_input_channel_count(self) -> int:
        """Returns the number of input channels"""
        return self.channel_count

    def get_output_image_size(self) -> ImageSize:
        """Returns the output size of the image(s)"""
        return self.output_image_size

    def get_class_idx_lut(self) -> np.ndarray:
        """Returns the class index lut to transform the mask image"""  # QUEST: what is lut?
        return np.array([cls.color for cls in self.classes], dtype=int)

    def get_class_name_from_idx(self, idx: int) -> str:
        """Returns the class name of the class at position `idx` in `self.classes`"""
        return self.get_output_channel_names()[idx]

    def get_use_void_class(self) -> bool:
        """returns bool to use background_class"""
        return self.use_background_class


def create_number_semseg_datadescription(
    max_number: int,
) -> List[SemSegClassInfo]:  # QUEST: still used?
    """Creates a list of SemSegClassInfo for the number dataset"""  # QUEST: better docstring
    return [SemSegClassInfo([idx], f"{idx}") for idx in range(max_number)]
