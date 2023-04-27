"""Module for ObjDetDataInfoListing"""
from os.path import join, splitext
from typing import List, Optional, Union

from attrs import asdict

from niceml.data.datadescriptions.outputdatadescriptions import (
    OutputObjDetDataDescription,
)
from niceml.data.datainfolistings.datainfolisting import DataInfoListing
from niceml.data.datainfos.objdetdatainfo import ObjDetDataInfo
from niceml.utilities.boundingboxes.bboxlabeling import (
    ObjDetImageLabel,
    ObjDetInstanceLabel,
)
from niceml.utilities.fsspec.locationutils import (
    LocationConfig,
    join_location_w_path,
    open_location,
)
from niceml.utilities.ioutils import list_dir, read_json


class ObjDetDataInfoListing(
    DataInfoListing
):  # pylint: disable=too-few-public-methods, too-many-arguments
    """Lists all consistent objdetdata in one folder and returns datainfolist"""

    def __init__(
        self,
        location: Union[dict, LocationConfig],
        sub_dir: str,
        label_suffix: str = ".json",
        image_suffixes: Optional[List[str]] = None,
        use_empty_images: bool = True,
    ):
        self.sub_dir = sub_dir
        self.location = location
        self.label_suffix = label_suffix
        self.image_suffixes = image_suffixes or [".png", ".jpg", ".jpeg"]
        self.use_empty_image = use_empty_images

    def list(
        self, data_description: OutputObjDetDataDescription
    ) -> List[ObjDetDataInfo]:
        if len(self.sub_dir) > 0:
            location = join_location_w_path(self.location, self.sub_dir)
        else:
            location = self.location
        class_count = data_description.get_output_class_count()
        class_names = data_description.get_output_class_names()
        data_info_list = list_data(
            class_count=class_count,
            class_names=class_names,
            location=location,
            label_suffix=self.label_suffix,
            image_suffixes=self.image_suffixes,
            use_empty_images=self.use_empty_image,
        )

        return data_info_list


# pylint: disable=too-many-arguments, too-many-locals
def list_data(
    class_count: int,
    class_names: List[str],
    location: Union[dict, LocationConfig],
    label_suffix: str,
    image_suffixes: List[str],
    use_empty_images: bool,
) -> List[ObjDetDataInfo]:
    """Lists all consistent objdetdata in one folder and returns datainfolist"""
    with open_location(location) as (data_fs, data_path):
        all_files = list_dir(data_path, file_system=data_fs)
        label_file_set = set(
            splitext(x)[0] for x in all_files if splitext(x)[1] == label_suffix
        )
        image_files = [
            file
            for file in all_files
            if splitext(file)[1] in image_suffixes
            and splitext(file)[0] in label_file_set
        ]
        data_info_list: List[ObjDetDataInfo] = []
        for cur_img_file in image_files:
            data = read_json(
                join(data_path, splitext(cur_img_file)[0]) + label_suffix,
                file_system=data_fs,
            )
            image_label: ObjDetImageLabel = ObjDetImageLabel(**data)
            # pylint: disable=use-dict-literal
            labels = [
                ObjDetInstanceLabel(
                    **{
                        **asdict(lbl),
                        **dict(class_index=class_names.index(lbl.class_name)),
                    }
                )
                for lbl in image_label.labels
                if lbl.class_name in class_names
            ]
            if use_empty_images or len(labels) > 0:
                cur_data_info = ObjDetDataInfo(
                    image_location=join_location_w_path(location, cur_img_file),
                    class_count_in_dataset=class_count,
                    labels=labels,
                )
                data_info_list.append(cur_data_info)
    return data_info_list
