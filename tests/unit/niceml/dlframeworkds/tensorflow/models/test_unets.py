"""Writing tests for the unets model."""
import pytest

from niceml.data.datadescriptions.semsegdatadescritption import (
    SemSegDataDescription,
    create_number_semseg_datadescription,
)
from niceml.dlframeworks.tensorflow.models.layerfactory import DownscaleConvBlockFactory
from niceml.dlframeworks.tensorflow.models.unets import resnet50v2_unet
from niceml.utilities.imagesize import ImageSize, ImageSizeDivisionError


@pytest.fixture
def unet_model():
    return resnet50v2_unet()


@pytest.fixture
def unet_model_with_ds_layer_factory():
    return resnet50v2_unet(downscale_layer_factory=DownscaleConvBlockFactory([16, 32]))


def test_model_creation(unet_model):
    data_description = SemSegDataDescription(
        classes=create_number_semseg_datadescription(3),
        input_image_size=ImageSize(512, 256),
        output_image_size=ImageSize(512, 256),
    )
    model = unet_model.create_model(data_description)
    output_shape = model.output_shape
    output_model_img_size = ImageSize(output_shape[2], output_shape[1])
    assert output_model_img_size == data_description.get_output_image_size()


def test_model_creation_with_different_input_output_size(unet_model):
    data_description = SemSegDataDescription(
        classes=create_number_semseg_datadescription(3),
        input_image_size=ImageSize(1024, 512),
        output_image_size=ImageSize(512, 256),
    )
    model = unet_model.create_model(data_description)
    output_shape = model.output_shape
    output_model_img_size = ImageSize(output_shape[2], output_shape[1])
    assert output_model_img_size == data_description.get_output_image_size()


def test_model_creation_with_different_input_output_size_raises_error(unet_model):
    data_description = SemSegDataDescription(
        classes=create_number_semseg_datadescription(3),
        input_image_size=ImageSize(1024, 512),
        output_image_size=ImageSize(512, 300),
    )
    with pytest.raises(ImageSizeDivisionError):
        unet_model.create_model(data_description)


def test_model_creation_with_raises_small_output_size(unet_model):
    data_description = SemSegDataDescription(
        classes=create_number_semseg_datadescription(3),
        input_image_size=ImageSize(1024, 512),
        output_image_size=ImageSize(16, 8),
    )
    with pytest.raises(Exception):
        unet_model.create_model(data_description)


def test_model_creation_with_small_output_size(unet_model_with_ds_layer_factory):
    data_description = SemSegDataDescription(
        classes=create_number_semseg_datadescription(3),
        input_image_size=ImageSize(1024, 512),
        output_image_size=ImageSize(16, 8),
    )
    unet_model_with_ds_layer_factory.create_model(data_description)
