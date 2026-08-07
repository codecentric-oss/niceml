"""Module for all callback factories"""
from abc import ABC, abstractmethod
from os.path import join
from pathlib import Path
from typing import Any, List, Optional

from niceml.dlframeworks.keras.callbacks.csvlogger import CSVLogger
from niceml.dlframeworks.keras.callbacks.modelcheckpoint import (
    ModelCheckpoint,
)
from niceml.experiments.experimentcontext import ExperimentContext
from niceml.utilities.factoryutils import subs_path_and_create_folder
from niceml.utilities.fsspec.locationutils import join_location_w_path


class CallbackFactory(ABC):  # pylint: disable=too-few-public-methods
    """ABC for creating callbacks"""

    @abstractmethod
    def create_callback(self, exp_context: ExperimentContext):
        """Creates a callback from the given experiment context"""


# pylint: disable=too-few-public-methods
class InitCallbackFactory(CallbackFactory):
    """Creates a callback which doesn't need
    any experiment specific parameters"""

    def __init__(self, callback: Any):
        """Initializes the InitCallbackFactory object with given callback"""
        self.callback = callback

    def create_callback(self, exp_context: ExperimentContext):
        """Returns the callback of the factory"""
        return self.callback


# pylint: disable=too-few-public-methods
class ModelCallbackFactory(CallbackFactory):
    """Creates the model checkpoint callback"""

    def __init__(
        self, model_subfolder: str, model_filename: Optional[str] = None, **kwargs
    ):
        """
        Initializes the ModelCallbackFactory object, which creates
        ModelCheckpoint callbacks. If model_filename is not given, it will
        be inferred from the model_subfolder. Fileextensions will be ignored.

        Args:
            model_subfolder: name of the subfolder to save the model in
            model_filename: filename of the model file without the file extension. If
                model_filename is not given, it will be inferred from the model_subfolder
            **kwargs: additional keyword arguments for ModelCheckpoint initialization
        """
        self.kwargs = kwargs
        self.model_subfolder = (
            model_subfolder if model_filename else str(Path(model_subfolder).parent)
        )
        self.model_filename = model_filename or str(Path(model_subfolder).stem)

    def create_callback(self, exp_context: ExperimentContext) -> ModelCheckpoint:
        """
        Creates the model checkpoint callback based on the given experiment context.
        The ModelCheckpoint callback saves the model of the experiment.

        Args:
            exp_context: experiment to create the model callback for

        Returns:
            ModelCheckpoint callback
        """
        target_model_fs = join_location_w_path(
            exp_context.fs_config, self.model_subfolder
        )
        file_formats = {"run_id": exp_context.run_id, "short_id": exp_context.short_id}
        return ModelCheckpoint(
            target_model_fs,
            file_formats=file_formats,
            model_filename=self.model_filename,
            **self.kwargs
        )


# pylint: disable=too-few-public-methods
class LoggingOutputCallbackFactory(CallbackFactory):
    """Creates a callback that logs the metrics to a csv file"""

    def __init__(self, filename: str = "train_logs.csv"):
        """
        Initializes a LoggingOutputCallbackFactory.

        Args:
            filename: name of the file to save the logging output to
        """
        self.filename = filename

    def create_callback(self, exp_context: ExperimentContext):
        """
        Creates the CSVLogger callback for the given experiment context.
        Args:
            exp_context: experiment context to create the callback for

        Returns:
            CSVLogger callback
        """
        return CSVLogger(experiment_context=exp_context, filename=self.filename)


class CamCallbackFactory(CallbackFactory):  # pylint: disable=too-few-public-methods
    """Callback factory for a cam callback"""

    def __init__(self, images: List[str]):
        """Initializes a CamCallbackFactory"""
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
