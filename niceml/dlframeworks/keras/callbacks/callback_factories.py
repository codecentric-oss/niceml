"""Module for all callback factories"""
from abc import ABC, abstractmethod
from os.path import join
from pathlib import Path
from typing import Any, List

from dagster import Config
from pydantic import BaseModel, Field

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
class InitCallbackFactory(CallbackFactory, BaseModel):
    """Creates a callback which doesn't need
    any experiment specific parameters"""

    callback: Any = Field(..., description="The callback to be created")

    def create_callback(self, exp_context: ExperimentContext):
        return self.callback


# pylint: disable=too-few-public-methods
class ModelCallbackFactory(CallbackFactory):
    """Creates the model checkpoint callback"""

    model_subfolder: str = Field(
        default="models", description="The subfolder where the model will be saved"
    )
    init_kwargs: dict = Field(
        default_factory=dict, description="The kwargs for the model checkpoint callback"
    )

    def create_callback(self, exp_context: ExperimentContext):
        target_model_fs = join_location_w_path(
            exp_context.fs_config, self.model_subfolder
        )
        file_formats = {"run_id": exp_context.run_id, "short_id": exp_context.short_id}
        return ModelCheckpoint(
            target_model_fs, file_formats=file_formats, **self.init_kwargs
        )


# pylint: disable=too-few-public-methods
class LoggingOutputCallbackFactory(CallbackFactory, BaseModel):
    """Creates a callback that logs the metrics to a csv file"""

    filename: str = Field(
        default="train_logs.csv", description="The filename of the csv file"
    )

    def create_callback(self, exp_context: ExperimentContext):
        return CSVLogger(experiment_context=exp_context, filename=self.filename)


class CamCallbackFactory(CallbackFactory):  # pylint: disable=too-few-public-methods
    """Callback factory for a cam callback"""

    def __init__(self, images: List[str]):
        self.images = images

    def create_callback(self, exp_context: ExperimentContext):
        """
        Factory method to initialize GRID-CAM callback

        Parameters will be set by parameters.yaml

        Examples:
        callbacks:
            - type: niceml.callbacks.callback_factories.cam_callback_factory
            params:
                image_location: *experiment_path
                images:
                    - /path/to/data/train/Lemon/r_304_100.jpg
                    - /path/to/data/train/Kiwi/2_100.jpg
                    - /path/to/data/train/Walnut/3_100.jpg
                    - /path/to/data/train/Watermelon/2_100.jpg

        Args:
            image_location: path to experiment folder
            images: list of image paths

        """
        filepath = join(exp_context.filepath, "cam")
        filepath = subs_path_and_create_folder(
            filepath, exp_context.short_id, exp_context.run_id
        )

        Path(filepath).mkdir(exist_ok=True, parents=False)

        # pylint: disable=import-outside-toplevel
        from niceml.dlframeworks.keras.callbacks.cam_callback import CamCallback

        return CamCallback(output_dir=filepath, images=self.images)
