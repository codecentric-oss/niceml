"""Module for SemSegDataInfoListing"""
from os.path import basename, splitext
from typing import List, Optional, Union

from niceml.data.datadescriptions.datadescription import DataDescription
from niceml.data.datainfolistings.datainfolisting import DataInfoListing
from niceml.data.datainfos.semsegdatainfo import SemSegDataInfo
from niceml.utilities.fsspec.locationutils import (
    LocationConfig,
    join_location_w_path,
    open_location,
)
from niceml.utilities.ioutils import list_dir


class SemSegDataInfoListing(DataInfoListing):  # pylint: disable=too-few-public-methods
    """Lists all image files which have a corresponding mask suffix"""

    def __init__(
        self,
        location: Union[dict, LocationConfig],
        sub_dir: str,
        mask_suffix: str = "_mask",
        img_suffixes: Optional[List[str]] = None,
    ):
        self.mask_suffix = mask_suffix
        self.img_suffixes = img_suffixes or [".png", ".jpg", ".jpeg"]
        self.sub_dir = sub_dir
        self.location = location

    def _get_file_id(self, input_filepath: str) -> str:
        file_id: str = basename(splitext(input_filepath)[0])
        file_id = file_id.replace(self.mask_suffix, "")
        return file_id

    def list(self, data_description: DataDescription) -> List[SemSegDataInfo]:
        if len(self.sub_dir) > 0:
            location = join_location_w_path(self.location, self.sub_dir)
        else:
            location = self.location
        with open_location(location) as (data_fs, data_path):
            all_files = list_dir(data_path, file_system=data_fs)
        mask_file_dict = {
            self._get_file_id(x): x
            for x in all_files
            if splitext(x)[1] in self.img_suffixes and self.mask_suffix in basename(x)
        }

        image_files = [
            file
            for file in all_files
            if splitext(file)[1] in self.img_suffixes
            and self._get_file_id(file) in mask_file_dict
            and self.mask_suffix not in file
        ]

        data_info_list: List[SemSegDataInfo] = []
        for image_file in image_files:
            file_id = self._get_file_id(image_file)
            image_location = join_location_w_path(location, image_file)
            mask_location = join_location_w_path(location, mask_file_dict[file_id])
            data_info_list.append(
                SemSegDataInfo(
                    file_id=file_id,
                    image_location=image_location,
                    mask_location=mask_location,
                )
            )

        return data_info_list
