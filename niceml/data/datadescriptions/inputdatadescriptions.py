"""Module for data descriptions used for input"""
from abc import ABC, abstractmethod
from typing import List, Tuple

from niceml.data.datadescriptions.datadescription import DataDescription
from niceml.utilities.imagesize import ImageSize


class InputImageDataDescription(DataDescription, ABC):
    """DataDescription used for models with images as input"""

    @abstractmethod
    def get_input_image_size(self) -> ImageSize:
        """Returns the ImageSize of the input image(s)"""

    @abstractmethod
    def get_input_channel_count(self) -> int:
        """Returns the number of channels of the input image(s)"""

    def get_input_tensor_shape(self) -> Tuple[int, int, int]:
        """Returns the 3-dim shape of the input tensor [height, width, channel_count]"""
        return self.get_input_image_size().to_numpy_shape() + (
            self.get_input_channel_count(),
        )


class InputVectorDataDescription(DataDescription, ABC):
    """DataDescription used by models with vectors as input"""

    @abstractmethod
    def get_input_size(self) -> int:
        """Returns the size of the input vector(s)"""

    @abstractmethod
    def get_input_entry_names(self) -> List[str]:
        """Returns a name for each vector entry"""
