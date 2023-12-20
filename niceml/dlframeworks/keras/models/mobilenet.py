from typing import Any

import tensorflow as tf
from tensorflow.keras import layers
from tensorflow.keras.applications.mobilenet_v2 import MobileNetV2
from tensorflow.keras.models import Model

from niceml.data.datadescriptions.datadescription import DataDescription
from niceml.data.datadescriptions.inputdatadescriptions import InputImageDataDescription
from niceml.data.datadescriptions.outputdatadescriptions import (
    OutputVectorDataDescription,
)
from niceml.mlcomponents.models.modelfactory import ModelFactory
from niceml.utilities.commonutils import check_instance


class OwnMobileNetModel(ModelFactory):
    def __init__(
        self,
        final_activation: str = "softmax",
        alpha: float = 0.5,
        use_scale_lambda: bool = True,
    ):
        self.alpha = alpha
        self.use_scale_lambda = use_scale_lambda
        self.final_activation = final_activation

    def create_model(self, data_desc: DataDescription) -> Any:
        input_dd: InputImageDataDescription = check_instance(
            data_desc, InputImageDataDescription
        )
        output_dd: OutputVectorDataDescription = check_instance(
            data_desc, OutputVectorDataDescription
        )
        in_layer = tf.keras.layers.Input(input_dd.get_input_tensor_shape())
        actual_layer = in_layer
        if self.use_scale_lambda:
            actual_layer = layers.Lambda(lambda x: x / 255.0)(actual_layer)
        mn2: Model = MobileNetV2(
            include_top=False, alpha=self.alpha, weights="imagenet"
        )
        actual_layer = mn2(actual_layer)
        actual_layer = layers.Conv2D(
            filters=256,
            kernel_size=(3, 3),
            strides=(2, 2),
            padding="same",
            name="conv",
            activation="relu",
        )(actual_layer)
        actual_layer = layers.Flatten()(actual_layer)
        actual_layer = layers.Dense(192, activation="relu")(actual_layer)
        actual_layer = layers.Dense(512, activation="relu")(actual_layer)
        actual_layer = layers.Dense(
            output_dd.get_output_size(), activation=self.final_activation
        )(actual_layer)

        model = Model(inputs=in_layer, outputs=actual_layer)
        model.summary()
        return model
