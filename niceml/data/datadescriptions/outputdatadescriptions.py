"""Module for output datadescriptions"""
from abc import ABC, abstractmethod
from typing import List, Optional, Tuple, Union

from niceml.data.datadescriptions.datadescription import DataDescription
from niceml.utilities.imagesize import ImageSize


class OutputImageDataDescription(DataDescription, ABC):
    """DataDescription used for models with images as output (e.g. SemSeg)"""

    @abstractmethod
    def get_output_channel_names(self) -> List[str]:
        """Returns a list of the output channel names"""

    def get_output_channel_count(self) -> int:
        """Returns the number of output channels"""
        return len(self.get_output_channel_names())

    @abstractmethod
    def get_output_image_size(self) -> ImageSize:
        """Returns the ImageSize of the input image(s)"""

    def get_output_tensor_shape(self) -> Tuple[int, int, int]:
        """Returns the 3-dim shape of the input tensor [height, width, channel_count]"""
        return self.get_output_image_size().to_numpy_shape() + (
            self.get_output_channel_count(),
        )

    @abstractmethod
    def get_use_void_class(self) -> bool:
        """Returns whether the model uses a default class (e.g. background)"""


class OutputVectorDataDescription(DataDescription, ABC):
    """DataDescription used by models with vectors as output"""

    @abstractmethod
    def get_output_size(self) -> int:
        """Returns the size of the output vector(s)"""

    @abstractmethod
    def get_output_entry_names(self) -> List[str]:
        """Returns a name for each vector entry"""

    def get_index_for_name(
        self, name: Union[str, List[str]]
    ) -> Optional[Union[int, List[int]]]:
        """Returns the index of the given output entry name(s) as int or list of indices"""
        if isinstance(name, str) and name in self.get_output_entry_names():
            return self.get_output_entry_names().index(name)
        if isinstance(name, list):
            index_list = []
            for cur_name in name:
                cur_index = self.get_index_for_name(cur_name)
                if cur_index is None:
                    continue
                if isinstance(cur_index, list):
                    index_list += cur_index
                else:
                    index_list.append(cur_index)
            index_list = sorted(list(set(index_list)))
            return None if len(index_list) == 0 else index_list
        return None

    def get_name_for_index(self, index: Union[int, List[int]]) -> Union[str, List[str]]:
        """Returns a name or list of names for given class index or indices"""
        output_names = self.get_output_entry_names()
        if isinstance(index, list):
            return [output_names[cur_idx] for cur_idx in index]
        return output_names[index]


class OutputObjDetDataDescription(DataDescription, ABC):
    """Abstract baseclass for OutputObjDetDataDescription"""

    @abstractmethod
    def get_featuremap_scales(self) -> List[int]:
        """
        Returns the scale per feature map as int.
        E.g. 2 means (1024,1024) -> (512, 512)
        It is assumed that a feature map is always smaller than
        the original image.
        """

    @abstractmethod
    def get_coordinates_count(self) -> int:
        """
        Returns the count of coordinates required to represent
        the object (e.g. bounding box: 4)
        """

    def get_featuremap_count(self) -> int:
        """Returns the number of feature maps. Should be the length of the featuremap_scales."""
        return len(self.get_featuremap_scales())

    @abstractmethod
    def get_anchorcount_per_feature(self) -> int:
        """Returns the number of anchors which are generated per feature cell"""

    def get_anchorcount_per_image(self) -> int:
        """Sums up all generated anchors for all feature maps and returns it."""
        return sum(self.get_anchorcount_featuremap_list())

    @abstractmethod
    def get_anchorcount_for_scale(self, scale: int) -> int:
        """Calculates the anchorcount for a specific scale"""

    def get_anchorcount_featuremap_list(self) -> List[int]:
        """Returns the anchorcount for the feature list"""
        return [
            self.get_anchorcount_for_scale(scale)
            for scale in self.get_featuremap_scales()
        ]

    @abstractmethod
    def get_anchor_aspect_ratios(self) -> List[float]:
        """Returns the aspect ratios for each feature map"""

    @abstractmethod
    def get_anchor_scales(self) -> List[float]:
        """Returns the scales for each feature map"""

    @abstractmethod
    def get_box_variance(self) -> List[float]:
        """Returns the box_variance list (length of 4)"""

    @abstractmethod
    def get_base_area_side(self) -> float:
        """Returns one side of a square base, which is used to determine the anchor size"""

    def get_output_class_count(self) -> int:
        """Returns the count of output classes used"""
        return len(self.get_output_class_names())

    @abstractmethod
    def get_output_class_names(self) -> List[str]:
        """Returns the used output class names"""
