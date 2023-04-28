"""Module of the ImageDataInfo"""
from abc import ABC
from dataclasses import dataclass
from os.path import basename
from typing import Union

from niceml.data.datainfos.datainfo import DataInfo
from niceml.utilities.fsspec.locationutils import LocationConfig


@dataclass
class ImageDataInfo(DataInfo, ABC):
    """Contains all information for image data"""

    image_location: Union[dict, LocationConfig]

    def get_filename(self) -> str:
        """
        Split the image_location from `self.image_location`

        Returns:
            Only the image_location as a str
        """
        return basename(self.get_identifier())

    def get_image_location(self) -> str:
        """Return the image filepath"""
        return self.image_location
