"""Module for ClsDataInfoListing"""
from os.path import basename, splitext
from typing import Callable, List, Optional, Union

from niceml.data.datadescriptions.datadescription import DataDescription
from niceml.data.datadescriptions.outputdatadescriptions import (
    OutputVectorDataDescription,
)
from niceml.data.datainfolistings.datainfolisting import DataInfoListing
from niceml.data.datainfolistings.objdetdatainfolisting import list_data
from niceml.data.datainfos.clsdatainfo import ClsDataInfo
from niceml.data.datainfos.objdetdatainfo import ObjDetDataInfo
from niceml.utilities.commonutils import check_instance
from niceml.utilities.fsspec.locationutils import (
    LocationConfig,
    join_location_w_path,
    open_location,
)
from niceml.utilities.ioutils import list_dir


class LabelClsDataInfoListing(
    DataInfoListing
):  # pylint: disable=too-few-public-methods, too-many-arguments
    """Lists all consistent clsdata in one folder and returns a list of data infos"""

    def __init__(
        self,
        data_location: Union[dict, LocationConfig],
        sub_dir: str,
        label_suffix: str = ".json",
        image_suffixes: Optional[List[str]] = None,
    ):
        self.sub_dir = sub_dir
        self.data_location = data_location
        self.label_suffix = label_suffix
        self.image_suffixes = image_suffixes or [".png", ".jpg", ".jpeg"]

    def list(self, data_description: DataDescription) -> List[ClsDataInfo]:
        output_data_description: OutputVectorDataDescription = check_instance(
            data_description, OutputVectorDataDescription
        )
        if len(self.sub_dir) > 0:
            location = join_location_w_path(self.data_location, self.sub_dir)
        else:
            location = self.data_location
        class_names = output_data_description.get_output_entry_names()
        class_count = len(class_names)
        data_info_list = list_data(
            class_count=class_count,
            class_names=class_names,
            location=location,
            label_suffix=self.label_suffix,
            image_suffixes=self.image_suffixes,
            use_empty_images=False,
        )

        new_data_info_list = []
        cur_data_info: ObjDetDataInfo
        for cur_data_info in data_info_list:
            cur_cls_names = list({x.class_name for x in cur_data_info.labels})
            cur_class_indexes = output_data_description.get_index_for_name(
                cur_cls_names
            )
            new_data_info = ClsDataInfo(
                identifier=cur_data_info.get_identifier(),
                image_location=cur_data_info.image_location,
                class_name=cur_cls_names,
                class_idx=cur_class_indexes,
            )
            new_data_info_list.append(new_data_info)

        return new_data_info_list


class DirClsDataInfoListing(
    DataInfoListing
):  # pylint: disable=too-few-public-methods, too-many-arguments
    """Lists all images in one folder and takes the class from the filename"""

    def __init__(
        self,
        location: Union[dict, LocationConfig],
        sub_dir: str,
        class_extractor: Optional[Callable] = None,
        image_suffixes: Optional[List[str]] = None,
    ):
        self.sub_dir = sub_dir
        self.location = location
        self.class_extractor = class_extractor or (
            lambda x: splitext(x)[0].rsplit("_", maxsplit=1)[-1]
        )
        self.image_suffixes = image_suffixes or [".png", ".jpg", ".jpeg"]

    def list(self, data_description: DataDescription) -> List[ClsDataInfo]:
        output_data_description: OutputVectorDataDescription = check_instance(
            data_description, OutputVectorDataDescription
        )
        if len(self.sub_dir) > 0:
            location = join_location_w_path(self.location, self.sub_dir)
        else:
            location = self.location
        with open_location(location) as (data_fs, data_path):
            all_files = list_dir(data_path, return_full_path=False, file_system=data_fs)
        image_files = [
            file for file in all_files if splitext(file)[1] in self.image_suffixes
        ]
        data_info_list: List[ClsDataInfo] = []
        for cur_image in image_files:
            cur_class = self.class_extractor(cur_image)
            cls_index = output_data_description.get_index_for_name(cur_class)
            if cls_index is not None:
                cur_class = output_data_description.get_name_for_index(cls_index)
                identifier = basename(cur_image)
                image_location = join_location_w_path(location, cur_image)
                cur_data_info = ClsDataInfo(
                    identifier=identifier,
                    image_location=image_location,
                    class_idx=cls_index,
                    class_name=cur_class,
                )
                data_info_list.append(cur_data_info)

        return data_info_list
