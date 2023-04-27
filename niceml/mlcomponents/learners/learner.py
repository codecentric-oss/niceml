"""Module for learner"""
from abc import ABC, abstractmethod

from niceml.config.trainparams import TrainParams
from niceml.data.datadescriptions.datadescription import DataDescription
from niceml.data.datasets.dataset import Dataset
from niceml.experiments.experimentcontext import ExperimentContext
from niceml.mlcomponents.modelcompiler.modelcustomloadobjects import (
    ModelCustomLoadObjects,
)
from niceml.mlcomponents.models.modelfactory import ModelFactory


class Learner(ABC):  # pylint: disable=too-few-public-methods
    """Wrapper to do the training"""

    # pylint: disable=too-many-arguments
    @abstractmethod
    def run_training(
        self,
        exp_context: ExperimentContext,
        model_factory: ModelFactory,
        train_set: Dataset,
        validation_set: Dataset,
        train_params: TrainParams,
        data_description: DataDescription,
        custom_objects: ModelCustomLoadObjects,
        callbacks: list,
    ):
        """Runs the training"""
