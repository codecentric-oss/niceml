"""Module for ownmlp for tensorflow model"""
from typing import Any, List

from tensorflow.keras import Sequential, layers  # pylint: disable=import-error

from niceml.data.datadescriptions.datadescription import DataDescription
from niceml.data.datadescriptions.inputdatadescriptions import InputVectorDataDescription
from niceml.data.datadescriptions.outputdatadescriptions import (
    OutputVectorDataDescription,
)
from niceml.mlcomponents.models.modelfactory import ModelFactory
from niceml.utilities.commonutils import check_instance


class OwnMLP(ModelFactory):  # pylint: disable=too-few-public-methods
    """Modelfactory for a mlp"""

    def __init__(
        self,
        hidden_layers: List[int],
        activation: str = "relu",
        final_activation: str = "linear",
        do_summary: bool = True,
    ):
        self.hidden_layers = hidden_layers
        self.activation = activation
        self.do_summary = do_summary
        self.final_activation = final_activation

    def create_model(self, data_description: DataDescription) -> Any:
        input_dd: InputVectorDataDescription = check_instance(
            data_description, InputVectorDataDescription
        )
        output_dd: OutputVectorDataDescription = check_instance(
            data_description, OutputVectorDataDescription
        )
        model = Sequential()
        input_size = input_dd.get_input_size()
        # first hidden layer
        count = self.hidden_layers.pop(0)
        model.add(
            layers.Dense(count, activation=self.activation, input_shape=(input_size,))
        )
        for count in self.hidden_layers:
            model.add(layers.Dense(count, activation=self.activation))

        # Outputs from dense layer are projected onto output layer
        target_size = output_dd.get_output_size()
        model.add(layers.Dense(target_size, activation=self.final_activation))
        if self.do_summary:
            model.summary()

        return model
