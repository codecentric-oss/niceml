"""Module for ObjDetDataLoader"""
from niceml.data.datadescriptions.inputdatadescriptions import InputImageDataDescription
from niceml.data.datainfos.objdetdatainfo import ObjDetData, ObjDetDataInfo
from niceml.data.dataloaders.dataloader import DataLoader
from niceml.utilities.commonutils import check_instance
from niceml.utilities.fsspec.locationutils import open_location
from niceml.utilities.imageloading import load_img_uint8


class ObjDetDataLoader(DataLoader):
    """DataLoader for ObjDetDataLoader"""

    def load_data(self, data_info: ObjDetDataInfo) -> ObjDetData:
        """Loads and returns object detection data (ObjDetData)"""
        input_data_description: InputImageDataDescription = check_instance(
            self.data_description, InputImageDataDescription
        )
        with open_location(data_info.image_location) as (image_fs, image_path):
            image = load_img_uint8(
                image_path,
                file_system=image_fs,
                target_image_size=input_data_description.get_input_image_size(),
            )

        return ObjDetData(image=image, labels=data_info.labels)
