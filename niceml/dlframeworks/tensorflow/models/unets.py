"""Module for unets"""
import math
from typing import Any, Callable, List, Optional

from keras.applications.xception import Xception

# pylint: disable=import-error, no-name-in-module
from tensorflow.keras import layers
from tensorflow.keras.applications import VGG16, MobileNetV2, ResNet50, ResNet50V2
from tensorflow.keras.models import Model

from niceml.data.datadescriptions.datadescription import DataDescription
from niceml.data.datadescriptions.inputdatadescriptions import InputImageDataDescription
from niceml.data.datadescriptions.outputdatadescriptions import (
    OutputImageDataDescription,
)
from niceml.dlframeworks.tensorflow.models.layerfactory import LayerFactory
from niceml.dlframeworks.tensorflow.models.premodellayers import add_premodel_layers
from niceml.mlcomponents.models.modelfactory import ModelFactory
from niceml.utilities.commonutils import check_instance


# pylint: disable=too-many-instance-attributes,too-few-public-methods
class UNetModel(ModelFactory):
    """Factory method for creating a UNet model"""

    def __init__(  # pylint: disable=too-many-arguments,too-many-locals
        self,
        channels: List[int],
        skip_connection_names: List[str],
        model_factory: Callable,
        depth: Optional[int] = None,
        use_input_scale: bool = False,
        use_output_scale: bool = False,
        activation: str = "sigmoid",
        enable_skip_connections: bool = True,
        allow_preconvolution: bool = False,
        additional_conv_layers: Optional[List[int]] = None,
        downscale_layer_factory: Optional[LayerFactory] = None,
        post_layer_factory: Optional[LayerFactory] = None,
        **kwargs,
    ):
        """
        Creates a Resnet50 UNet variation for pixelwise output.
        The output has the same dimension as the input.

        Parameters
        ----------
        skip_connection_names: List[str]
            The names of the layers to use as skip connections.
        depth: Optional[int], default None
            Describes the amount of skip_connections used.
            If not given it uses the maximal amount w.r.t the given
            channels or the the maximal mobilenet depth (count of downsamplings, 5).
        channels: Optional[List[int]], default [16, 32, 48, 64, 128]
            How many channels after each upsampling should be used.
        use_input_scale: bool, default False
            If true the input is divided by 255.0
        use_output_scale: bool, default False
            If true the output is multiplied by 255.0
        activation: Optional[str], default sigmoid
            Final activation, used for last layer
        enable_skip_connections: Optional[bool], default True,
            Determines, whether to use skip connections
        allow_preconvolution: bool, default False
            Uses a convolution to normalize the amount of layers to three.
        model_params: Optional[dict], default None
            Additional params to init the modelfactory
        additional_conv_layers: Optional[List[int]], default None
            Additional conv layers to add between the input and model.
        downscale_layer_factory: Optional[LayerFactory], default None
            Factory to create the downscale layers.
        post_layer_factory: Optional[LayerFactory], default None
            Factory to create the post layers.

        """
        self.model_factory = model_factory
        self.model_params = kwargs
        self.channels: List[int] = [64, 128, 256, 512] if channels is None else channels
        self.depth: int = len(self.channels) + 1 if depth is None else depth
        # adjust channels again
        self.channels = self.channels[: self.depth - 1]
        self.skip_connection_names = skip_connection_names[: self.depth]
        self.activation = activation
        self.use_input_scale = use_input_scale
        self.use_output_scale = use_output_scale
        self.enable_skip_connections = enable_skip_connections
        self.allow_preconvolution = allow_preconvolution
        self.additional_conv_layers = additional_conv_layers
        self.downscale_layer_factory = downscale_layer_factory
        self.post_layer_factory = post_layer_factory

    # pylint: disable=too-many-locals
    def create_model(self, data_description: DataDescription) -> Any:
        """
        Create a model for the given data description.

        Args:
            data_description: Data description the model is based on
        Returns:
            A Unet model object
        """
        input_dd: InputImageDataDescription = check_instance(
            data_description, InputImageDataDescription
        )
        output_dd: OutputImageDataDescription = check_instance(
            data_description, OutputImageDataDescription
        )
        expected_input_channels = 3
        if (
            not self.allow_preconvolution
            and input_dd.get_input_channel_count() != expected_input_channels
        ):
            raise Exception(
                f"Input channels must have the size of {expected_input_channels}!"
                f" Instead size == {input_dd.get_input_channel_count()}"
            )
        input_image_size = input_dd.get_input_image_size()
        output_image_size = output_dd.get_output_image_size()
        skip_connection_count = len(self.skip_connection_names)
        image_size_scale = input_image_size.get_division_factor(output_image_size)

        if not math.log(image_size_scale, 2).is_integer():
            raise Exception(
                f"Image size scale must be a power of 2! Instead {image_size_scale}"
            )
        input_shape = input_image_size.to_numpy_shape() + (3,)
        inputs = layers.Input(shape=input_shape, name="image")
        actual_layer = inputs

        encoder = self.model_factory(
            input_tensor=actual_layer,
            weights="imagenet",
            include_top=False,
            **self.model_params,
        )
        encoder_output = encoder.get_layer(self.skip_connection_names.pop()).output

        actual_layer = encoder_output
        actual_image_size = input_image_size / (2 ** (skip_connection_count - 1))
        for skip_connection_name in reversed(self.skip_connection_names):
            if actual_image_size >= output_image_size:
                break
            channels = self.channels.pop()
            x_skip = encoder.get_layer(skip_connection_name).output
            actual_layer = layers.UpSampling2D((2, 2))(actual_layer)
            if self.enable_skip_connections:
                actual_layer = layers.Concatenate()([actual_layer, x_skip])

            actual_layer = layers.Conv2D(channels, (3, 3), padding="same")(actual_layer)
            actual_layer = layers.BatchNormalization()(actual_layer)
            actual_layer = layers.Activation("relu")(actual_layer)

            actual_layer = layers.Conv2D(channels, (3, 3), padding="same")(actual_layer)
            actual_layer = layers.BatchNormalization()(actual_layer)
            actual_layer = layers.Activation("relu")(actual_layer)
            actual_image_size *= 2

        while actual_image_size > output_image_size:
            if self.downscale_layer_factory is None:
                raise Exception(
                    "Downscale layer factory must be given, if the image size "
                    "after the skip connections is larger than the output image size!"
                )
            actual_layer = self.downscale_layer_factory.create_layers(actual_layer)
            actual_image_size /= 2

        if self.post_layer_factory is not None:
            actual_layer = self.post_layer_factory.create_layers(actual_layer)

        output_conv_name = "output_conv" if self.use_output_scale else "output"
        filters = output_dd.get_output_channel_count()
        if output_dd.get_use_void_class():
            filters += 1
        actual_layer = layers.Conv2D(
            name=output_conv_name,
            filters=filters,
            kernel_size=(1, 1),
            activation=self.activation,
            padding="same",
        )(actual_layer)

        if self.use_output_scale:
            actual_layer = layers.Lambda(lambda x: x * 255.0, name="output")(
                actual_layer
            )

        model = Model(inputs, actual_layer)
        model.summary()

        model = add_premodel_layers(
            allow_preconvolution=self.allow_preconvolution,
            use_input_scale=self.use_input_scale,
            data_desc=input_dd,
            model=model,
            additional_conv_layers=self.additional_conv_layers,
        )

        return model


def resnet50_unet(**kwargs):
    """Creates a ResNet50 U-Net model."""
    resnet_50_skipconnections: List[str] = [
        "image",
        "conv1_relu",
        "conv2_block3_out",
        "conv3_block4_out",
        "conv4_block6_out",
    ]
    channels = [64, 128, 256, 512]
    return UNetModel(
        channels=channels,
        skip_connection_names=resnet_50_skipconnections,
        model_factory=ResNet50,
        **kwargs,
    )


def mobilenetv2_unet(**kwargs):
    """Creates a MobileNetV2 U-Net model."""
    skip_connections: List[str] = [
        "image",
        "block_1_expand_relu",
        "block_3_expand_relu",
        "block_6_expand_relu",
        "block_13_expand_relu",
        "out_relu",
    ]
    channels = [48, 64, 128, 256, 512]
    return UNetModel(
        channels=channels,
        skip_connection_names=skip_connections,
        model_factory=MobileNetV2,
        **kwargs,
    )


def resnet50v2_unet(**kwargs):
    """Creates a ResNet50V2 U-Net model."""
    skip_connections: List[str] = [
        "image",
        "conv1_conv",
        "conv2_block3_1_relu",
        "conv3_block4_1_relu",
        "conv4_block6_1_relu",
        "post_relu",
    ]
    channels = [48, 64, 128, 256, 512]
    return UNetModel(
        channels=channels,
        skip_connection_names=skip_connections,
        model_factory=ResNet50V2,
        **kwargs,
    )


def vgg16_unet(**kwargs):
    """Creates a VGG16 U-Net model."""
    skip_connections: List[str] = [
        "block1_conv2",
        "block2_conv2",
        "block3_conv3",
        "block4_conv3",
        "block5_conv3",
        "block5_pool",
    ]
    channels = [48, 64, 128, 256, 512]
    return UNetModel(
        channels=channels,
        skip_connection_names=skip_connections,
        model_factory=VGG16,
        **kwargs,
    )


def xception_unet(**kwargs):
    """Creates a Xception U-Net model.
    WARNING: Downscaling needs to be 16 or greater!"""
    skip_connections: List[str] = [
        "image",
        "block2_sepconv2_bn",
        "block3_sepconv2_bn",
        "block4_sepconv2_bn",
        "block13_sepconv2_bn",
        "block14_sepconv2_act",
    ]
    channels = [64, 128, 256, 728, 1024]
    return UNetModel(
        channels=channels,
        skip_connection_names=skip_connections,
        model_factory=Xception,
        **kwargs,
    )
