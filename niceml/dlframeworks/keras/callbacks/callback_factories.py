"""Module for all callback factories"""
from abc import ABC, abstractmethod
from os.path import join
from pathlib import Path
from typing import Any, List, Optional

from dagster import Config
from pydantic import BaseModel, Field

from niceml.config.config import Configurable, InitConfig
from niceml.dlframeworks.keras.callbacks.csvlogger import CSVLogger
from niceml.dlframeworks.keras.callbacks.modelcheckpoint import ModelCheckpoint
from niceml.experiments.experimentcontext import ExperimentContext
from niceml.utilities.factoryutils import subs_path_and_create_folder
from niceml.utilities.fsspec.locationutils import join_location_w_path


class CallbackFactory(ABC):  # pylint: disable=too-few-public-methods
    """ABC for creating callbacks"""

    @abstractmethod
    def create_callback(self, exp_context: ExperimentContext):
        """Creates a callback from the given experiment context"""


# pylint: disable=too-few-public-methods
class InitCallbackFactory(CallbackFactory, Configurable):
    """Creates a callback which doesn't need
    any experiment specific parameters"""

    def __init__(self, callback: Any):
        super().__init__()
        self.callback = callback

    def create_callback(self, exp_context: ExperimentContext):
        return self.callback


# pylint: disable=too-few-public-methods
class ModelCallbackFactory(CallbackFactory, Configurable):
    """Creates the model checkpoint callback"""

    def __init__(
        self, model_subfolder: str = "models", init_kwargs: Optional[dict] = None
    ):
        """
        Creates the model checkpoint callback
        Args:
            model_subfolder: The subfolder where the model will be saved
            init_kwargs: The kwargs for the model checkpoint callback
        """
        super().__init__()
        self.model_subfolder = model_subfolder
        self.init_kwargs = init_kwargs or {}

    def create_callback(self, exp_context: ExperimentContext):
        target_model_fs = join_location_w_path(
            exp_context.fs_config, self.model_subfolder
        )
        file_formats = {"run_id": exp_context.run_id, "short_id": exp_context.short_id}
        return ModelCheckpoint(
            target_model_fs, file_formats=file_formats, **self.init_kwargs
        )


# pylint: disable=too-few-public-methods
class LoggingOutputCallbackFactory(CallbackFactory, Configurable):
    """Creates a callback that logs the metrics to a csv file"""

    def __init__(self, filename: str = "train_logs.csv"):
        """

        Args:
            filename: The filename of the csv file
        """
        self.filename = filename

    def create_callback(self, exp_context: ExperimentContext):
        return CSVLogger(experiment_context=exp_context, filename=self.filename)
