"""Module for ABC ModelCompiler"""
from abc import ABC, abstractmethod

from niceml.data.datadescriptions.datadescription import DataDescription
from niceml.mlcomponents.models.modelbundle import ModelBundle
from niceml.mlcomponents.models.modelfactory import ModelFactory


class ModelCompiler(ABC):  # pylint: disable=too-few-public-methods
    """Prepares a model for training"""

    @abstractmethod
    def compile(
        self, model_factory: ModelFactory, data_description: DataDescription
    ) -> ModelBundle:
        """Converts a ModelFactory to a ModelBundle"""
