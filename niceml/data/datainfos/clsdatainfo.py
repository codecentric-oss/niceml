"""Module for ClsDataInfo"""
from dataclasses import dataclass
from typing import List, Union

import numpy as np

from niceml.data.datainfos.imagedatainfo import ImageDataInfo
from niceml.utilities.fsspec.locationutils import LocationConfig, get_location_uri


@dataclass
class ClsDataInfo(ImageDataInfo):
    """Contains all information about one data point for classification"""

    identifier: str
    class_idx: Union[int, List[int]]
    class_name: Union[str, List[str]]

    def get_info_dict(self) -> dict:
        return dict(
            identifier=self.identifier,
            class_idx=self.class_idx,
            class_name=self.class_name,
        )

    def get_identifier(self) -> str:
        return self.identifier

    def get_image_location(self) -> Union[dict, LocationConfig]:
        """Return the image filepath"""
        return self.image_location

    def get_image_filepath(self) -> str:
        """Return the image filepath"""
        return get_location_uri(self.image_location)

    def get_index_list(self) -> List[int]:
        """Return a list of class indexes"""
        return [self.class_idx] if isinstance(self.class_idx, int) else self.class_idx

    def get_name_list(self) -> List[str]:
        """Return a list of class names"""
        return (
            [self.class_name] if isinstance(self.class_name, str) else self.class_name
        )

    def get_index_of_name(self, name: str) -> int:
        """Return the index of the class with the given name"""
        return self.get_name_list().index(name)


@dataclass
class ClsData:
    """Contains all data for classification"""

    identifier: str
    image: np.ndarray
    class_idx: Union[int, List[int]]
    class_name: Union[str, List[str]]

    def get_identifier(self) -> str:
        """Return the identifier"""
        return self.identifier

    def get_index_list(self) -> List[int]:
        """Return a list of class indexes"""
        return [self.class_idx] if isinstance(self.class_idx, int) else self.class_idx

    def get_name_list(self) -> List[str]:
        """Return a list of class names"""
        return (
            [self.class_name] if isinstance(self.class_name, str) else self.class_name
        )

    def get_index_of_name(self, name: str) -> int:
        """Return the index of the class with the given name"""
        return self.get_name_list().index(name)
