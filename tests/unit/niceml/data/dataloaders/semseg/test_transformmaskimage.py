from random import randint

import numpy as np

from niceml.data.datadescriptions.semsegdatadescritption import (
    SemSegClassInfo,
    SemSegDataDescription,
    create_number_semseg_datadescription,
)
from niceml.data.dataloaders.semseg.transformmaskimage import transform_mask_image
from niceml.utilities.imagesize import ImageSize


def test_transform_mask_image_one_channel():
    img_size = ImageSize(100, 100)
    classes = create_number_semseg_datadescription(5)
    semseg_dd = SemSegDataDescription(
        classes=classes, input_image_size=img_size, output_image_size=img_size
    )

    input_mask_image = np.ones(img_size.to_numpy_shape(), dtype=np.uint8) * 255
    for cur_idx in range(6):
        input_mask_image[cur_idx * 10 : cur_idx * 10 + 10, 0:20] = cur_idx

    out_mask_image = transform_mask_image(
        input_mask_image, semseg_dd.get_class_idx_lut()
    )
    assert out_mask_image.shape == img_size.to_numpy_shape()
    assert np.sum(out_mask_image < 255) == 1000


def test_transform_mask_image_3_channels():
    img_size = ImageSize(100, 100)
    classes = [SemSegClassInfo([0, idx * 10, -1], f"{idx}") for idx in range(5)]
    semseg_dd = SemSegDataDescription(
        classes=classes, input_image_size=img_size, output_image_size=img_size
    )

    input_mask_image = np.ones(img_size.to_numpy_shape() + (3,), dtype=np.uint8) * 255
    for cur_idx in range(6):
        input_mask_image[cur_idx * 10 : cur_idx * 10 + 10, 0:20, 0] = 0
        input_mask_image[cur_idx * 10 : cur_idx * 10 + 10, 0:20, 1] = cur_idx * 10
        input_mask_image[cur_idx * 10 : cur_idx * 10 + 10, 0:20, 2] = randint(10, 100)

    out_mask_image = transform_mask_image(
        input_mask_image, semseg_dd.get_class_idx_lut()
    )
    assert out_mask_image.shape == img_size.to_numpy_shape()
    assert np.sum(out_mask_image < 255) == 1000
