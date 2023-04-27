"""Module for ClsDataLoader"""
from niceml.data.datadescriptions.inputdatadescriptions import InputImageDataDescription
from niceml.data.datainfos.clsdatainfo import ClsData, ClsDataInfo
from niceml.data.dataloaders.dataloader import DataLoader
from niceml.utilities.commonutils import check_instance
from niceml.utilities.imageloading import load_img_uint8


class ClsDataLoader(DataLoader):
    """DataLoader for image classification data"""

    def load_data(self, data_info: ClsDataInfo) -> ClsData:
        """Loads and returns image classification data from 'data_info'"""
        input_data_description: InputImageDataDescription = check_instance(
            self.data_description, InputImageDataDescription
        )
        image = load_img_uint8(
            data_info.image_location,
            target_image_size=input_data_description.get_input_image_size(),
        )
        return ClsData(
            identifier=data_info.get_identifier(),
            image=image,
            class_name=data_info.get_name_list(),
            class_idx=data_info.get_index_list(),
        )
