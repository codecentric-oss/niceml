"""
niceml implementation of the retinanet
This is a modified version of the original implementation

https://github.com/keras-team/keras-io/blob/master/examples/vision/retinanet.py

"""
from typing import Any, List, Optional

import keras
import numpy as np
import tensorflow as tf
from keras import layers
from keras.applications.resnet import ResNet50
from keras.models import Model

from niceml.data.datadescriptions.datadescription import DataDescription
from niceml.data.datadescriptions.inputdatadescriptions import InputImageDataDescription
from niceml.data.datadescriptions.outputdatadescriptions import (
    OutputObjDetDataDescription,
)
from niceml.dlframeworks.tensorflow.models.premodellayers import add_premodel_layers
from niceml.mlcomponents.models.modelfactory import ModelFactory
from niceml.utilities.commonutils import check_instance
from niceml.utilities.imagesize import ImageSize


def get_backbone(input_size: ImageSize) -> Model:
    """Builds ResNet50 with pre-trained imagenet weights"""
    input_shape = input_size.to_numpy_shape() + (3,)
    backbone = ResNet50(include_top=False, input_shape=input_shape)
    c3_output, c4_output, c5_output = [
        backbone.get_layer(layer_name).output
        for layer_name in ["conv3_block4_out", "conv4_block6_out", "conv5_block3_out"]
    ]
    return keras.Model(
        inputs=[backbone.inputs], outputs=[c3_output, c4_output, c5_output]
    )


def feature_pyramid(
    layer_scaled_x, layer_scaled_2x, layer_scaled_4x, filter_count: int = 256
):
    """creates a feature pyramid"""
    conv_c3_1x1 = layers.Conv2D(filter_count, 1, 1, "same")
    conv_c4_1x1 = layers.Conv2D(filter_count, 1, 1, "same")
    conv_c5_1x1 = layers.Conv2D(filter_count, 1, 1, "same")
    conv_c3_3x3 = layers.Conv2D(filter_count, 3, 1, "same")
    conv_c4_3x3 = layers.Conv2D(filter_count, 3, 1, "same")
    conv_c5_3x3 = layers.Conv2D(filter_count, 3, 1, "same")
    conv_c6_3x3 = layers.Conv2D(filter_count, 3, 2, "same")
    conv_c7_3x3 = layers.Conv2D(filter_count, 3, 2, "same")
    upsample_2x = layers.UpSampling2D(2)
    layer_scaled_x = conv_c3_1x1(layer_scaled_x)
    layer_scaled_2x = conv_c4_1x1(layer_scaled_2x)
    layer_scaled_4x = conv_c5_1x1(layer_scaled_4x)
    layer_scaled_2x = layer_scaled_2x + upsample_2x(layer_scaled_4x)
    layer_scaled_x = layer_scaled_x + upsample_2x(layer_scaled_2x)
    layer_scaled_x = conv_c3_3x3(layer_scaled_x)
    layer_scaled_2x = conv_c4_3x3(layer_scaled_2x)
    layer_scaled_4x = conv_c5_3x3(layer_scaled_4x)
    layer_scaled_8x = conv_c6_3x3(layer_scaled_4x)
    layer_scaled_16x = conv_c7_3x3(tf.nn.relu(layer_scaled_8x))
    return [
        layer_scaled_x,
        layer_scaled_2x,
        layer_scaled_4x,
        layer_scaled_8x,
        layer_scaled_16x,
    ]


def build_head(output_filters, bias_init, layer_count: int = 256):
    """Builds the class/box predictions head.

    Arguments:
      output_filters: Number of convolution filters in the final layer.
      bias_init: Bias Initializer for the final convolution layer.
      layer_count: number of layers for convolutions

    Returns:
      A keras sequential model representing either the classification
        or the box regression head depending on `output_filters`.
    """
    head = keras.Sequential([keras.Input(shape=[None, None, layer_count])])
    kernel_init = tf.initializers.RandomNormal(0.0, 0.01)
    for _ in range(4):
        head.add(
            keras.layers.Conv2D(
                layer_count, 3, padding="same", kernel_initializer=kernel_init
            )
        )
        head.add(keras.layers.ReLU())
    head.add(
        keras.layers.Conv2D(
            output_filters,
            3,
            1,
            padding="same",
            kernel_initializer=kernel_init,
            bias_initializer=bias_init,
        )
    )
    return head


def retina_net(
    feature_layers: list,
    num_classes: int,
    anchor_per_cell: int,
    coordinates_count: int,
    anchor_feature_count_list: List[int],
):
    """
    Builds the heads of the feature_layers and returns one output tensor

    :param feature_layers: tensors with all feature maps
    :param num_classes: count of classes
    :param anchor_per_cell: how many anchors are generated per feature cell
    :param coordinates_count: how many coordinates are required to
           represent the object (e.g. bounding box)
    :param anchor_feature_count_list: a list of anchors per feature map
    :return: output_tensor with shape [batch_size, num_anchors, coordinates_count + num_classes]
    """
    prior_probability = tf.constant_initializer(-np.log((1 - 0.01) / 0.01))
    cls_head = build_head(anchor_per_cell * num_classes, prior_probability)
    box_head = build_head(anchor_per_cell * coordinates_count, "zeros")

    cls_outputs = []
    box_outputs = []

    assert len(feature_layers) == len(anchor_feature_count_list)

    for feature, cur_anchor_count in zip(feature_layers, anchor_feature_count_list):
        cur_box_head = box_head(feature)
        box_outputs.append(
            tf.reshape(cur_box_head, [-1, cur_anchor_count, coordinates_count])
        )
        cur_cls_head = cls_head(feature)
        cls_outputs.append(
            tf.reshape(cur_cls_head, [-1, cur_anchor_count, num_classes])
        )
    cls_outputs = tf.concat(cls_outputs, axis=1)
    box_outputs = tf.concat(box_outputs, axis=1)
    return tf.concat([box_outputs, cls_outputs], axis=-1)


class RetinaNetFactory(ModelFactory):  # pylint: disable=too-few-public-methods
    """Modelfactory which creates a RetinaNet for ObjectDetection"""

    def __init__(
        self,
        use_scale_lambda: bool = True,
        allow_preconvolution: bool = False,
        additional_conv_layers: Optional[List[int]] = None,
    ):
        self.use_scale_lambda = use_scale_lambda
        self.allow_preconvolution = allow_preconvolution
        self.additional_conv_layers = additional_conv_layers

    def create_model(self, data_description: DataDescription) -> Any:
        input_dd: InputImageDataDescription = check_instance(
            data_description, InputImageDataDescription
        )
        output_dd: OutputObjDetDataDescription = check_instance(
            data_description, OutputObjDetDataDescription
        )
        if not self.allow_preconvolution and input_dd.get_input_channel_count() != 3:
            raise Exception(
                f"Input channels must have the size of 3! Instead "
                f"{input_dd.get_input_channel_count()}"
            )
        input_size: ImageSize = input_dd.get_input_image_size()
        input_shape = input_size.to_numpy_shape() + (3,)
        in_layer = layers.Input(shape=input_shape, name="image")
        actual_layer = in_layer
        model: Model = get_backbone(input_size)
        layer_list = model(actual_layer)
        layer_scaled_8, layer_scaled_16, layer_scaled_32 = layer_list
        before_head_layers = feature_pyramid(
            layer_scaled_8, layer_scaled_16, layer_scaled_32
        )
        out_layer = retina_net(
            before_head_layers,
            output_dd.get_output_class_count(),
            anchor_per_cell=output_dd.get_anchorcount_per_feature(),
            coordinates_count=output_dd.get_coordinates_count(),
            anchor_feature_count_list=output_dd.get_anchorcount_featuremap_list(),
        )
        model = keras.Model(inputs=[in_layer], outputs=[out_layer])

        model = add_premodel_layers(
            allow_preconvolution=self.allow_preconvolution,
            use_input_scale=self.use_scale_lambda,
            data_desc=input_dd,
            model=model,
            additional_conv_layers=self.additional_conv_layers,
        )

        return model
