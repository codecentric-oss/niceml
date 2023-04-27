"""Module for SemSegDataLoader"""

from niceml.data.datadescriptions.semsegdatadescritption import SemSegDataDescription
from niceml.data.datainfos.semsegdatainfo import SemSegData, SemSegDataInfo
from niceml.data.dataloaders.dataloader import DataLoader
from niceml.data.dataloaders.semseg.transformmaskimage import transform_mask_image
from niceml.utilities.commonutils import check_instance
from niceml.utilities.fsspec.locationutils import open_location
from niceml.utilities.imageloading import load_img_uint8


class SemSegDataLoader(DataLoader):
    """Implementation of SemSegDataLoader"""

    def load_data(self, data_info: SemSegDataInfo) -> SemSegData:
        """
        Takes a SemSegDataInfo object as input, which contains all the information needed to load
        the image and mask files. The function returns a SemSegData object, which contains
        both the image and mask data.

        Args:
            data_info: SemSegDataInfo: Contains SemSeg data info

        Returns:
            A SemSegData object

        """
        semseg_dd: SemSegDataDescription = check_instance(
            self.data_description, SemSegDataDescription
        )

        class_lut = semseg_dd.get_class_idx_lut()
        with open_location(data_info.image_location) as (image_fs, image_path):
            image = load_img_uint8(
                image_path,
                file_system=image_fs,
                target_image_size=semseg_dd.get_input_image_size(),
            )
        with open_location(data_info.mask_location) as (mask_fs, mask_path):
            mask_image = load_img_uint8(
                mask_path,
                file_system=mask_fs,
                target_image_size=semseg_dd.get_input_image_size(),
            )

        mask_image = transform_mask_image(mask_image, class_lut)
        return SemSegData(
            file_id=data_info.get_identifier(), image=image, mask_image=mask_image
        )
