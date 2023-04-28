from typing import List, Optional

from tensorflow.keras import layers
from tensorflow.keras.models import Model

from niceml.data.datadescriptions.datadescription import DataDescription
from niceml.data.datadescriptions.inputdatadescriptions import InputImageDataDescription
from niceml.data.datadescriptions.outputdatadescriptions import (
    OutputVectorDataDescription,
)
from niceml.dlframeworks.tensorflow.models.premodellayers import add_premodel_layers
from niceml.mlcomponents.models.modelfactory import ModelFactory
from niceml.utilities.commonutils import check_instance
from niceml.utilities.imagesize import ImageSize


class ClsModelFactory(ModelFactory):
    def __init__(
        self,
        model: Model,
        dense_layer_list: List[int],
        final_activation: str = "softmax",
        dense_activation: str = "relu",
        use_scale_lambda: bool = True,
        allow_preconvolution: bool = False,
        dropout_prob_list: Optional[List[float]] = None,
        additional_conv_layers: Optional[List[int]] = None,
    ):
        self.model_params = model
        self.dense_layer_list = dense_layer_list
        self.use_scale_lambda = use_scale_lambda
        self.final_activation = final_activation
        self.allow_preconvolution = allow_preconvolution
        self.dropout_prob_list = (
            dropout_prob_list if dropout_prob_list is not None else []
        )
        self.dense_activation = dense_activation
        self.additional_conv_layers = additional_conv_layers

    def create_model(self, data_desc: DataDescription):
        input_dd: InputImageDataDescription = check_instance(
            data_desc, InputImageDataDescription
        )
        output_dd: OutputVectorDataDescription = check_instance(
            data_desc, OutputVectorDataDescription
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
        model: Model = self.model_params
        actual_layer = model(actual_layer)

        actual_layer = create_dense_layers(
            actual_layer,
            self.dense_layer_list,
            self.dense_activation,
            self.dropout_prob_list,
        )

        actual_layer = layers.Dense(
            output_dd.get_output_size(), activation=self.final_activation
        )(actual_layer)

        model = Model(inputs=in_layer, outputs=actual_layer)
        model.summary()

        model = add_premodel_layers(
            allow_preconvolution=self.allow_preconvolution,
            use_input_scale=self.use_scale_lambda,
            data_desc=input_dd,
            model=model,
            additional_conv_layers=self.additional_conv_layers,
        )

        return model


def create_dense_layers(
    actual_layer,
    dense_layer_list: List[int],
    dense_activation,
    dropout_prob_list: Optional[List[float]] = None,
):
    if dropout_prob_list is None:
        dropout_prob_list = []
    actual_layer = layers.Flatten()(actual_layer)
    for idx, cur_nodes in enumerate(dense_layer_list):
        actual_layer = layers.Dense(cur_nodes, activation=dense_activation)(
            actual_layer
        )
        if idx < len(dropout_prob_list):
            cur_prob = dropout_prob_list[idx]
            actual_layer = layers.Dropout(cur_prob)(actual_layer)
    return actual_layer
