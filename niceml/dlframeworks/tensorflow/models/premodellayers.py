from typing import List, Optional

from tensorflow.keras import Model, layers

from niceml.data.datadescriptions.inputdatadescriptions import InputImageDataDescription


def add_premodel_layers(
    allow_preconvolution: bool,
    use_input_scale: bool,
    data_desc: InputImageDataDescription,
    model: Model,
    print_summary: bool = True,
    output_names: Optional[List[str]] = None,
    additional_conv_layers: Optional[List[int]] = None,
) -> Model:
    use_preconvolution: bool = (
        allow_preconvolution and data_desc.get_input_channel_count() != 3
    )
    if use_preconvolution or use_input_scale:
        inputs = layers.Input(shape=data_desc.get_input_tensor_shape(), name="image")
        actual_layer = inputs
        if use_input_scale:
            actual_layer = layers.Lambda(lambda x: x / 255.0)(actual_layer)

        if use_preconvolution:
            additional_conv_layers = additional_conv_layers or []
            for cur_layer_count in additional_conv_layers:
                actual_layer = layers.Conv2D(
                    cur_layer_count,
                    kernel_size=(3, 3),
                    activation="relu",
                    padding="same",
                )(actual_layer)
            actual_layer = layers.Conv2D(3, kernel_size=(1, 1), activation="relu")(
                actual_layer
            )
        actual_layer = model(actual_layer)
        if output_names is not None:
            if type(actual_layer) is not list:
                actual_layer = [actual_layer]
            actual_layer = [
                layers.Lambda(lambda x: x, name=name)(layer)
                for layer, name in zip(actual_layer, output_names)
            ]

        model = Model(inputs, actual_layer)
        if print_summary:
            model.summary()
    return model
