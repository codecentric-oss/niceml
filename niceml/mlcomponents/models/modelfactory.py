"""Module for ModelFactory"""
from abc import ABC, abstractmethod
from typing import Any

from niceml.data.datadescriptions.datadescription import DataDescription


class ModelFactory(ABC):  # pylint: disable=too-few-public-methods
    """ABC for model factories. Used to create the model before training"""

    @abstractmethod
    def create_model(self, data_description: DataDescription) -> Any:
        """Creates a model for training according to the data_description"""
