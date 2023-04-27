"""Module for SemsegDataINfo and SemsegData"""
from dataclasses import dataclass
from typing import Union

import numpy as np

from niceml.data.datainfos.imagedatainfo import ImageDataInfo
from niceml.utilities.fsspec.locationutils import LocationConfig


@dataclass
class SemSegDataInfo(ImageDataInfo):
    """Stores information data about SemSeg"""

    file_id: str
    mask_location: Union[dict, LocationConfig]

    def get_info_dict(self) -> dict:
        image_uri = (
            self.image_location["uri"]
            if isinstance(self.image_location, dict)
            else self.image_location.uri
        )
        mask_uri = (
            self.mask_location["uri"]
            if isinstance(self.mask_location, dict)
            else self.mask_location.uri
        )
        # pylint: disable=use-dict-literal
        return dict(file_id=self.file_id, image_uri=image_uri, mask_uri=mask_uri)

    def get_identifier(self) -> str:
        return self.file_id


@dataclass
class SemSegData:
    """Stores content Data about SemSeg"""

    file_id: str
    image: np.ndarray
    mask_image: np.ndarray
