"""Module for layerfactories"""
from abc import ABC, abstractmethod
from typing import List, Optional

# pylint: disable=import-error
from tensorflow.keras import layers


class LayerFactory(ABC):  # pylint: disable=too-few-public-methods
    """Base class for layer factories"""

    @abstractmethod
    def create_layers(self, input_layer):
        """Creates one or multiple layers from an input layer"""


class DownscaleConvBlockFactory(LayerFactory):  # pylint: disable=too-few-public-methods
    """Layer factory for a downscale convolution block"""

    def __init__(
        self,
        channel_list: List[int],
        kernel_size: int = 3,
        activation: str = "relu",
        dropout_values: Optional[List[float]] = None,
    ):
        self.channel_list = channel_list
        self.kernel_size = kernel_size
        self.activation = activation
        self.dropout_values = dropout_values

    def create_layers(self, input_layer):
        for idx, cur_channel_count in enumerate(self.channel_list):
            input_layer = layers.Conv2D(
                cur_channel_count,
                (self.kernel_size, self.kernel_size),
                padding="same",
                activation=self.activation,
            )(input_layer)
            if self.dropout_values is not None and idx < len(self.dropout_values):
                input_layer = layers.Dropout(self.dropout_values[idx])(input_layer)

        input_layer = layers.MaxPooling2D()(input_layer)
        return input_layer


class Conv2DBlockFactory(LayerFactory):  # pylint: disable=too-few-public-methods
    """Layer factory for a convolution block"""

    def __init__(
        self,
        channel_list: List[int],
        kernel_size: int = 3,
        activation: str = "relu",
        dropout_values: Optional[List[float]] = None,
    ):
        self.channel_list = channel_list
        self.kernel_size = kernel_size
        self.activation = activation
        self.dropout_values = dropout_values

    def create_layers(self, input_layer):
        for idx, cur_channel_count in enumerate(self.channel_list):
            input_layer = layers.Conv2D(
                cur_channel_count,
                (self.kernel_size, self.kernel_size),
                padding="same",
                activation=self.activation,
            )(input_layer)
            if self.dropout_values is not None and idx < len(self.dropout_values):
                input_layer = layers.Dropout(self.dropout_values[idx])(input_layer)

        return input_layer
